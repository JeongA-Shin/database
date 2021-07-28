#import
import pymongo

#연결
connection=pymongo.MongoClient() #localhost연결이므로 따로 인자를 주지 않음
books=connection.books #books라는 db 만들고 books라는 변수에 담음
book_it=books.book_it #db인 books안에 book이라는 collection

data=list()
for index in range(100):
    data.append({"author":"jeong","publisher":"yours.com","number":index})

#CRUD- CREATE
book_it.insert_many(data) #리스트의 각 요소들이 document로 들어가게 됨

#CRUD - READ
print("read:")
for item in book_it.find({},{"_id":0}):
    print(item)


#CRUD - UPDATE
print("update: ")
book_it.update_many({},{"$set":{"publisher":"www.yours.com"}})

for item in book_it.find({},{"_id":0}):
    print(item)


#CRUD - DELETE
#number 가 6 이상(>=)인 doc 삭제하기
print("delete: ")
book_it.delete_many({"number":{"$gte":6}})
for item in book_it.find({},{"_id":0}):
    print(item)
