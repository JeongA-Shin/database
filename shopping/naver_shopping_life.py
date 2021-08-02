import requests
from bs4 import BeautifulSoup
import pymysql
import re


'''
CREATE TABLE life(
    ranking INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    id BIGINT NOT NULL,
    image BLOB, 
    title VARCHAR(100),
    price INT,
    review INT
)DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

'''

db = pymysql.connect(host='localhost', port=3306, user='root', passwd='anjfgkfksmsakfdldi0613!', db='naver_shopping', charset='utf8')
#print(db) 연결확인

cursor = db.cursor()

res = requests.get('https://search.shopping.naver.com/best100v2/detail.nhn?catId=50000008&listType=B10002')
soup = BeautifulSoup(res.content, 'html.parser')


item_info_list=list()

items = soup.select('ul.type_normal li')
for index,item in enumerate(items):
    item_info_dict=dict()
    ranking=index+1
    item_info_dict['ranking']=ranking
    item_info_dict['id']=int(item['data-nv-mid'])
    item_info_dict['image']=1 #아직 모름
    item_info_dict['title']=item.select_one('p.cont a').get_text()
    item_price=item.select_one('div.price strong span.num').get_text().replace(',','')
    item_info_dict['price']=int(item_price)
    review_num=item.select_one('div.info span.mall a.txt em').get_text().replace(',','')
    review_num=re.sub('\W','',str(review_num))
    item_info_dict['review']=int(review_num)
    item_info_list.append(item_info_dict)


#print(item_info_list)

for item_info in item_info_list:
    print(item_info)
    sql = """INSERT INTO life(ranking, id, image, title, price, review) VALUES(
        '""" + str(item_info['ranking']) + """',
        '""" + str(item_info['id']) + """',
        '""" + pymysql.NULL + """',
        '""" + item_info['title'] + """',
        '""" + str(item_info['price']) + """',
        '""" + str(item_info['review']) + """')"""
    cursor.execute(sql)

db.commit()
db.close()

