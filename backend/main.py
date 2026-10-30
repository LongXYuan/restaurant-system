from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from database import get_db, init_db

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- 数据模型 -----
class OrderItem(BaseModel):
    dish_id: int
    name_es: str
    quantity: int
    remarks: List[str]

class OrderSubmit(BaseModel):
    table_id: int
    submit_id: str
    items: List[OrderItem]

# ----- 接口 -----

@app.get("/api/tables")
def get_tables():
    conn = get_db()
    tables = conn.execute("SELECT * FROM tables").fetchall()
    conn.close()
    
    result = []
    for t in tables:
        # 直接读取数据库里的真实状态！
        real_status = t["status"] 
        
        result.append({
            "id": t["id"], 
            "name_zh": t["name_zh"], 
            "name_es": t["name_es"],
            # 如果是 busy 就传 busy，否则传 free
            "status": "busy" if real_status == "busy" else "free", 
            "amount": 45.00 if real_status == "busy" else 0.00 # 金额暂时写死，以后再算
        })
    return result

@app.get("/api/menu")
def get_menu():
    # 从数据库真实读取菜单
    conn = get_db()
    dishes = conn.execute("SELECT * FROM dishes WHERE is_sold_out = 0").fetchall()
    conn.close()
    
    # 为了兼容前端的 tags，这里先死板地把所有菜都随便塞两个 tag (后续我们会建立真正的 Tag 表)
    menu = []
    for d in dishes:
        menu.append({
            "id": d["id"], "name_es": d["name_es"], "name_zh": d["name_zh"],
            "price": d["price"] / 100.0, # 把分转成元
            "tags": ["招牌", "热菜"] if d["id"] < 5 else ["饮料"] # 暂时的假tag
        })
    return menu

@app.post("/api/orders")
def submit_order(order: OrderSubmit):
    conn = get_db()
    try:
        # 开启事务防并发
        conn.execute("BEGIN IMMEDIATE")
        
        # 1. 幂等去重（防连点）
        existing = conn.execute("SELECT id FROM orders WHERE submit_id = ?", (order.submit_id,)).fetchone()
        if existing:
            conn.rollback()
            return {"status": "success", "message": "订单已存在，忽略重复提交"}
            
        # 2. 写入订单主表
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (table_id, submit_id) VALUES (?, ?)", (order.table_id, order.submit_id))
        order_id = cursor.lastrowid
        
        # 3. 写入出单票 (这里暂时所有菜都发给厨房)
        cursor.execute("INSERT INTO tickets (order_id, batch_id, station) VALUES (?, 1, 'kitchen')", (order_id,))
        ticket_id = cursor.lastrowid
        
        # 4. 写入订单明细
        for item in order.items:
            # 查真实价格快照
            dish = cursor.execute("SELECT price FROM dishes WHERE id = ?", (item.dish_id,)).fetchone()
            price_snapshot = dish["price"] if dish else 0
            
            cursor.execute("""
                INSERT INTO order_items (ticket_id, dish_id, quantity, notes_snapshot, dish_name_es_snapshot, price_snapshot) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (ticket_id, item.dish_id, item.quantity, ",".join(item.remarks), item.name_es, price_snapshot))
            
        # 5. 更新桌台状态
        cursor.execute("UPDATE tables SET status = 'busy' WHERE id = ?", (order.table_id,))
            
        conn.commit()
        print(f"\n✅ [数据库落盘] 订单 {order_id} 写入成功！桌号: {order.table_id}\n")
        return {"status": "success", "message": "订单已接收并入库"}
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ 订单写入失败: {e}\n")
        raise HTTPException(status_code=500, detail="订单写入失败")
    finally:
        conn.close()