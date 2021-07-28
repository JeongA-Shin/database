###참고
#1.import pymongo
#2.mongoDB 접속 (주소)
#3.사용할 database,collection 생성 또는 선택
#4.해당 database의 collection에 CRUD 명령하는 방법


import pymongo #pymongo를 통해 mongoDB 활용
connection=pymongo.MongoClient() #일단 mongoDB에 연결
#디폴트는 localhost의 27017로 접속
#만약에 ec등으로 접속한다면 
# connection=pymongo.MongoClient('mongodb://13.209.140.30',12301) 이렇게 파라미터에 주소를 넣음, 포트 번호도 바꾸고 싶으면 임의로 지정(12301)

#db 선택하기 -없으면 만들어짐!
knowledge=connection.knowledge #db=connection["test"] 이렇게도 가능함
#knowledge 변수 안에 mongodb의 knowledge라는 db가 담겨져 있는 거임
#print(knowledge)
#연결되었는지 확인 Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'test') 뜨면 됨
#에러 안 나면 됨

#print(knowledge.name) #knowledge

#사용하고 있는 db에 collection생성하기
#(얘도 db와 마찬가지로 없으면 만들어짐)
knowledge_it=knowledge.it #knowledge라는 db안의 it라는 collection 정보가 knowledge_it라는 변수 안에 담겨 있음
#it=knowledge["it"]  이렇게도 가능
#print(knowledge_it) #확인을 위한 print

#이제 CRUD
#*insert_one()
#mongo shell에서는 insertOne()이었지만 pymongo 라이브러리에서는 insert_one()이라는 메소드를 사용한다.
#pymongo는 python에 기반을 두므로 반드시 key 마다 따옴표를 해줘야 한다!
post = {"author": "Mike", "text": "My first blog post!","tags": ["mongodb", "python", "pymongo"] }
#post_id=knowledge_it.insert_one(post) #document를 하나의 변수로 만들어서 insesrt

#print(post_id)#정상적으로 insert되었는지 알 수 있음
#따로 확인 안 하려면 그냥 knowledge_it.insert_one(post)만 해줘도 됨(변수에 따로 안 넣고)
#print(post_id.inserted_id) #해당 document의 유니크한 아이디를 알려줌

#여러 개 입력시
'''knowledge_it.insert_many([
    {"author":"Dave","age":25},
    {"author":"Dave Lee","age":35}
])'''

'''1. key는 string만 가능하지만, value는 다양한 자료형이 가능함
    # 리스트, 객체 삽입 가능
    knowledge_it.insert_one({'title' : '암살', 'castings' : ['이정재', '전지현', '하정우']})
    knowledge_it.insert_one(
        {
            'title' : '실미도', 
            'castings' : ['설경구', '안성기'], 
            'datetime' : 
            {
                'year' : '2003', 
                'month' : 3,
                'val' : 
                {
                    'a' :
                    {
                        'b' : 1
                    }
                }
            }
        }
    )

   2. 파이썬 기본 문법을 통해 document를 만들 수 있음
    data = list()
    data.append({'name' : 'aaron', 'age' : 20})
    data.append({'name' : 'bob', 'age' : 30})
    data.append({'name' : 'cathy', 'age' : 25})
    data.append({'name' : 'david', 'age' : 27})
    data.append({'name' : 'erick', 'age' : 28})
    data.append({'name' : 'fox', 'age' : 32})
    data.append({'name' : 'hmm'})

    knowledge_it.insert_many(data)
'''

#document 개수 세기: 1.estimated_document_count() or 2.count_documents()
#count_documents(): 메서드, 수업에서는 그냥 count만 씀 그런데 아래의 경고도 떠서 찾아보니까 내가 한 것처럼 해야 함
#or db.collection.estimated_document_count({})
#count is deprecated. Use estimated_document_count or count_documents instead. Please note that $where must be replaced by $expr, 
# $near must be replaced by $geoWithin with $center, and $nearSphere must be replaced by $geoWithin with $centerSphere
print(knowledge_it.count_documents({})) #총 document 수를 알려줌
#내가 원하는 조건에 맞는 document 수를 뽑아내려면 {}안에 조건 넣으면 됨
print(knowledge_it.count_documents({"author":"Dave"}))



#5.5 Document 검색 하기(읽기) -> find_one()과 find()
#find_one():가장 빨리 검색되는 하나 검색하기
print(knowledge_it.find_one())
#* find_one( 안에 조건을 넣을 때는 사전 형식으로 해야 합니다. { 키:값 } )
print(knowledge_it.find_one({"author":"Dave"}))#find_one에 조건 달기 (sql에서의 where문)
#dave=knowledge_it.find_one()  print(dave) 이렇게 해주면 확인 됨

#* find() 메서드 : 검색되는 모든 Document 읽어오기
#find로 찾으면 그 결과가 리스트로 넘어옴!->for문을 통해 다뤄줌
#원하는 것만 뽑으려면 find({},{})안에 조건이랑 보고 싶은 record를 써줌
docs=knowledge_it.find({},{"_id":0})
for item in docs:
    print(item)

docs=knowledge_it.find({},{})
for post in docs.sort("age",1): #age의 value로 sort함,1이면 오름차순, -1이면 내림차순
    print(post)


### 5.6. Document Update 하기 (update_one() 과 update_many())
# 즉, document의 수정 및 추가
#mongoDB에서의 구문:db.people.updateMany( { age: { $gt: 25 } }, { $set: { status: "C" } } )
#* update_one() : 가장 먼저 검색되는 한 Document만 수정하기
knowledge_it.update_one({"author":"Dave"}, #첫 번째 {}안에는 수정할 document를 가르키는 조건문(sql의 where문)
{
    "$set":
    {"text":"hello!"} ##두 번째 {}는 수정문(기존에 없는 record면 추가되는 거임)
})

#print(knowledge_it.find_one({"author":"Dave"}))
knowledge_it.update_one({"author":"Dave Lee"}, #첫 번째 {}안에는 수정할 document를 가르키는 조건문(sql의 where문)
{
    "$set":
    {"author":"Dave"} ##두 번째 {}는 수정문(기존에 없는 record면 추가되는 거임)
})

print("***********************")
knowledge_it.update_many({"author":"Dave"},{"$set":{"text":"My second blog post!"}})
docs=knowledge_it.find({},{"_id":0})
for item in docs:
    print(item)


### 5.7. Document 삭제 하기 (delete_one() 과 delete_many())
#* delete_one() 메서드 : 가장 먼저 검색되는 한 Document만 삭제하기
print("*************here***************")
knowledge_it.delete_one({"author":"Dave"})
docs=knowledge_it.find({"author":"Dave"},{"_id":0})
for item in docs:
    print(item)

#* delete_many() 메서드 : 조건에 맞는 모든 Document 삭제하기
print("*************here***************")
knowledge_it.delete_many({"author":"Mike"})
print(knowledge_it.count_documents({"author":"Mike"})) #0