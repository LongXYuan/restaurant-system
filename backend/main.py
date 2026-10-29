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