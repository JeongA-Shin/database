import pymysql;

db = pymysql.connect(host='localhost', port=3306, user='root', passwd='anjfgkfksmsakfdldi0613!', db='ecommerce', charset='utf8')


cursor=db.cursor()

#현재 이미 product라는 테이블이 ecommerce라는 db안에 있는 상황임

#1. Insert -create에서 그냥 구문만 바뀐 거임
'''
for index in range(1,10):
    product_code = 215673140 + index 
    sql = """INSERT INTO product VALUES(
   '""" + str(product_code)+  """', '스위트바니 여름신상', 23000, 6900, 70, 'F'); """
    #print (sql)
    cursor.execute(sql)     #10번 실행됨(한 번 실행될 때마다 하나의 레코드(row)가 추가되는 거임),할 때마다 commit할 필요 없음. 
                            # commit은 코드 제일 마지막에 모든 작업이 끝나면 마지막으로 한 번만 해주면 됨
'''





#2. read(select* from...)
'''
데이터 조회(SELECT)
1.Cursor Object 가져오기: cursor = db.cursor()
2.SQL 실행하기: cursor.execute(SQL) --->여기까지는 동일
3.mysql 서버로부터 데이터 가져오기: fetch 메서드 사용
fetchall(): Fetch all the rows   ###모든 row를 가져옴  ---> 각 row들을 요소들로 가지는(각각의 요소들도 모두 튜플임) 하나의 큰? 튜플이 반환됨
                                                      ---> 예) ((1,2,3,4),(5,6,7,8))
fetchmany(size=None): Fetch several rows    ### 몇 개의 row만 가져옴
fetchone(): Fetch the next row     ###테이블에서 제일 위의 row만 가져옴


sql="""select * from product;"""

#결과를 바로 확인하려면 우선, <<<select구문을 실행하고나서>>>!!!! fecth~함수로 읽어와야함!
#일단 부캐에서 sql구문을 실행
cursor.execute(sql)
result=cursor.fetchmany(size=7)#result 안에 ^^^튜플로 반환된 결과^^^가 들어있는 거임

for row in result:
    print(row)
'''


#3. update(수정하기)
'''
sql=""" UPDATE product SET
    TITLE='뷔스티에 썸머 가디건',
    ORI_PRICE=33000,
    DISCOUNT_PRICE=9900,
    DISCOUNT_PERCENT=70
    WHERE PRODUCT_CODE='215673142';
"""

cursor.execute(sql)

sql="""select * from product;"""  ####결과를 print를 통해 바로 확인하려면 우선! select 구문을 먼저 실행해주고나서! fectch함수 등으로 뽑아낸다.
cursor.execute(sql)
result=cursor.fetchall()

for record in result:
    print(record)
'''

#4. delete (삭제하기)
sql="""DELETE FROM product WHERE PRODUCT_CODE='215673142';"""
cursor.execute(sql)

sql="SELECT * FROM product;"
cursor.execute(sql)

result=cursor.fetchall()
for record in result:
    print(record)


db.commit()#이제 본캐에도 실행된 정보들을 업데이트
db.close() #본캐(db)와의 연결도 끊음