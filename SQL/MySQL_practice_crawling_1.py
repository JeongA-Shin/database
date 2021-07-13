# 실제 활용해보는 MySQL 문법
## 1.Schema 설계(정의)
### - TABLE 분리(검색과 저장의 효율성): primary key, foreign key의 활용

'''
#각 카테고리 별 랭킹을 보여주는 table
CREATE TABLE ranking(
    num INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    ... 필드 내용은 아래 참고
    item_code VARCHAR(20) NOT NULL,
    FOREIGN KEY (item_code) REFERENCES items(item_code)
)DEFAULT CHARSET=utf8 COLLATE=utf8_bin;   ### 혹시나 한글 처리 시 에러를 방지하기 위해 utf8 추가

#랭킹을 보여주는 테이블에 각 아이템들이 데이터로 들어가 있는데
# 이 데이터들은 items라는 테이블의 아이템임
# 즉! ranking table의 데이터들은 items라는 테이블의 데이터를 참조하고 있는 거임
#(ex) best 상품(ranking)에서 해당 ranking의 아이템을 클릭하면 그 상품 페이지로 넘어감, 그리고 그 아이템은 items라는 db안에 속해있음

CREATE TABLE items(
    item_code VARCHAR(20) NOT NULL PRIMARY KEY,
    ... 필드 내용은 아래 내용 참고
)DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
'''

'''import pymysql
db=pymysql.connect(host='localhost',port=3306,user='root',passwd='anjfgkfksmsakfdldi0613!',db='bestproducts',charset='utf8')
cursor=db.cursor()

###foreign key를 쓰고 있는 테이블은 이미 그 전의 테이블이 존재해야 한다. 따라서 table items를 먼저 만들어준다.
sql="""
CREATE TABLE items(
    item_code VARCHAR(20) NOT NULL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    ori_price INT NOT NULL,
    dis_price INT NOT NULL,
    discount_percent INT NOT NULL,
    provider VARCHAR(100)
)DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
"""

cursor.execute(sql)

sql="""
CREATE TABLE ranking(
    num INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    main_category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL,
    item_ranking TINYINT UNSIGNED,
    item_code VARCHAR(20) NOT NULL,
    FOREIGN KEY (item_code) REFERENCES items(item_code)
)DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
"""

cursor.execute(sql)

## 제일 마지막에 꼭 commit(), close()해주기
db.commit()
db.close()'''

#2. 크롤링
import requests
from bs4 import BeautifulSoup

## 메인 카테고리들의 이름 얻어오기
res=requests.get("http://corners.gmarket.co.kr/Bestsellers")
soup=BeautifulSoup(res.content,'html.parser')

categories=soup.select('#categoryTabG > li > a')

for category in categories:
    print("http://corners.gmarket.co.kr"+category['href'],category.get_text())  #내가 보고 싶은 태그의 "속성"(딕셔너리처럼 표현)

