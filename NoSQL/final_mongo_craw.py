#1.라이브러리 import
from bs4 import BeautifulSoup
import requests
import pymongo
import re #정규표현식을 위한 라이브러리

#2. mongodb 연결,db,collection 생성/선택
connection=pymongo.MongoClient()#mongoDB에 연결
actor_db=connection.cine21 #database만들기
actor_collection=actor_db.actor_collection # collection만들기


actor_info_list=list() #혹시 페이지 바뀌어서 나중에 초기화되면 날아가니까 미리 선언해놓음

#3.크롤링 주소 request
cine21_url='http://www.cine21.com/rank/person/content'
#form data를 딕셔너리로 만들자
post_data=dict()
post_data["section"]='actor'
post_data["period_start"]='2021-6'
post_data["gender"]='all'

for index in range(1,21):
    post_data["page"]=index


    #post방식의 데이터 크롤링
    res=requests.post(cine21_url,data=post_data)

    #4. 데이터 파싱,추출
    #여기서부터는 전과 같이 css selector등을 활용해서 추출
    soup=BeautifulSoup(res.content,'html.parser')

    actors=soup.select('div.name > a') #리스트로 반환됨, 제일 위에서 정의된 것임
    hits=soup.select('ul.num_info > li > strong')
    movies=soup.select('ul.mov_list')
    rankings=soup.select('li.people_li span.grade')


    for index,actor in enumerate(actors):
        actor_name=re.sub("\(\w+\)", "",str(actor.get_text())) #<a href="/db/person/info/?person_id=30235">진경(1편)</a>
        actor_hits=int(hits[index].get_text().replace(',','')) #<strong>116,657</strong>   #116657
        movie_titles=movies[index].select('li a span') # 한 배우당 필모들이 하나의 리스트로 되어 있으므로 한 배우당 for문으로 영화들을 뽑아내야함
        movie_title_list=list()

        for movie_title in movie_titles:
                    my_movie_title=re.sub("\.*n","",str(movie_title.get_text()))
                    movie_title_list.append(my_movie_title)
            
        actor_info_dict=dict()
        actor_info_dict['배우이름']=actor_name
        actor_info_dict['흥행지수']=actor_hits
        actor_info_dict['출연영화']=movie_title_list
        actor_info_dict['랭킹']=rankings[index].text


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



#for myactor in actor_info_list:
        #print(myactor)

#9. 크롤링한 데이터 mongoDB에 저장
actor_collection.insert_many(actor_info_list)
#참고: document들 모두 삭제
#actor_collection.delete_many({})

