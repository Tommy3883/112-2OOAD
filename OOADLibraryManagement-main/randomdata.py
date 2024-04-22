import random
from faker import Faker
from datetime import datetime, timedelta
from dataclasses import dataclass

# 初始化 faker
faker = Faker()

# 定義書籍類別
@dataclass
class Book:
    id: int
    book_name: str
    author: str

# 定義使用者類別
@dataclass
class User:
    id: int
    name: str
    role: str

# 定義借閱紀錄類別
@dataclass
class BorrowRecord:
    user_id: int
    book_id: int
    borrowed_time: datetime
    expected_return_time: datetime
    actual_return_time: datetime = None
    returned: bool = False

# 生成書籍資料
books = []
for i in range(1, 21):
    book_name = faker.sentence(nb_words=3)
    author = faker.name()
    book = Book(i, book_name, author)
    books.append(book)

# 生成使用者資料
users = []
for i in range(1, 11):
    name = faker.name()
    role = random.choice(['admin', 'user'])
    user = User(i, name, role)
    users.append(user)

# 生成借閱紀錄
# 生成借閱紀錄
borrow_records = []
borrowed_books = set()  # 用于跟踪已经借出的书籍

for i in range(10):
    user_id = random.randint(1, 10)
    book_id = random.randint(1, 20)
    
    # 检查书籍是否已经借出且未归还
    if book_id in borrowed_books:
        continue  # 如果已经借出且未归还，则跳过生成借阅记录
    
    borrowed_books.add(book_id)  # 将书籍标记为已借出
    
    borrowed_time = faker.date_time_between(start_date='-30d', end_date='now')
    expected_return_time = borrowed_time + timedelta(days=random.randint(7, 30))
    
    # 模拟实际还书时间
    if random.choice([True, False]):  # 50% 的概率书已经归还
        actual_return_time = borrowed_time + timedelta(days=random.randint(1, 30))
        returned = True  # 设置书籍已归还
    else:
        actual_return_time = None  # 未归还的情况，使用 None 代替
        returned = False  # 设置书籍未归还
    
    record = BorrowRecord(user_id, book_id, borrowed_time, expected_return_time, actual_return_time, returned)
    borrow_records.append(record)



# 打印生成的資料
print("書籍資料：")
for book in books:
    print(book.id, book.book_name, book.author)

print("\n使用者資料：")
for user in users:
    print(user.id, user.name, user.role)

print("\n借閱紀錄：")
for record in borrow_records:
    print(record.user_id, record.book_id, record.borrowed_time, record.expected_return_time, record.actual_return_time)
