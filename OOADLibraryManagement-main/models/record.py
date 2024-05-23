from datetime import datetime
from typing import Optional

from sqlmodel import Column, Field, ForeignKey, Integer, SQLModel
from sqlalchemy.orm import Session
from models import User, Book  # 确保已导入User和Book模型
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, ForeignKey

class Record(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Column(Integer, ForeignKey("user.id"))
    book_id: int = Column(Integer, ForeignKey("book.id"))
    borrowed_time: datetime = Field(...)
    expected_return_time: datetime = Field(...)
    actual_return_time: Optional[datetime] = Field(default=None)
    returned: bool = Field(default=False)

    @staticmethod
    def get_record_by_book_name(db: Session, book_name: str):
        return db.query(Record).join(Book).filter(Book.name == book_name).first()

    def get_borrower_info(self, db: Session):
        borrower = db.query(User).filter(User.id == self.user_id).first()
        borrower_name = borrower.name if borrower else None
        
        return {
            'borrower_name': borrower_name,
            'borrowed_time': self.borrowed_time,
            'expected_return_time': self.expected_return_time,
            'actual_return_time': self.actual_return_time
        }
