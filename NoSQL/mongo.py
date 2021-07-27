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
post = {"author": "Mike", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"] }
knowledge_it.insert_one(post) #document를 하나의 변수로 만들어서 insesrt


