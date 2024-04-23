import random
from faker import Faker
from datetime import datetime, timedelta
import pandas as pd

# 初始化 faker
faker = Faker()

# 定義書籍類別
class Book:
    def __init__(self, id, book_name, author):
        self.id = id
        self.book_name = book_name
        self.author = author

# 定義使用者類別
class User:
    def __init__(self, id, name, role):
        self.id = id
        self.name = name
        self.role = role

# 定義借閱紀錄類別
class BorrowRecord:
    def __init__(self, user_id, book_id, borrowed_time, expected_return_time, actual_return_time=None, returned=False):
        self.user_id = user_id
        self.book_id = book_id
        self.borrowed_time = borrowed_time
        self.expected_return_time = expected_return_time
        self.actual_return_time = actual_return_time
        self.returned = returned

# 生成書籍資料
books = []
for i in range(1, 201):
    book_name = faker.sentence(nb_words=3)
    author = faker.name()
    book = Book(i, book_name, author)
    books.append(book)

# 生成使用者資料
users = []
for i in range(1, 101):
    name = faker.name()
    role = random.choice(['admin', 'user'])
    user = User(i, name, role)
    users.append(user)

# 生成借閱紀錄
borrow_records = []
borrowed_books = set()  # 用于跟踪已经借出的书籍

for i in range(100):
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


# 将数据转换为DataFrame
books_df = pd.DataFrame([(book.id, book.book_name, book.author) for book in books], columns=["id", "book_name", "author"])
users_df = pd.DataFrame([(user.id, user.name, user.role) for user in users], columns=["id", "name", "role"])
records_df = pd.DataFrame([(record.user_id, record.book_id, record.borrowed_time, record.expected_return_time, record.actual_return_time) for record in borrow_records], columns=["user_id", "book_id", "borrowed_time", "expected_return_time", "actual_return_time"])

# 保存到Excel文件
books_df.to_excel("books.xlsx", index=False)
users_df.to_excel("users.xlsx", index=False)
records_df.to_excel("records.xlsx", index=False)
