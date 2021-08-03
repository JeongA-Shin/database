from bs4 import BeautifulSoup
import requests
import pymongo
import re

conn = pymongo.MongoClient()
actor_db = conn.cine21
actor_collection = actor_db.actor_collection

actor_collection.find_one({})
docs = actor_collection.find({}).limit(3)
for doc in docs:
    print (doc)



### 2.3 Compound(복합) 필드 인덱스-최대 31개의 필드로 만들 수 있음
## 여러 필드를 하나의 인덱스 파일에 넣을 수 있음
actor_collection.create_index([('출연영화', pymongo.TEXT), ('직업', pymongo.TEXT), ('흥행지수', pymongo.DESCENDING)])

docs = actor_collection.find({'$text': {'$search': '가수'}})  
for doc in docs:
    print (doc)


### 2.4 다양한 문자열 검색
# 정규표현식 ($text operator 는 $search operator 와 함께 사용됨) #regex뒤에는 찾는 문자열이 있음(정규 표현식도 포함함!!!!!!!)
#따로 field가 없어도 regex로 하면 찾는 게 가능함
result = actor_collection.find({'출연영화' : {'$regex' : '함께'}})
for record in result:
    print(record)


#실습
#배우중에 중앙대학교를 나온 배우를 흥행지수 순으로 최대 10명 출력하라
#regex는 단어 중간이라도 나오기만 하면 해당되는 듯(완결된 단어가 아니라도 되는 듯)
docs = actor_collection.find({'학교': {'$regex': '중앙'}}).sort('흥행지수',pymongo.DESCENDING).limit(10)
for doc in docs:
    print (doc)

