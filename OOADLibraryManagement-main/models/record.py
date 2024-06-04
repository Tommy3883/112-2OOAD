from datetime import datetime
from typing import Optional

from sqlmodel import Column, Field, ForeignKey, Integer, SQLModel
from sqlalchemy.orm import Session
from models import user, book  # 導入User和Book模型
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import select

class Record(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Column(Integer, ForeignKey("user.id"))
    book_id: int = Column(Integer, ForeignKey("book.id"))
    borrowed_time: datetime = Field(...)
    expected_return_time: datetime = Field(...)
    actual_return_time: Optional[datetime] = Field(default=None)
    #returned: bool = Field(default=False)
    
    # @classmethod
    # def get_record_by_book_id(cls, db: Session, id: int):
    #         return db.exec(
    #             select(cls)
    #             .where(cls.book_id == id)
    #         ).first()
    