import pymysql
import pandas as pd#데이터 분석할 때 사용- 많은 기능들 중 db다루는 부분을 봄
#pandas를 import함으로써 .cursor()을 쓰지 않음 -> 앞에서 배웠던 CRUD 파트와 좀 다르게 진행됨
#이게 더 편한 듯


host_name='localhost'
host_port=3306
username='root'
password='anjfgkfksmsakfdldi0613!'
database_name='student_mgmt'


#일단 사용할 데이터베이스에 connect 메소드로 접속
db = pymysql.connect(
    host=host_name, 
    port=host_port, 
    user=username, 
    passwd=password, 
    db=database_name, 
    charset='utf8')


#1)pandas.read_sql(쿼리(sql구문), 연결된 db(객체)-cursor가 아님!)---->db에 나의 쿼리를 전달하고 실행!(excute와 fecth..()함수+for문을 합친 것)
SQL="select * from students"
df=pd.read_sql(SQL,db)#read_sql: 테이블 읽어오는 함수  #df변수에 query의 결괏값이 담겨짐
print(df)  #그냥 pymysql만 import하면, fetchall()등을 이용하고 for문등을 해야 보기가 쉬워지지만, pandas의 read_sql()을 사용함으로써 쉬워짐


#2)to_csv()
#to_csv()메서드로 query의  결과를 파일로 저장하기
#객체.to_csv('저장하고 싶은 파일명',sep='구분자로 설정할 기호-그냥 공백으로도 가능',encoding='utf8') 
# index='false' -->내가 준 id값 외에도 pandas 자체에서 각 row들에게 준 index값들이 있음. 그게 필요없으면 false로 설정
df.to_csv('students.csv',sep=',',index=False,encoding='utf8')