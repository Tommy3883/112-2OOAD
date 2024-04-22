from randomdata import books, users, borrow_records

book_name_input = input("請輸入要查詢的書籍名稱：")

print("\n借閱紀錄：")
book_found = False
for record in borrow_records:
    if books[record.book_id - 1].book_name == book_name_input:
        book_found = True
        print("借書人:", users[record.user_id - 1].name)
        print("借書時間:", record.borrowed_time)
        print("預計歸還時間:", record.expected_return_time)
        if record.actual_return_time:  # 如果实际归还时间不为空，则表示书籍已归还
            print("實際歸還時間:", record.actual_return_time)
        else:
            print("此書籍尚未歸還")

if not book_found:
    for book in books:
        if book.book_name == book_name_input:
            print("無借閱紀錄，可借閱")
            break
    else:
        print("館藏中無此書籍")
