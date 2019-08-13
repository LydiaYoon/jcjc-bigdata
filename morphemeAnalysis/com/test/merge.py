# -*- coding:utf-8 -*-
import os
import pymongo
import pandas as pd
import csv

def convert(x):
    try:
        return x.astype(int)
    except:
        return x
        

class merge():
    os.environ["NLS_LANG"] = ".AL32UTF8" # UTF-8 : .AL32UTF8, CP949 : .KO16MSWIN949
    con = pymongo.MongoClient("localhost", 27017)['jcjc'] 
    
    
    def merge(self):
        
        # 1. csv 파일로 출력할 DataFrame 객체를 생성한다.
        result = {}
#         res_df = pd.DataFrame(columns=['words'])
#         print(res_df)
        print("===================================================")
        
        # 2. mongoDB의 billAnalysis 컬렉션을 조회한다.
        for item in self.con['billAnalysis'].find():
            
            bill_no = item.get('bill_no')
            politician_no = item.get('politician_no')
            words = item.get('words')
            
            if result.get(politician_no) is None:
                result[politician_no] = pd.DataFrame(columns=['words'])
            
#             print(bill_no, "\t", politician_no, "\t", words)
            
            keys = list(words.keys()) # 단어
            values = list(words.values()) # 단어 수
            
            # 3. DataFrame 타입의 임시변수에 현재 의안의 정보를 저장한다.
            temp_df = pd.DataFrame( data={'words':keys, bill_no:values} )
            print("DataFrame\t", temp_df.columns)
            
            # 4. 결과 변수에 임시 변수의 정보를 merge한다.
            #    단어 전체를 기록할 것이기 때문에 words 컬럼을 기준으로 outer join을 실행
            result[politician_no] = pd.merge(result[politician_no], temp_df, how='outer', on='words')
        
        
        print("===================================================")
        
        
#         print(result)
        
        for politician_no in result.keys(): # 결과 변수에서 정치인 번호 추출
            
            df = result[politician_no]
            columns = list(df.columns) # df에서 컬럼명 추출
            len = df.shape[0] # df에서 로우 길이 추출
            df = df.fillna(0) # NaN 값을 0으로 채움
            print(df)
#             print(politician_no, "\t", len, "\t", columns)
            
            
            # 5. 결과 변수를 csv로 저장한다.
            filename = politician_no + '.csv'
            with open(filename, 'w', encoding='utf-8', newline='\n') as file:
                writer = csv.DictWriter(file, fieldnames=columns)
                writer.writeheader()
                
                df.to_csv(filename, sep=',', na_rep='0', index=False)

#                 for i in range(len):
#                     print("csv write\t", politician_no, "\t", i, "\t", dict(df.iloc[i]))
#                     writer.writerow(dict(df.iloc[i]))
            
#         result_columns = list(result.columns) # 결과 변수에서 컬럼명 추출
#         result_len = result.shape[0]
#         
#         
#         # 5. 결과 변수를 csv로 저장한다.
#         filename = 'result.csv'
#         with open(filename, 'w', encoding='utf-8', newline='\n') as file:
#             writer = csv.DictWriter(file, fieldnames=result_columns)
#             writer.writeheader()
#              
#             for i in range(result_len):
# #                 print("csv write\t", i, "\t", dict(result.iloc[i]))
#                 writer.writerow(dict(res_df.iloc[i]))

        
        print("입 력 완 료 데 스")
        
        
        
if __name__ == '__main__':
    obj = merge()
    obj.merge()