import os
import collections
import random
import json
import csv

import pandas as pd
import dbfread


'''
汇集了常用的函数
'''


# 切换测试和运行状态
dev = True

def set_phase(phase):
    if phase not in ['dev', 'run']:
        raise ValueError('The project phase must be "dev" or "run" phase.')
    if phase == 'dev':
        dev = True
    else:
        dev = False
        

def read_text(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding) as f:
        t = f.read()
    return t


def save_text(path, text, encoding='utf-8'):
    with open(path, 'w', encoding=encoding) as f:
        f.write(text)


def read_excel(path):
    return pd.read_excel(path)


def save_excel(path, df):
    df.to_excel(path, encoding='utf-8-sig', index=False)


def read_dbf(path, encoding='utf-8', char_decode_errors='strict'):  # char_decode_errors='ignore'
    f = dbfread.DBF(path, encoding=encoding, char_decode_errors=char_decode_errors)
    df = pd.DataFrame(iter(f))
    return df


def save_json(path, obj):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)

        
def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def read_csv(path, encoding='utf-8', header=0):
    df = pd.read_csv(path, header=header, encoding=encoding,
                     low_memory=False, dtype=object)
    return df


def save_csv(path, df, encoding='utf-8'):
    df.to_csv(path, encoding=encoding, index=False)
    

# list to frequency dict
def freq_map_v1(lst):
    m = dict()
    for k in lst:
        if k in m.keys():
            m[k] += 1
        else:
            m[k] = 1
    return m


def freq_map(lst):
    counter = collections.Counter(lst)
    return dict(counter.items())


def freq_map_ordered(lst, reverse=False):
    counter = collections.Counter(lst)
    tpls = list(counter.items())
    tpls.sort(key=lambda x: x[1], reverse=reverse)
    return collections.OrderedDict(tpls)

# magic number
MAGIC = 1e6

def freq_map_ordered_by_key(lst, keys):
    if len(keys) != len(set(keys)):
        raise ValueError('Keys must be unique.')
    
    counter = collections.Counter(lst)
    tpls = list(counter.items())
    
    dt = dict(zip(keys, list(range(len(keys)))))
    tpls.sort(key=lambda x: dt.get(x[0], MAGIC))
    return collections.OrderedDict(tpls)


def count_nan(lst):
    bool_lst = [pd.isna(i) for i in lst]
    return len(lst), sum(bool_lst)


def get_clean_segs(s, sep=';'):
    segs = s.split(sep)
    segs = [i.strip() for i in segs]
    segs = [i for i in segs if i]
    return segs


# 列表排名
def get_orders(lt, reverse=True):
    lt_sorted = sorted(lt, reverse=reverse)
    orders = [lt_sorted.index(i) for i in lt]
    return orders


# 检验两个list值相等
def check_lst(lst1, lst2):
    try:
        lst1 = list(lst1)
        lst2 = list(lst2)
    except Exception as e:
        raise e
        
    if len(lst1) != len(lst2):
        return False
    l = len(lst1)
    bools = [i==j for i,j in zip(lst1, lst2)]
    if l != sum(bools):
        return False
    return True


# 随机的抽查检验两个表格的顺序
def random_check(df1, df2):
    common_cols = [i for i in df1.columns if i in df2.columns]
    if not len(common_cols):
        raise ValueError('The 2 table to check should have at list 1 common column.')
    rand_col = random.choice(common_cols)
    flag = check_lst(list(df1[rand_col]), list(df2[rand_col]))
    return flag


def get_fn_from_path(path):
    _, fn = os.path.split(path)
    return fn


def get_prefix_from_path(path):
    fn = get_fn_from_path(path)
    prefix, _ = os.path.splitext(fn)
    return prefix


def get_ext_from_path(path):
    fn = get_fn_from_path(path)
    _, ext = os.path.splitext(fn)
    return ext


# 给出list，得到排名
# 从1开始
def ranking(lt, ascending=True):
    uniq_vals = list(set(lt))
    reverse = not ascending
    lt_sorted = sorted(lt, reverse=reverse)
    m = dict([(k, lt_sorted.index(k)+1) for k in uniq_vals])
    r = [m[k] for k in lt]
    return r
