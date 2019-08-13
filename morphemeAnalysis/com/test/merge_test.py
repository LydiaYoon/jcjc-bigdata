# -*- coding:utf-8 -*-
import pandas as pd


class merge():
    
    def merge(self):
        
        df1 = pd.DataFrame()
        df2 = pd.DataFrame({'의안번호': {'a':1, 'b':3, 'c':5, 'd':7, 'e':9, 'f':11} })
        
        
#         print(df1)
#         print(df2)
        
        result = df1.append(df2)
        
        print(result)
        
        
        
if __name__ == '__main__':
    obj = merge()
    obj.merge()