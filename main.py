import os

import pandas as pd

import util
import ztcata


if __name__ == '__main__':
    workdir = r'd:/workdir/ztcata-lab'
    src = os.path.join(workdir, 'middle.xlsx')
    
    df = util.read_excel(src)
    data = dict(zip(df['code'], df['成果数量']))
    tree = ztcata.tree.generate_tree(data)
    r = tree.traverse_post_order()
    
    temp_path = os.path.join(workdir, 'temp.xlsx')
    dft = pd.DataFrame(r, columns=['code', 'number'])
    util.save_excel(temp_path, dft)
    