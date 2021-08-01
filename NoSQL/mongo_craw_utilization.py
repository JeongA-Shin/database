#mongo_craw.py를 통해 mongoDB에 저장한 데이터들을 기반으로 (즉 이미 mongo_craw.py를 실행하고 mongoDB에 데이터 넣은 상황임)
#필요한 정보들(EX)흥행지수가 높은 배우순 을 뽑아내는 방법

#1.라이브러리 import
from bs4 import BeautifulSoup
import requests
import pymongo
import re #정규표현식을 위한 라이브러리

#2. mongodb 연결,db,collection 생성/선택
connection=pymongo.MongoClient()#mongoDB에 연결
actor_db=connection.cine21 #database지정(없었다면 만들어짐)
actor_collection=actor_db.actor_collection # collection지정(없었다면 만들어짐)

print(actor_collection.find_one({}))

docs=actor_collection.find({}).limit(3)#3개만 찾음
for doc in docs:
    print(doc) 


### 1.1. 컬럼명 변경 
#* 저장되어 있는 mongodb 데이터의 컬럼명을 변경하는 방법
#* update_one()/update_many() 함수 활용
actor_collection.update_many({},{'$rename':{'배우이름':'배우 이름'}}) #모든 document들을 모두 보되, 배우이름을 배우 름으로 수정
docs=actor_collection.find({}).limit(3)#3개만 찾음
for doc in docs:
    print(doc) 



### 1.2 find의 다양한 문법 - sort

#그냥 이렇게 하면 생년월일이 없는 걸 우선순위(젤 위로)로 하므로 없는 배우들 정보가 먼저 나옴#
#즉, sort의 default는 ASCENDING임
#docs=actor_collection.find({},{'_id':0}).sort('생년월일').limit(10)#우선 전체를 보고 생년월일로 sort를 한 후 10개의 document만 가져옴
docs=actor_collection.find({},{'_id':0}).sort('생년월일',pymongo.DESCENDING).limit(10) #내림차순(2011->2010 즉 어린 순서)
for doc in docs:
    print(doc)


### 1.3 find의 다양한 문법 - exists
docs=actor_collection.find({'특기':{'$exists':True}},{'_id':0}).sort('흥행지수',pymongo.DESCENDING) 
#첫 번째 {}, 즉 where문에 해당되는 것에 조건임. 특기가 있는 document만 뽑아냄
#두 번째 {}는 출력하고 싶은/않은 필드명들을 지정
for doc in docs:
    print(doc)


print("------실습------")

###실습
##생년월일이 없는 doc의 actor_name 만 출력하기   
docs=actor_collection.find({'생년월일':{'$exists':False}},{'_id':0,'배우 이름':1}) #내가 보고 싶은 것만 1로 해주면 나머지는 0이 됨
for doc in docs:
    print(doc)



### 1.4 find의 다양한 문법 - 필드값 범위로 검색
docs=actor_collection.find({'흥행지수':{'$gte':10000},'출연영화':'모가디슈'},{'_id':0,'배우 이름':1,'출연영화':1})
# 흥행지수가 10000이상이고, 출연영화에 모가디슈가 있는 document들 중에! 배우 이름,출연영화만 출력
for doc in docs:
    print(doc)

### find의 다양한 문법 - or ::반드시!!! or은 list 형태로 해줘야 한다!
docs=actor_collection.find({'$or':[{'출연영화':'모가디슈'},{'출연영화':'발신제한'}]},{'_id':0,'배우 이름':1,'출연영화':1})
# 출연영화에 모가디슈 혹은! 발신제한이 있는 document 중에, 배우 이름,출연영화만 출력
for doc in docs:
    print(doc)

### 여러 조건들 섞기(범위-gte,or)
##or은 반드시 []형태여야 함!!!!!!!
#or은 반드시 list형태가 와야 함!{}들은 그 요소
docs = actor_collection.find({ '흥행지수': {'$gte': 10000}, '$or': [{'출연영화':'극한직업'}, {'출연영화':'더 킹'}] }, {'배우이름':1, '출연영화':1, '_id':0})
for doc in docs:
    print(doc)

### find의 다양한 문법 - nor (즉,결과적으로는 and와 같은 기능)
docs = actor_collection.find({'$nor': [{'흥행지수': { '$gte': 10000}}, {'흥행지수': { '$lte': 2000}}]}, {'배우이름':1, '흥행지수':1, '_id':0}).limit(3)
#흥행지수가 2000~10000인 document들을 찾음
for doc in docs:
    print (doc)



### find의 다양한 문법 - in, nin + 리스트 자료형: 리스트 안에 해당되는 요소가 있는지 확인
# in: 들어가 있다.
# nin: not in - 들어가 있지 않다.
docs = actor_collection.find({'흥행지수': { '$in': [9182, 8439]}}, {'배우이름':1, '흥행지수':1, '_id':0})
#흥행지수가 9182,8439 중에 있는 것을 찾음.(리스트 안에 해당 되는 것이 있는지)
for doc in docs:
    print (doc)

docs = actor_collection.find({'흥행지수': { '$nin': [9182, 8439]}}, {'배우이름':1, '흥행지수':1, '_id':0}).limit(3)
#리스트의 요소에 해당되지 않는 document들을 뽑음
for doc in docs:
    print (doc)

##실습
#흥행지수 가 9182, 8439가 아니고, 10000 이하인 데이터를 3개만 검색하세요. (nor, in, gt 활용, 배우이름과 흥행지수만 출력)
#or은 반드시 list형태가 와야 함!{}들은 그 요소
docs=actor_collection.find({'$nor':[{'흥행지수':{'$in':[9182,8439]}},{'흥행지수':{'$gt':1000}}]},{'_id':0,'배우 이름':1,'흥행지수':1}).limit(3)
for doc in docs:
    print (doc)


### find의 다양한 문법 - skip, limit
##* skip(n): 검색 결과 n개만큼 건너뜀
##* limit(n): 검색 결과 n개만 표시
docs=actor_collection.find({'흥행지수':{'$gte':10000}}).skip(3).limit(5) #조건에 맞는 검색 결과에서 처음 3개의 document들은 제외하고 그 후의 결과를 보여줌
for doc in docs:
    print (doc)



##만약 document의 data 중에 리스트 자료형이 있다면
#아래처럼 리스트 요소 중 하나만 조건에 해당되어도 그 document를 뽑아올 수 있음
docs = actor_collection.find({'출연영화': '극한직업'})
for doc in docs:
    print (doc)


#and나 or같은 조건들은 리스트 안에 넣어줘야 함[{},{}]
docs = actor_collection.find({'$or': [{'출연영화': '극한직업'}, {'출연영화': '사바하'}]})
for doc in docs:
    print (doc)

### find의 다양한 문법 - list 검색 (all)
# find의 리스트 요소 모두를 가지고 있는 (그 외에 더 있어도 상관 없음) document를 뽑아냄
docs = actor_collection.find({'출연영화': { '$all': ['변산', '사바하']}})
for doc in docs:
    print (doc)



### find의 다양한 문법 - list 검색 (리스트 index 번호로 검색하기)
docs = actor_collection.find({'출연영화.0': '사바하'}) #document에서 list 자료형을 가지는 출연영화에서 0번째 데이터가 사바하인 것을 찾아라
for doc in docs:
    print (doc)




### find의 다양한 문법 - list 검색 (리스트 사이즈로 검색하기)
docs = actor_collection.find({'출연영화': {'$size': 5}}) #document에서 list 자료형을 가지는 출연영화에서 그 요소가 5개인 document를 찾아라
for doc in docs:
    print(doc)


#실습->mongo_craw_utilization.py에서 함
#직업이 가수인 배우 중, 흥행지수가 가장 높은 배우순으로 10명을 출력하세요
docs=actor_collection.find({'직업':'가수'}).sort('흥행지수',pymongo.DESCENDING).limit(10)
for doc in docs:
    print(doc)


#국가부도의 날에 출연한 배우를 흥행지수가 높은 순으로 10명 출력하세요 
docs=actor_collection.find({'출연영화':'국가부도의 날'}).sort('흥행지수',pymongo.DESCENDING).limit(10)
for doc in docs:
    print(doc)
