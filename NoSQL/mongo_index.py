## 2. mongodb 인덱스 (INDEX)
#- 검색을 더 빠르게 수행하고자 만든 추가적인 data structure
#  - index 데이터 구조가 없다면, 컬렉션에 있는 데이터를 하나씩 조회하는 방식으로 검색이 됨

### 2.1 기본 인덱스 _id
#- 모든 mongodb 컬렉션은 기본적으로 _id 필드를 기반으로 기본 인덱스가 생성됨

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

#actor = actor_collection



### 2.2 Single(단일) 필드 인덱스
actor_collection.create_index('배우이름')
print(actor_collection.index_information()) # index 정보 확인: index_information()
'''
{'_id_': {'v': 2, 'key': [('_id', 1)]}, '배우이름_1': {'v': 2, 'key': [('배우이름', 1)]}}

- key: ('필드명', direction)
  - direction
    - pymongo.ASCENDING = 1  //디폴트임
    - pymongo.DESCENDING = -1
    - pymongo.TEXT = 'text'  ##텍스트 검색이 용이하도록 만들어달라는 의미

'''

##전체 인덱스 삭제
actor_collection.drop_indexes()
print(actor_collection.index_information()) # index 정보 확인: index_information()
'''
{'_id_': {'v': 2, 'key': [('_id', 1)]}} #배우이름 필드 부분이 삭제됨

'''

## 특정 인덱스 삭제  #파라미터로 리스트 안에 key부분을 direction까지 정확히 써주면 됨
# 하나 그 이상 여러개 삭제할 수도 있음: actor_collection.drop_index([('배우이름', 1)],['또 삭제할 필드명','그 필드의 direction'])
#actor_collection.drop_index([('배우이름', 1)])


#### 여러개의 single index 생성 가능
actor_collection.create_index([('배우이름', 1)])
actor_collection.create_index('흥행지수')
actor_collection.create_index('랭킹')
actor_collection.create_index([('출연영화', 'text')])
### collection의 인덱스에 text는 단 하나만 존재해야 한다!!!!
print(actor_collection.index_information())
'''
'배우이름_1': {'v': 2, 'key': [('배우이름', 1)]}, '
흥행지수_1': {'v': 2, 'key': [('흥행지수', 1)]}, 
'랭킹_1': {'v': 2, 'key': [('랭킹', 1)]}, 

'출연영화_text': {'v': 2, 'key': [('_fts', 'text'), ('_ftsx', 1)], 'weights': SON([('출연영화', 1)]), 
'default_language': 'english', 'language_override': 'language', 'textIndexVersion': 3}}

'''



#### 부분 문자열 검색: $text
print("----------------------------------------------------")
docs = actor_collection.find({'$text': {'$search': '가수'}})  #'너의'가 들어간 출연 영화들을 뽑음
for doc in docs:
    print (doc)
'''
{'_id': ObjectId('61056f03cd4f1f750a8b0cf6'), '흥행지수': 143443, '출연영화': ['발신제한', '너의 이름은.', '조작된 도시'], '랭킹': '2', '직업': '배우', '생년월일': '1987-07-05', '성별': '남', '홈페이지': '\nhttps://twitter.com/jichangwook\nhttps://www.instagram.com/jichangwook/\n', '신장/체중': '180cm, 65kg', '학교': '단국대학교
 공연영상학부', '특기': '노래, 유도, 수영', '소속사': '(주)글로리어스', '배우 이름': '지창욱'}
'''



