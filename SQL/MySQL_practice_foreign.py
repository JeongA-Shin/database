'''
## userbuy.sql 파일 참고

CREATE TABLE buyTbl (
    num INT AUTO_INCREMENT NOT NULL PRIMARY KEY, #이렇게 요소들에 PRIMARY KEY라고 해줘도 됨
    userID CHAR(8) NOT NULL,
    prodName CHAR(4),
    groupName CHAR(4),
    price  INT NOT NULL,
    amount  SMALLINT NOT NULL,
    FOREIGN KEY (userID) REFERENCES userTbl(userID) #foreign key 설정
####FOREIGN KEY (외부키가 될 필드명) REFERENCES [관계 있는 다른 테이블](연관된 다른 테이블의 필드명)
) DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

----주의할 점(problem)
지금 현재 buytbl이 usertbl의 데이터를 참조하고 있는 거임 그래서
(buyTbl 테이블의 userID 커럼은 userTbl 테이블의 userID를 참조하므로)
!!!!!!!!!!!!1 userTbl 테이블에 userID가 STJ인 데이터가 없으면, 입력이 안됨\n",!!!!!!!!!!11
"  - 데이터 무결성 (두 테이블간 관계에 있어서, 데이터의 정확성을 보장하는 제약 조건을 넣는 것임)\n",

반대로도 똑같이 buytbl이 참조하고 있는 usertbl의 데이터를 삭제하면 에러남!
buytbl에서 삭제하고, 마지막으로 usertbl에서 삭제할 수 있음
'''

import pymysql
import pandas as pd

host_name='localhost'
host_port=3306
username='root'
password='anjfgkfksmsakfdldi0613!'
database_name='sqldb'

db=pymysql.connect(
    host=host_name,
    port=host_port,
    user=username,
    passwd=password,
    db=database_name,
    charset='utf8')

""" 저번 시간 복습하기 (pymysql, pandas로 sql구문 다루기)
#pandas로 sql 구문 실행하기
#sql="select * from usertbl"
#df=pd.read_sql(sql,db)
#print(df)

#pymysql로 sql구문 실행하기 
# - Print로 결과 확인하려면 반드시 select* from~ 구문을 실행하고 해줘야 함
'''SQL_QUERY ="INSERT INTO buyTbl (userID, prodName, groupName, price, amount) VALUES('BBK', '운동화', '의류', 30, 2)"
cursor=db.cursor()
cursor.execute(SQL_QUERY)

SQL_TABLE="select * from buyTbl"
cursor.execute(SQL_TABLE)
result=cursor.fetchall()
for row in result:
    print(row)

db.commit()
db.close()'''
"""



#import위 주석 처리한 곳에서 주의할 점에 유의해서(foreign 키의 연결 사항을 지키면서) table에 입력하기
#foreign key 관계에서 나오듯이 usertbl에 해당 데이터가 먼저 있어야 buytbl에도 insert가 가능함
'''SQL_QUERY = "INSERT INTO usertbl VALUES('STJ', '서태지', 1975, '경기', '011', '00000000', 171, '2014-4-4')" #usertbl에 먼저 insert
cursor=db.cursor()
result=cursor.execute(SQL_QUERY)
db.commit()

SQL_QUERY2="select * from usertbl"
result2=pd.read_sql(SQL_QUERY2,db)
print(result2)'''

#usertbl에 먼저 데이터를 넣었으니까 이제 buytbl에 해당 데이터를 넣어도 오류나지 않음
SQL_QUERY3 = "INSERT INTO buyTbl (userID, prodName, groupName, price, amount) VALUES('STJ', '운동화', '의류', 30, 2)"
cursor=db.cursor()
result3=cursor.execute(SQL_QUERY3)
db.commit()
SQL_QUERY4="select * from buytbl"
result4=pd.read_sql(SQL_QUERY4,db)
print(result4)

db.close()