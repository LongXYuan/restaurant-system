import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "restaurant.db")

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    # 开启 WAL 模式（SRS 核心要求：允许读写并发）
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # 建表语句
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS tables (
        id INTEGER PRIMARY KEY,
        name_zh TEXT NOT NULL,
        name_es TEXT NOT NULL,
        status TEXT DEFAULT 'free'
    );

    CREATE TABLE IF NOT EXISTS dishes (
        id INTEGER PRIMARY KEY,
        name_zh TEXT NOT NULL,
        name_es TEXT NOT NULL,
        price INTEGER NOT NULL, -- 整数/分
        is_sold_out BOOLEAN DEFAULT 0,
        destination TEXT DEFAULT 'kitchen'
    );

    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_id INTEGER,
        submit_id TEXT UNIQUE,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        batch_id INTEGER,
        station TEXT,
        status TEXT DEFAULT 'pending'
    );

    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id INTEGER,
        dish_id INTEGER,
        quantity INTEGER,
        notes_snapshot TEXT,
        dish_name_es_snapshot TEXT,
        price_snapshot INTEGER,
        status TEXT DEFAULT 'normal'
    );
    """)
    
    # 初始化 20 张桌台
    cursor.execute("SELECT COUNT(*) FROM tables")
    if cursor.fetchone()[0] == 0:
        for i in range(1, 21):
            cursor.execute("INSERT INTO tables (id, name_zh, name_es) VALUES (?, ?, ?)", (i, f"{i}号桌", f"Mesa {i:02d}"))

    # 初始化假菜单（和前端对应）
    cursor.execute("SELECT COUNT(*) FROM dishes")
    if cursor.fetchone()[0] == 0:
        dishes = [
            (1, "鸡肉炒饭", "CHAUFA CON POLLO", 1200),
            (2, "烤猪炒饭", "CHAUFA CHANCHO", 1400),
            (3, "牛肉炒饭", "CHAUFA CARNE", 2000),
            (4, "鸡肉炒面", "TALLARIN POLLO", 1200),
            (5, "秘鲁炒牛柳", "LOMO SALTADO", 2500),
            (6, "烤鸡", "POLLO A LA BRAZA", 1800),
            (7, "白饭", "ARROZ BLANCO", 600),
            (8, "印加可乐", "INCA COLA", 800)
        ]
        cursor.executemany("INSERT INTO dishes (id, name_zh, name_es, price) VALUES (?, ?, ?, ?)", dishes)
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("✅ 数据库初始化完成，已生成 restaurant.db 并写入基础数据！")