# -*- coding:utf-8 -*-

import os
import cx_Oracle
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib
from bs4 import BeautifulSoup


# oracle의 쿼리 결과를 Dict로 받기위한 메서드
def makeDictFactory(cursor):
    columnNames = [d[0] for d in cursor.description]
    def createRow(*args):
        return dict(zip(columnNames, args))
    return createRow



class inputNo() :
    os.environ["NLS_LANG"] = ".AL32UTF8" # UTF-8 : .AL32UTF8, CP949 : .KO16MSWIN949
    conn = cx_Oracle.connect('bigdata/admin1234@localhost:1521/xe') # oracle 서버와 연결 (connection 맺기)
    
    def input(self):
    
        serviceKey = "Qdb5KydABzjhFWA4CzQ4gSgtLMnxo6C5jGrv%2FOLaQ6evALcjMQDkPllXowGQzr9DzraCGymtgDwuQmge6QJzng%3D%3D"

        print(self.conn.version) # connection 확인
        oracle = self.conn.cursor() # cursor 객체 얻어오기
         
        # 1. oracle의 bill 테이블에서 proposer_kind가 '의원'인 데이터에서
        #    '의원'앞의 문자열을 kor_name으로 가져온다.
        sql_select = """
        select 
        proposer, 
        substr(proposer, 0, instr(proposer, '의원')-1) as "kor_name" 
        from bill 
        where proposer_kind = '의원'
        and substr(proposer, 0, instr(proposer, '의원')-1) is not null
        """
        
        oracle.execute(sql_select)
        oracle.rowfactory = makeDictFactory(oracle) # cursor의 rowfactory 메서드를 오버라이딩하여 리턴받는 데이터의 형태를 바꿀 수 있음
        items = oracle.fetchall() 
        
        for item in items:
            print(item, "\t", item['kor_name'])
            
            if item['kor_name'] != '김성태 ' or item['kor_name'] != '최경환':
            
                # 2. oracle의 politician 테이블에서 위에서 받은 kor_name을 검색한다.
                sql_find = """
                select
                politician_no as "pno", 
                politician_kor_name as "kor_name",
                politician_hj_name as "hj_name"
                from politician
                where
                politician_kor_name = :kor_name
                """
                
                oracle.execute(sql_find,
                               kor_name = item['kor_name'])
                oracle.rowfactory = makeDictFactory(oracle)
                results = oracle.fetchall()
                
                for result in results:
                    print("\t>>>\t", result)
                    
                    # 3. oracle의 bill 테이블에서 해당 로우에 pno, kor_name, hj_name을 업데이트
                    sql_update = """
                    update bill
                    set
                    politician_no = :politician_no,
                    proposer = :proposer,
                    proposer_hj=  :proposer_hj
                    where
                    substr(proposer, 0, instr(proposer, '의원')-1) = :politician_kor_name
                    """
                    
                    oracle.execute(sql_update,
                                   politician_no = result['pno'],
                                   proposer = result['kor_name'],
                                   proposer_hj = result['hj_name'],
                                   politician_kor_name = result['kor_name']
                                   )
            else:
                print("김성태, 최경환")
                                
        print("완료~~")   
        self.conn.commit()
        
if __name__ == '__main__':
    obj = inputNo()
    obj.input()
    
