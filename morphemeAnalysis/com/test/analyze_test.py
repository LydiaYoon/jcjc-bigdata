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
        
#         summary = """
#                 게임물을 이용함에 따라 획득할 수 있는 게임 내 점수, 등급, 성과 등은 게임물의 이용자가 직접 또는 정상적으로 게임물을 이용함에 따라 획득할 수 있도록 하는 것이 원칙임. 특히 여러 게임 이용자들이 함께 이용하는 온라인 게임 환경에서는 게임 이용자가 게임 내에서 획득한 결과물이 다른 게임 이용자와의 관계에 영향을 끼칠 수 있음.
#                 그러나 최근 게임물의 이용자가 직접 또는 정상적으로 게임을 하지 아니하고, 제3자에게 자신의 개인정보와 계정정보를 공유하는 방법을 통해 부적절한 게임 결과물을 획득하고 있는 사례가 급증함. 또한 이와 같이 게임 내 결과물 획득 행위를 불법적으로 제공, 알선하여 그 대가로 금전 등을 취득하는 영리행위를 하는 자들 역시 증가하고 있음. 
#                 이러한 불법행위는 게임 내 공정한 경쟁을 해침으로써 게임물을 이용하는 이용자들에게 피해를 입히고 있으며, 게임물 관련사업자에게도 직·간접적 피해를 주고 있는 상황임. 아울러 이러한 영리행위를 목적으로 타인의 개인정보를 무분별하게 도용하거나 결제사기가 발생하는 등, 사회적으로도 심각한 물의를 빚는 결과도 발생하고 있음.
#                 이와 같이 게임물의 유통질서를 저해하는 행위를 처벌할 수 있도록 하여 건전한 게임문화를 조성하고 게임물 이용자와 관련사업자를 보호하고자 함. 
#                 가. 영리를 목적으로 하여 게임물 관련사업자가 제공 또는 승인하지 아니한 방법으로 게임물 이용자가 점수·성과 등을 획득하게 하여 게임물의 정상적인 운영을 방해하거나 이를 알선하는 행위를 금지함(안 제32조제1항제11호 신설).
#                 나. 제32조제1항제11호의 규정을 위반하여 영리를 목적으로 하여 게임물 관련사업자가 제공 또는 승인하지 아니한 방법으로 게임물 이용자가 점수·성과 등을 획득하게 하여 게임물의 정상적인 운영을 방해하거나 이를 알선한 자를 2년 이하의 징역 또는 2천만원 이하의 벌금에 처함(안 제45조제5호의2 신설).
#         """

#         summary = """
#               프로그래밍화된 데이터를 기반으로 만들어진 게임의 특성상 게임서비스 제공 중 오류 등으로 인한 게임 장애가 발생하여 이용자가 피해를 입는 사례가 다수 있음.  
#               그러나 게임이용자들이 이에 대해 의견 개진이나 불만을 제기하더라도 게임사에서는 이용자들에게 합당한 대응과 만족할만한 대처를 하지 않는 경우가 지속해서 발생하고 있음. 
#               이에 게임물 관련사업자는 게임 오류로 인해 게임물 이용자로부터 제기되는 정당한 불만을 즉시 처리하도록 하고, 즉시 처리하기 곤란한 경우에는 게임물 이용자에게 그 사유와 처리일정을 알리도록 하여 게임이용자의 권익을 보호하고자 함(안 제14조제2항 신설).
#         """
        
#         summary = """
#               현행법은 게임물을 유통시키거나 이용을 제공하기 위해서는 등급분류를 받아야 하며, 등급분류를 받지 아니한 게임물을 유통 또는 이용에 제공한 경우 처벌을 받게 됨.
#               그러나 비영리 목적으로 제작·배급하는 게임물까지 등급분류를 받도록 강제하는 것은 자유로운 창작 활동을 제한할 뿐만 아니라 게임 개발자들의 개발 의욕을 꺾는 것임.
#               이에 비영리 목적으로 제작·배급하는 게임물에 대하여 등급분류를 면제하는 한편, 대통령령으로 정하는 기준에 해당하는 자가 등급분류를 신청할 경우 수수료를 면제하도록 하여 우리나라 게임 개발 생태계를 보존하는 한편, 창작 욕구를 고취시키고자 하는 것임(안 제21조제1항제4호, 제41조제2항 및 제3항 단서 신설).
#         """
        
        summary = """
                게임산업은 한국 콘텐츠 수출 전체의 56%를 차지하며 수출액이 약 3조 6천억원에 달하는 등, K-POP이나 한류 드라마 등 여타 콘텐츠에 비해 국가 경쟁력 제고에 기여하는 비중이 훨씬 큰 산업분야임.
                그러나 정작 관련 정책을 결정하게 될 공적 기관의 고위직에 게임산업과 무관한 인사들이 임명되어 실제 산업 현장과 괴리된 정책으로 게임산업 발전의 발목을 잡아오고 있는 실정임.
                이에 게임 관련 공공기관에서의 게임산업 정책 의사결정 과정에 게임산업 전문가가 보다 더 충원될 수 있게 할 필요가 있으며, 특히 게임물관리위원회 사무국의 실무를 총괄하는 사무국장을 공개모집 절차를 통해 임명하도록 함으로써 이를 도모하고자 함(안 제18조제2항).
        """
        
        print(type(summary))
        # komoran은 빈줄이 있으면 에러가 남
        
        if type(summary) is not NoneType:
            summary = summary.replace("\r", "").replace("\n", " ").replace("\t", " ")
            summary = summary.replace("？", "ㆍ").replace(",", "")
#             summary = summary.replace("등", "").replace("수", "").replace("것", "").replace("점", "")
        
        
            # 명사 추출
            nouns = self.komoran.nouns(summary)
            print("len(nouns) :", len(nouns))

            cnt = Counter(nouns)
            result_list = cnt.most_common(len(nouns))
            print("len(result_list) :", len(result_list))
            
        # print(item.get('summary').replace("\n", " ").replace("？", "ㆍ"))

        # List 객체인 결과를 Dict로 변경
        result_dict = {} # Dict 객체 생성
        for i in range( len(result_list) ):
            key = result_list[i][0] # 단어
            value = result_list[i][1] # count
            result_dict[key] = value 
        
#             pprint(result_dict)
        
        
        del_str = ['등', '수', '것', '물', '점', '조', '제', '호', '년', '말', '밖', '자', '바', '중', '때문', '한편', '뿐', '임', '항']
        
        for str in del_str:
            if result_dict.get(str) is not None:
                del result_dict[str]
        
        sortDict = sorted(result_dict.items(), key=operator.itemgetter(1), reverse=True)
        pprint(sortDict)
        
        print("==========================================================")
    
        

if __name__ == '__main__':
    obj = konlpy()
    obj.analyze()