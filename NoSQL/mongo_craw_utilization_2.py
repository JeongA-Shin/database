### find의 다양한 문법 (elemMatch)
#* 적어도 한 개 이상의 리스트 요소가 복수 개의 조건을 동시에 만족하는 경우

from bs4 import BeautifulSoup
import requests
import pymongo
import re

conn = pymongo.MongoClient()
actor_db = conn.cine21
elemmatch_sample = actor_db.sample

elemmatch_sample.insert_many([
    {'results': [82, 85, 88]},
    {'results': [75, 88, 91]}
])

docs = elemmatch_sample.find({'results': {'$gte': 90, '$lt':85}})
for doc in docs:
    print (doc)
#즉 여기서 90보다 크고, 85보다 작다는 조건을 만족하는 요소가 <<<모두>>> 있어야 document가 해당되는 거임
#'results': [82, 85, 88] 따라서 얘는 해당 안 되고(82가 있어도 90보다 큰 것을 만족하는 게 없으므로)
#'results': [75, 88, 91] 이게 해당되는 거임


docs = elemmatch_sample.find({'results': {'$elemMatch': {'$gte':75, '$lt':80}}})
for doc in docs:
    print (doc)   

#실습->mongo_craw_utilization.py에서 함
#직업이 가수인 배우 중, 흥행지수가 가장 높은 배우순으로 10명을 출력하세요
#국가부도의 날에 출연한 배우를 흥행지수가 높은 순으로 10명 출력하세요 

