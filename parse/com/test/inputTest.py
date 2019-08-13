# -*- coding:utf-8 -*-

import cx_Oracle
import os

# UTF-8 : .AL32UTF8
# CP949 : .KO16MSWIN949
os.environ["NLS_LANG"] = ".AL32UTF8"

# oracle 서버와 연결 (connection 맺기)
conn = cx_Oracle.connect('bigdata/admin1234@localhost:1521/xe')
print(conn.version) # connection 확인
db = conn.cursor() # cursor 객체 얻어오기
# insert
sql_insert = "insert into test values(:empno, :ename)"
db.execute(sql_insert, empno='003', ename='오승룡')
conn.commit()

# select
db.execute("SELECT * FROM test")
for i in db:
    print(i)

db.close() # cursor 객체 닫기
conn.close() # oracle 서버와 연결 끊기
    
"""
insert into politician
values(0, 0, '윤나래','尹나래','lydia yoon',
'1993-04-28', '무소속', 'ajax마스터', '엔코아',
'당선횟수', '당선대수', 
'010-6311-4096', 'https://github.com/LydiaYoon', 'narae456@gmail.com',
'400 Bad Request', '404 Not Found',
'https://pbs.twimg.com/media/DIAnF29VoAACic1.jpg');
"""

