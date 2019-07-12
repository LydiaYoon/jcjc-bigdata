# -*- coding:utf-8 -*-
import os
import pymongo

from collections import Counter

from konlpy.corpus import kolaw
from konlpy.tag import Komoran
from konlpy.tag import Hannanum
from konlpy.utils import concordance, pprint


class konlpy():
    os.environ["NLS_LANG"] = ".AL32UTF8" # UTF-8 : .AL32UTF8, CP949 : .KO16MSWIN949
    con = pymongo.MongoClient("localhost", 27017)['jcjc']
#     conn = cx_Oracle.connect('bigdata/admin1234@localhost:1521/xe') # oracle 서버와 연결 (connection 맺기)
    
    # userdic : 단어 추출에서 제외할 목록들이 들어갈 단어사전
    komoran = Komoran(userdic='C:\\Project\\morphemeAnalysis\\com\\test\\user_dic.txt')
    hannanum = Hannanum()
    
    def analyze(self):
        count = 0
        for item in self.con['bill'].find({"$or": [{"proposer":"이동섭"}, {"proposer":"유승민"}] }):#, {"analysisCheck":"0"}): 
            count += 1
            billid = item.get('bill_id')
            billname = item.get('bill_name')
            summary = item.get('summary') 
            
            # komoran은 빈줄이 있으면 에러가 남
            summary = summary.replace("\r", "").replace("\n", " ").replace("\t", " ")
            summary = summary.replace("？", "ㆍ").replace(",", "")
            
            print(count, "번째")
            print(billname)
            print(summary)
            # print(item.get('summary').replace("\n", " ").replace("？", "ㆍ"))
            
            # 명사 추출
            nouns = self.komoran.nouns(summary)
            print("len(nouns) :", len(nouns))

            cnt = Counter(nouns)
            result_list = cnt.most_common(len(nouns))
            print("len(result_list) :", len(result_list))
            
            # List 객체인 결과를 Dict로 변경
            result_dict = {} # Dict 객체 생성
            for i in range( len(result_list) ):
                key = result_list[i][0] # 단어
                value = result_list[i][1] # count
                result_dict[key] = value 
            
#             pprint(result_dict)
            
            row = {} # Dict 객체 생성
            row['bill_no'] = item.get('bill_no')
            row['politician_no'] = item.get('politician_no')
            row['words'] = result_dict
            
            pprint(row)
            
            self.con['billAnalysis'].insert_one(row)
            print("==========================================================")
        
        
        print("요시! 입력 완료!")    

if __name__ == '__main__':
    obj = konlpy()
    obj.analyze()