#request method 에 따라 다름
#GET:각 페이지에 접속할 때마다 주소가 다름 -->request.get(....)
#주소에 일정한 정보들이 들어있음 예)www.cine21.rank/actor....
#POST:각 페이지에 접속해도 주소가 달라지지 않음 ---> request.post(.....)
#주소에 별도로 데이터가 들어가 있지 않고, 따로(header를 통해) data를 전송함
#예)
'''
section: actor
period_start: 2021-06
gender: all
page: 1

'''


'''
## 크롤링과 데이터 베이스 예제
#cine21 배우 랭킹 사이트 크롤링
#사이트 주소:http://www.cine21.com/rank/person
# 요청방식 확인: 개발자 모드로 들어가서, (F12), network->content 페이지 요청 확인
#preserve log 체크 하고, all 체크한 후에 
1.header의 general부분에서 
Request URL: http://www.cine21.com/rank/person/content
Request Method: POST
Status Code: 200 OK
Remote Address: 115.68.232.4:80
Referrer Policy: strict-origin-when-cross-origin
을 보고 request url 확인

2. header의 form data 부분
section: actor
period_start: 2021-06
gender: all
page: 1
등의 데이터를 확인
# # '''



#1.라이브러리 import
from bs4 import BeautifulSoup
import requests
import pymongo
import re #정규표현식을 위한 라이브러리

#2. mongodb 연결,db,collection 생성/선택
connection=pymongo.MongoClient()#mongoDB에 연결
#print(connection) 연결확인
actor_db=connection.cine21 #database만들기
actor_collection=actor_db.actor_collection # collection만들기

#3.크롤링 주소 request
cine21_url='http://www.cine21.com/rank/person/content'
#form data를 딕셔너리로 만들자
post_data=dict()
post_data["section"]='actor'
post_data["period_start"]='2021-6'
post_data["gender"]='all'
post_data["page"]=1


#post방식의 데이터 크롤링
res=requests.post(cine21_url,data=post_data)

#4. 데이터 파싱,추출
#여기서부터는 전과 같이 css selector등을 활용해서 추출
soup=BeautifulSoup(res.content,'html.parser')
actors=soup.select('div.name > a') #리스트로 반환됨


#정규표현식 활용해서 필요한 부분만 출력
for actor in actors:
    actor_data=actor.get_text()
    print(re.sub("\(\w+\)", "",actor_data))



