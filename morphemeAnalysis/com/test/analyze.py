# -*- coding:utf-8 -*-
import os
import pymongo

from collections import Counter

from konlpy.corpus import kolaw
from konlpy.tag import Komoran
from konlpy.tag import Hannanum
from konlpy.utils import concordance, pprint
from hyperlink._url import NoneType

import operator

class konlpy():
    os.environ["NLS_LANG"] = ".AL32UTF8" # UTF-8 : .AL32UTF8, CP949 : .KO16MSWIN949
    con = pymongo.MongoClient("localhost", 27017)['jcjc']
#     conn = cx_Oracle.connect('bigdata/admin1234@localhost:1521/xe') # oracle 서버와 연결 (connection 맺기)
    
    # userdic : 단어 추출에서 제외할 목록들이 들어갈 단어사전
    komoran = Komoran(userdic='C:\\Project\\morphemeAnalysis\\com\\test\\user_dic.txt')
    hannanum = Hannanum()
    
    def analyze(self):
        count = 0
        for item in self.con['bill'].find({"$or": [{"proposer":"이동섭"}, {"proposer":"원유철"}] }):#, {"analysisCheck":"0"}): 
            count += 1
            billid = item.get('bill_id')
            billname = item.get('bill_name')
            summary = item.get('summary') 
            
            print(type(summary))
            # komoran은 빈줄이 있으면 에러가 남
            
            if type(summary) is not NoneType:
                summary = summary.replace("\r", "").replace("\n", " ").replace("\t", " ")
                summary = summary.replace("？", "ㆍ").replace(",", "")
            
            
                # 명사 추출
                nouns = self.komoran.nouns(summary)
                print("len(nouns) :", len(nouns))
    
                cnt = Counter(nouns)
                result_list = cnt.most_common(len(nouns))
                print("len(result_list) :", len(result_list))
                
            print(count, "번째")
            print(billname)
            print(summary)
            # print(item.get('summary').replace("\n", " ").replace("？", "ㆍ"))

            # List 객체인 결과를 Dict로 변경
            result_dict = {} # Dict 객체 생성
            for i in range( len(result_list) ):
                key = result_list[i][0] # 단어
                value = result_list[i][1] # count
                result_dict[key] = value 
            
#             pprint(result_dict)

            del_str = ['등', '수', '것', '물', '점', '조', '제', '호', '년', '말', '밖', '자', '바', '중', '때문', '한편', '뿐', '임', '항', '원', '간', '장', '때', '건', '형', '질', '날', '후', '탈', '시', '면', '성', '량', '곳', '일', '참', '액', '명', '감', '회', '사', '직', '법', '개', '봄', '상', '차', '검', '경', '김', '만', '식', '전', '한', '입', '주', '권', '청', '과', '주', '분', '대', '적', '급', '뒤', '업', '전', '지', '을', '데', '턱', '군', '인', '구', '위', '체', '균', '도', '직', '초', '차', '서', '세']
        
            for str in del_str:
                if result_dict.get(str) is not None:
                    del result_dict[str]
            
#             for key in result_dict.keys():
#                 if len(result_dict.get(key)) == 1:
#                     del result_dict[key]
            
            sortDict = sorted(result_dict.items(), key=operator.itemgetter(1), reverse=True)
            
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