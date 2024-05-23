from typing import List

from fastapi import APIRouter, Depends, Request, status, HTTPException
from sqlmodel import Session, select

from dbHelper import get_db
from models.record import Record

router = APIRouter(tags=["record"], prefix="/record")


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[Record],
    summary="Get all records by paging, default page=1, per_page=10",
    responses={
        status.HTTP_200_OK: {"description": "Records retrieved successfully"},
        status.HTTP_404_NOT_FOUND: {"description": "No records found"},
    },
)
def read_records(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 10,
):
    skip = (page - 1) * per_page
    records = db.exec(select(Record).offset(skip).limit(per_page)).all()
    return records

@router.get("/query-record")
async def query_record(book_name: str, db: Session = Depends(get_db)):
    # 使用Record類中的方法查詢借閱紀錄
    record = Record.get_record_by_book_name(db, book_name)
    
    if record:
        # 使用Record實例的方法提取借閱信息
        result = record.get_borrower_info(db)
        return result
    else:
        # 如果沒有找到借閱紀錄，返回相應消息
        raise HTTPException(status_code=404, detail="No record found for the book.")