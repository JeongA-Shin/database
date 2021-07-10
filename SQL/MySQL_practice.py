'''
일반적인 mysql 핸들링 코드 순서

# 1. 라이브러리 가져오기
import pymysql

# 2. 접속하기
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='funcoding', db='ecommerce', charset='utf8')

# 3. 커서(부캐) 가져오기
cursor = db.cursor()

# 4. SQL 구문 만들기 (CRUD SQL 구문 등)
sql="show databases;" #문자열로 만들기!

# 5. SQL 구문 실행하기
cursor.execute(sql)

# 6. (본캐)DB에 Complete 하기
db.commit()

# 7. DB 연결 닫기
db.close()
'''




import pymysql  #python으로 mysql을 다룰 수 있는 라이브러리
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='anjfgkfksmsakfdldi0613!', db='ecommerce', charset='utf8')
#pymysql의 connect 메소드를 통해 내가 다루고 싶은 database에 접속(테이블 아님)
'''
pymysql.connect() 메소드를 사용하여 MySQL에 연결
호스트명, 포트, 로그인, 암호, 접속할 DB 등을 파라미터로 지정
주요 파라미터
host : 접속할 mysql server 주소
port : 접속할 mysql server 의 포트 번호
user : mysql ID
passwd : mysql ID의 암호
db : 접속할 데이터베이스
charset='utf8' : mysql에서 select하여 데이타를 가져올 때 한글이 깨질 수 있으므로 연결 설정에 넣어줌!!
'''
#print(db)를 통해 현재 접속이 되었는지 확인. 정상적으로 접속이 되었으면

#접속된 객체에다가 ""명령을 내릴 수 있게"" .cursor()을 호출한다.
cursor=db.cursor() #MySQL 접속이 성공하면, Connection 객체(접속한 db)로부터 cursor() 메서드를 호출한다.(명령을 전달하기 위한 말 그대로 커서 역할)
                   

#테이블 생성하는 SQL명령어
sql="""
    CREATE TABLE product(
    PRODUCT_CODE VARCHAR(20) NOT NULL,
    TITLE VARCHAR(20) NOT NULL,
    ORI_PRICE INT,
    DISCOUNT_PRICE INT,
    DISCOUNT_PERCENT INT,
    DELIVERY VARCHAR(2),
    PRIMARY KEY(PRODUCT_CODE)
    );
"""

#일단 부캐에서 sql구문을 실행
#해당 커서( 접속한 db를 가르킴)하고 싶은 sql 명령어 실행
cursor.execute(sql) #Cursor 객체(여기서는 변수 cursor에 담겨있음)의 execute() 메서드를 사용하여 """SQL 문장을 DB 서버에 전송"""""
                    #예) cursor.excute("show databases")




db.commit() # 지금까지는 db를 가르키는 "커서"만 가지고 작업한 거임.(중간에 삭제 등 명령어를 잘못했을 때, 그래도 이전의 상태로 돌아갈 수 있도록)
            # 작업내용을 실제 db 자체에, 실행 mysql 서버에 최종 확정해서 반영해야함 (삭제 등 중요한 것도 이제 되돌릴 수 없음)

db.close()  #지금까지 작업한 db와의 연결/접속을 끊음
