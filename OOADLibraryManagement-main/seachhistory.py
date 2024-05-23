from fastapi import FastAPI, HTTPException
from models import book, user, record
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import sqlite3

app = FastAPI()

# 與數據庫建立連接
engine = create_engine("sqlite:///library.db")
Session = sessionmaker(bind=engine)
session = Session()

@app.post('/query')
async def query_record(book_name: str):
    # 查詢借閱紀錄
    record = session.query(record).join(book).filter(book.book_name == book_name).first()

    if record:
        # 找到閱紀錄，提取相關訊息
        borrower = session.query(user).filter(user.id == record.user_id).first()
        borrower_name = borrower.name if borrower else None
        borrowed_time = record.borrowed_time
        expected_return_time = record.expected_return_time
        actual_return_time = record.actual_return_time
        
        # 江信息組合成字典返還給前端
        result = {
            'borrower_name': borrower_name,
            'borrowed_time': borrowed_time,
            'expected_return_time': expected_return_time,
            'actual_return_time': actual_return_time
        }
        return result
    else:
        # 如果沒有找到借閱紀錄，檢查書籍列表是否包含該書名
        book_found = False
        '''for book in books:
            if book.book_name == book_name:
                book_found = True
                return {"message": "No record found for the book, but the book is available for borrowing."}
        if not book_found:
            return {"message": "The book is not available in the library collection."}
        '''