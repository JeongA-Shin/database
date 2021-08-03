from bs4 import BeautifulSoup
import requests
import pymongo
import re

conn = pymongo.MongoClient()
actor_db = conn.cine21
text_collection = actor_db.text_collection

text_collection.insert_many(
    [
        { "name": "Java Hut", "description": "Coffee and cakes", "ranking": 1 },
        { "name": "Burger Buns", "description": "Java hamburgers", "ranking": 2 },
        { "name": "Coffee Shop", "description": "Just coffee", "ranking": 3 },
        { "name": "Clothes Clothes Clothes", "description": "Discount clothing", "ranking": 4 },
        { "name": "Java Shopping", "description": "Indonesian goods", "ranking": 5 }
    ]
)


docs = text_collection.find({'name': {'$regex': 'Co.*'}})
for doc in docs:
    print (doc)
#{'_id': ObjectId('61091acee97a037a92781583'), 'name': 'Coffee Shop', 'description': 'Just coffee', 'ranking': 3}

docs = text_collection.find({'name': {'$regex': 'Sh.*'}})
for doc in docs:
    print (doc)
#{'_id': ObjectId('61091ae3de43d37e34eedc91'), 'name': 'Coffee Shop', 'description': 'Just coffee', 'ranking': 3}

#{'_id': ObjectId('61091acee97a037a92781583'), 'name': 'Coffee Shop', 'description': 'Just coffee', 'ranking': 3}
#{'_id': ObjectId('61091acee97a037a92781585'), 'name': 'Java Shopping', 'description': 'Indonesian goods', 'ranking': 5}
#{'_id': ObjectId('61091ae3de43d37e34eedc91'), 'name': 'Coffee Shop', 'description': 'Just coffee', 'ranking': 3}
#{'_id': ObjectId('61091ae3de43d37e34eedc93'), 'name': 'Java Shopping', 'description': 'Indonesian goods', 'ranking': 5}




##이제 regex말고 필드를 만들어서 활용해보자
text_collection.create_index([('name', pymongo.TEXT)])
docs = text_collection.find({'$text': {'$search': 'coffee'}})
for doc in docs:
    print (doc)


docs = text_collection.find({'$text': {'$search': 'java coffee shop'}}) #java, coffee, shop 세 단어 중 하나만 걸리면 됨
for doc in docs:
    print (doc)

'''{'_id': ObjectId('5d4d2d3bc92b650ad6a7cb3d'), 'name': 'Coffee Shop', 'description': 'Just coffee', 'ranking': 3}
{'_id': ObjectId('5d4d2d3bc92b650ad6a7cb3f'), 'name': 'Java Shopping', 'description': 'Indonesian goods', 'ranking': 5}
{'_id': ObjectId('5d4d2d3bc92b650ad6a7cb3b'), 'name': 'Java Hut', 'description': 'Coffee and cakes', 'ranking': 1}'''

docs = text_collection.find({'$text': {'$search': '\"coffee shop\"'}}) #coffe, shop 따로 보지 않고 합쳐서 coffee shop으로 찾고 싶을 때
for doc in docs:
    print (doc)
#{'_id': ObjectId('61091acee97a037a92781583'), 'name': 'Coffee Shop', 'description': 'Just coffee', 'ranking': 3}

docs = text_collection.find({'$text': {'$search': 'Coffee', '$caseSensitive': True}})
#대소문자까지 다 구분해서 정확히 내가 찾는 것과 일치하는 것만 뽑아냄
for doc in docs:
    print (doc)

#실습은 mongo_index_2.py에 해놓음