#!/usr/bin/env python
# coding: utf-8

import os

import pandas as pd

from .. import util

    
# 弹性分类：完整分类code由长到短匹配，有限匹配到的就是最低级分类
class Cata:
    def __init__(self, df):
        self.df = df
        
        self.check()
    
        # self.m = dict(zip(list(self.df['xxdm']), list(self.df['xxmc'])))
        self.m = self.gen_map()  # {code: info_dt}
        self.cata_codes = list(self.m.keys())
        self.max_code_len = max([len(i) for i in self.cata_codes])
    
    def check(self):
        # code列要保证唯一性
        assert len(self.df) == len(self.df['xxdm'].unique())
    
    def gen_map(self):
        m = dict()
        for i, row in self.df.iterrows():
            temp = dict()
            code = row['xxdm']
            temp['code'] = code
            temp['name'] = row['xxmc']
            temp['level'] = row['level']
            temp['link'] = row['link'] if not pd.isna(row['link']) else None
            m[code] = temp
        return m
    
    # 从完整code获取给定code
    def get_code(self, code):
        for i in range(self.max_code_len):
            seg = code[:self.max_code_len-i]
            if seg in self.cata_codes:
                find_dt = self.m[seg]
                if not find_dt['link']:
                    return seg
                else:
                    return find_dt['link']
        print('The given code is illegal.')
        return None
    
    # 从完整code获取name
    def get_name(self, code):
        k = self.get_code(code)
        if not k:
            return None
        find_dt = self.m[k]
        return find_dt['name']
    
    # 从完整code获取级别
    def get_grade(self, code):
        k = self.get_code(code)
        if k:
            find_dt = self.m[k]
            level = find_dt['level']
            return level
        else:
            return None
    

# 实例化
def init():
    base_path = os.path.abspath(__file__)
    direc = os.path.dirname(base_path)
    path1 = os.path.join(direc, 'ztfl1ji.xlsx')
    path2 = os.path.join(direc, 'ztfl2ji_full.xlsx')
    path3 = os.path.join(direc, 'ztfl3ji部分_full.xlsx')
    ztfl1ji = util.read_excel(path1)
    ztfl2ji = util.read_excel(path2)
    ztfl3ji = util.read_excel(path3)
    assert util.check_lst(ztfl1ji.columns.tolist(), ztfl2ji.columns.tolist())
    assert util.check_lst(ztfl2ji.columns.tolist(), ztfl3ji.columns.tolist())
    
    df = pd.concat([ztfl1ji, ztfl2ji, ztfl3ji])
    df = df.reset_index(drop=True)  # 必须要重置

    cataobj = Cata(df)
    return cataobj


# 初始化环境变量
cataobj = init()
