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
import pymysql


def save_data(item_info): #item_info는 딕셔너리 형태로 저장된 item 정보
    ## items 데이터베이스에 아이템이 중복되어 insert되면 안 됨. 해당 아이템이 이미 items데이터베이스에 있으면 넣으면 안 됨
    ''' COUNT SQL(위의 문제에 대한 솔루션)
    - COUNT: 검색 결과의 row 수를 가져올 수 있는 SQL 문법
    - SQL 예제: SELECT COUNT(*) FROM items ---->전체 row의 수가 몇 개인지 나옴'''


    sql = """SELECT COUNT(*) FROM items WHERE item_code = '""" + item_info['item_code'] + """';"""
    #해당 item code의 아이템이 이미 items 데이터베이스에 insert되어 있는지 count를 통해 확인
    cursor.execute(sql) # count 실행
    result = cursor.fetchone() #어차피 결과는 숫자 하나만 있으므로 그냥 fetchone()을 해준다
    if result[0] == 0: #어차피 결과는 숫자 하나, 즉 단 한 줄이므로 그냥 0번째 인덱스면 됨 #0이면 없음, 1이면 이미 있음
        ###데이터베이스에 넣기 위한 INSERT구문
        sql = """INSERT INTO items VALUES('""" + item_info['item_code'] + """',
        '""" + item_info['title'] + """', 
        """ + str(item_info['ori_price']) + """,  #숫자가 value가 될 수도 있으므로 혹시나 무조건 str을 해준다
        """ + str(item_info['dis_price']) + """, 
        """ + str(item_info['discount_percent']) + """, 
        '""" + item_info['provider'] + """')"""
        cursor.execute(sql)

    sql = """INSERT INTO ranking (main_category, sub_category, item_ranking, item_code) VALUES('""" + item_info[
        'category_name'] + """',
    '""" + item_info['sub_category_name'] + """', 
    '""" + str(item_info['ranking']) + """', 
    '""" + item_info['item_code'] + """')"""
    cursor.execute(sql)



#각 페이지마다(메인카테고리, 서브 카테고리들)의 상품 목록을 뽑아내는 함수
def get_items(html, category_name, sub_category_name):#html은 이미 파싱된 것을 의미
    best_item = html.select('div.best-list') #select()는 리스트, 즉 여러 요소들을 포함
    for index, item in enumerate(best_item[1].select('li')): 
        data_dict = dict()

        ranking = index + 1
        title = item.select_one('a.itemname')
        ori_price = item.select_one('div.o-price')
        dis_price = item.select_one('div.s-price strong span')
        discount_percent = item.select_one('div.s-price em')

        '''해당되는 태그가 없는데(None인데) .get_text()를 해버리면 에러남 (ex) 할인율이 없는 경우
        따라서 item.select_one('div.o-price span').get_text() 이렇게 해버리면 너무 위험부담이 크므로 
        none인 경우를 따로 처리해주고 get_text()호출'''


        if ori_price == None or ori_price.get_text() == '':
            ori_price = dis_price

        if dis_price == None:
            ori_price, dis_price = 0, 0
        else:
            ori_price = ori_price.get_text().replace(',', '').replace('원', '')
            dis_price = dis_price.get_text().replace(',', '').replace('원', '')

        if discount_percent == None or discount_percent.get_text() == '':
            discount_percent = 0
        else:
            discount_percent = discount_percent.get_text().replace('%', '')

        #아이템 판매처 정보 - 다시 하나의 아이템에 연결된 링크 페이지에서 다시 크롤링 시작
        #일단 링크 페이지 얻기    
        product_link = item.select_one('div.thumb > a')
        item_code = product_link.attrs['href'].split('=')[1]
        #해당 아이템 링크 페이지에서 크롤링 시작
        res = requests.get(product_link.attrs['href'])
        soup = BeautifulSoup(res.content, 'html.parser')
        
        provider = soup.select_one('div.item-topinfo_headline > p > span.text_brand > span.text')

        if provider == None:
            provider = ''
        else:
            provider = provider.get_text()

        data_dict['category_name'] = category_name
        data_dict['sub_category_name'] = sub_category_name
        data_dict['ranking'] = ranking
        data_dict['title'] = title.get_text()
        data_dict['ori_price'] = ori_price
        data_dict['dis_price'] = dis_price
        data_dict['discount_percent'] = discount_percent
        data_dict['item_code'] = item_code
        data_dict['provider'] = provider

        save_data(data_dict) #각 아이템들을 저장한 딕셔너리를 save_data에 파라미터로 넘김
        # print (category_name, sub_category_name, ranking, item_code, provider, title.get_text(), ori_price, dis_price, discount_percent)



### 각 메인 카테고리의 페이지에 표시 되어있는 subcategory들 뽑아내는 함수
def get_category(category_link, category_name):
    print(category_link, category_name)
    res = requests.get(category_link)
    soup = BeautifulSoup(res.content, 'html.parser')

    get_items(soup, category_name, "ALL")

    sub_categories = soup.select('div.navi.group ul li > a')#서브 카테고리들끼리 selector가 일치하지 않으므로 그냥 바로 하위 태그 관계로 표현
    for sub_category in sub_categories:
        res = requests.get('http://corners.gmarket.co.kr/' + sub_category['href'])## 다시 서브 카테고리의 페이지에서 크롤링함
        soup = BeautifulSoup(res.content, 'html.parser')
        print(category_name, sub_category.get_text())
        get_items(soup, category_name, sub_category.get_text())



#main함수

db = pymysql.connect(host='localhost', port=3306, user='root', passwd='funcoding', db='bestproducts', charset='utf8')
cursor = db.cursor()

res = requests.get('http://corners.gmarket.co.kr/Bestsellers')
soup = BeautifulSoup(res.content, 'html.parser')

categories = soup.select('div.gbest-cate ul.by-group li a')
for category in categories:
    get_category('http://corners.gmarket.co.kr/' + category['href'], category.get_text()) #내가 보고 싶은 태그의 ['속성'](딕셔너리처럼 표현)

db.commit()
db.close()


