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


'''#정규표현식 활용해서 필요한 부분만 출력- 배우 이름만 출력
for actor in actors:
    actor_data=actor.get_text()
    print(re.sub("\(\w+\)", "",actor_data))'''


"""
#5. 배우 이름을 클릭해서 전환된 페이지에 나오는 상세 정보 출력하기
actor_info_list=list()

for actor in actors:
    actor_data=actor.get_text()
    print(re.sub("\(\w+\)", "",actor_data)) #이름 출력
    #<a href="/db/person/info/?person_id=30235">진경(1편)</a> --->그냥 actor는 이렇게 나옴
    #print(actor['href']) #해당 이름에 걸린 사이트 주소 /db/person/info/?person_id=30235
    #그런데 full 주소는 http://www.cine21.com/db/person/info/?person_id=30235 이런 식으로 앞에 http://www.cine21.com붙여야함 따라서
    #print("http://www.cine21.com"+actor["href"]) #즉 얘가 이제 새로운 주소가 되는 거임 http://www.cine21.com/db/person/info/?person_id=98611
    actor_link="http://www.cine21.com"+actor["href"] #이제 이 주소로 다시 크롤링
    res_actor=requests.get(actor_link)#이번에는 get형식임
    soup_actor=BeautifulSoup(res_actor.content,'html.parser')
    #<li><span class="tit">직업</span>배우</li>
    default_info=soup_actor.select_one('ul.default_info')
    actor_details=default_info.select('li')#<ul class="default_info"> 이거는 안 봐도 되니까
    
    actor_info_dict=dict()
    for actor_item in actor_details:
        '''#print(actor_item) #<li><span class="tit">소속사</span>싸이더스 HQ</li>
        print(actor_item.select_one('span.tit').get_text()) #필드명  #<span class="tit">소속사</span>
        actor_item_value=re.sub('<span.*?>.*?</span>', '', str(actor_item)) #반드시 string으로 re를 해줘야 함!
        actor_item_value=re.sub('<.+?>', '', actor_item_value) 
        print(actor_item_value)#해당 필드의 데이터
        #mongoDB에 넣으려면 딕셔녀리 자료형으로 만들어야 함'''
        actor_item_field=actor_item.select_one('span.tit').get_text()
        actor_item_value=re.sub('<span.*?>.*?</span>', '', str(actor_item)) #반드시 string으로 re를 해줘야 함!
        actor_item_value=re.sub('<.+?>', '', actor_item_value) 
        actor_info_dict[actor_item_field]=actor_item_value
    actor_info_list.append(actor_info_dict)


for item in actor_info_list:
    print(item)

###참고: 특수한 정규 표현식
'''
 html
 -Greedy(.*) vs Non-Greedy(.*?)
 -https://regexr.com :정규 표현식에 따른 결과를 보여줌
 - <li><span class="tit">직업</span>배우</li>
 - . 문자는 줄바꿈 문자인 \n을 제외한 모든 문자 한 개를 의미
 - *는 앞 문자가 0번 또는 그 이상 반복되는 패턴
 - .* : 문자열 전체
 - greedy는 해당 패턴이 매치 되는 그 전체를 모두 포함 (부분 집합, 전체 집합 모두 봄)
  예) <.*>에서
  - <li>,<span class="tit">,</span>,</li>을 포함한  <li><span class="tit">직업</span>배우</li>

 - non greedy는 하나의 패턴만 봄(부분 집합만 취급함)
  예) 위와 같은 상황에서
  -<li>,<span class="tit">,</span>,</li>

'''

##6. 흥행지수와 출연한 영화 추출
#actors=soup.select('div.name > a') #리스트로 반환됨, 제일 위에서 정의된 것임
hits=soup.select('ul.num_info > li > strong')
movies=soup.select('ul.mov_list')

for index,actor in enumerate(actors):
    print("배우 이름: ",re.sub("\(\w+\)", "",str(actor.get_text()))) #<a href="/db/person/info/?person_id=30235">진경(1편)</a>
    print("흥행 지수: ",int(hits[index].get_text().replace(',',''))) #<strong>116,657</strong>   #116657
    movie_titles=movies[index].select('li a span') # 한 배우당 필모들이 하나의 리스트로 되어 있으므로 한 배우당 for문으로 영화들을 뽑아내야함
    movie_title_list=list()
    for movie_title in movie_titles:
        movie_title_list.append(movie_title.get_text()) #필모들을 리스트로 만들기
    print("출연영화: ",movie_title_list)    

"""

##7. 지금까지의 데이터들 총 통합/위의 코드들 총 통합해서 하나의 코드로 만들기. (하나의 자료형으로 만들기)   
actor_info_list=list()
actors=soup.select('div.name > a') #리스트로 반환됨, 제일 위에서 정의된 것임
hits=soup.select('ul.num_info > li > strong')
movies=soup.select('ul.mov_list')

for index,actor in enumerate(actors):
    actor_name=re.sub("\(\w+\)", "",str(actor.get_text())) #<a href="/db/person/info/?person_id=30235">진경(1편)</a>
    actor_hits=int(hits[index].get_text().replace(',','')) #<strong>116,657</strong>   #116657
    movie_titles=movies[index].select('li a span') # 한 배우당 필모들이 하나의 리스트로 되어 있으므로 한 배우당 for문으로 영화들을 뽑아내야함
    movie_title_list=list()

    for movie_title in movie_titles:
                movie_title_list.append(movie_title.get_text()) #필모들을 리스트로 만들기
        
    actor_info_dict=dict()
    actor_info_dict['배우이름']=actor_name
    actor_info_dict['흥행지수']=actor_hits
    actor_info_dict['출연영화']=movie_title_list

    actor_link="http://www.cine21.com"+actor["href"] #이제 이 주소로 다시 크롤링
    res_actor=requests.get(actor_link)#이번에는 get형식임
    soup_actor=BeautifulSoup(res_actor.content,'html.parser')
    default_info=soup_actor.select_one('ul.default_info')
    actor_details=default_info.select('li')#<ul class="default_info"> 이거는 안 봐도 되니까
    

    for actor_item in actor_details:
        actor_item_field=actor_item.select_one('span.tit').get_text()
        actor_item_value=re.sub('<span.*?>.*?</span>', '', str(actor_item)) #반드시 string으로 re를 해줘야 함!
        actor_item_value=re.sub('<.+?>', '', actor_item_value) 
        actor_info_dict[actor_item_field]=actor_item_value
    actor_info_list.append(actor_info_dict)

    




