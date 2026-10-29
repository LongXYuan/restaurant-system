from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/ping")
def ping():
    return {"message": "Pong! 后端已经跑起来了。"}

# 新增获取桌台列表的接口
@app.get("/api/tables")
def get_tables():
    # 模拟生成 20 张桌台的数据
    tables = []
    for i in range(1, 21):
        # 为了演示，我们让 15 号桌变成用餐中
        status = "busy" if i == 15 else "free"
        amount = 45.00 if i == 15 else 0.00
        
        tables.append({
            "id": i,
            "name_zh": f"{i}号桌",
            "name_es": f"Mesa {i:02d}",
            "status": status,
            "amount": amount
        })
    return tables

@app.get("/api/menu")
def get_menu():
    # 模拟真实的菜单数据，带有交叉 Tags
    menu = [
        {"id": 1, "name_es": "CHAUFA CON POLLO", "name_zh": "鸡肉炒饭", "price": 12.00, "tags": ["炒饭", "鸡肉"]},
        {"id": 2, "name_es": "CHAUFA CHANCHO", "name_zh": "烤猪炒饭", "price": 14.00, "tags": ["炒饭", "猪肉"]},
        {"id": 3, "name_es": "CHAUFA CARNE", "name_zh": "牛肉炒饭", "price": 20.00, "tags": ["炒饭", "牛肉"]},
        {"id": 4, "name_es": "TALLARIN POLLO", "name_zh": "鸡肉炒面", "price": 12.00, "tags": ["炒面", "鸡肉"]},
        {"id": 5, "name_es": "LOMO SALTADO", "name_zh": "秘鲁炒牛柳", "price": 25.00, "tags": ["热菜", "牛肉", "招牌"]},
        {"id": 6, "name_es": "POLLO A LA BRAZA", "name_zh": "烤鸡", "price": 18.00, "tags": ["热菜", "鸡肉", "招牌"]},
        {"id": 7, "name_es": "ARROZ BLANCO", "name_zh": "白饭", "price": 6.00, "tags": ["主食"]},
        {"id": 8, "name_es": "INCA COLA", "name_zh": "印加可乐", "price": 8.00, "tags": ["饮料"]},
    ]
    return menu