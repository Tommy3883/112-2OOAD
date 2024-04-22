from fastapi import FastAPI, HTTPException
from models import book, user, record
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi import Query

app = FastAPI()

# 與資料庫建立連線
engine = create_engine("sqlite:///library.db")
Session = sessionmaker(bind=engine)
session = Session()

@app.post('/query')
async def query_record(book_name: str):
    # 查詢借閱記錄
    record = session.query(record).join(book).filter(book.book_name == book_name).first()

    if record:
        # 找到借閱記錄，提取相關信息
        
        borrower = session.query(user).filter(user.id == record.user_id).first()
        borrower_name = borrower.name if borrower else None
        borrowed_time = record.borrowed_time
        expected_return_time = record.expected_return_time
       
        # 將信息組合成字典返回給前端
        result = {
            'borrower_name': borrower_name,
            'borrowed_time': borrowed_time,
            'expected_return_time': expected_return_time
        }
        
        return result
        
        print("借閱紀錄訊息：")
        print(f"借閱者姓名：{borrower_name}")
        print(f"借閱時間：{borrowed_time}")
        print(f"預計歸還時間：{expected_return_time}")

    else:
        # 如果沒有找到借閱記錄，返回錯誤訊息
        raise HTTPException(status_code=404, detail="No record found for the book")
