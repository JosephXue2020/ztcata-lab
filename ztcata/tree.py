# coding: utf-8
# date: 20221209

'''
    输入字符串列表，生成前缀树结构。
    该树结构具有向上归并的方法，即当节点的值小于某阈值，归并至父节点上去。
'''


# 定义Value格式
class ValueItem:
    def __init__(self, code, number, keywords):
        self.code = code
        self.number = number
        self.keywords = keywords
        
        self.prop_codes = list()
    
    def merge(self, val):
        if not isinstance(val, ValueItem):
            raise TypeError("The type to merge should be ValueItem type.")
        self.number += val.number
        self.keywords += ';' + val.keywords
        self.prop_codes.append(val.code)


class Node:
    def __init__(self, path, value, is_root=False, is_raw=False):
        self.path = path  # 父节点路径
        self.value = value  # 记录某些值
        self.is_root = is_root
        # 原始节点对应实际分类号
        # 叶子节点必为原始节点
        self.is_raw = is_raw
        
        self.char = self.path[-1] if self.path else ''
        self.children = list()  # Node类型list
        
        self.prop_lt = list()  # 用来追踪反向传播回来的值
    
    def add(self, code, value):
        head = code[0]
        resi = code[1:]
        for child in self.children:
            if child.char == head:
                if len(resi):
                    child.add(resi, value)
                    return
                if child.is_raw:
                    raise ValueError('Duplicate raw node appeared.')
                else:
                    child.is_raw = True
                    child.value = value
                    return
                
        # self子节点中不存在
        # 包含没有子节点情况
        if len(resi):
            new_child = Node(self.path+head, None, False, False)
            new_child.add(resi, value)
        else:
            new_child = Node(self.path+head, value, False, True)
        self.children.append(new_child)
        return

    # 获取所有raw节点
    def traverse_post_order(self):
        r = list()
        for child in self.children:
            r.extend(child.traverse_post_order())
        if self.is_raw:
            r.append(self.value)
        return r

    # 根据阈值收缩
    # 直到所有叶子节点在阈值之上，或者收缩到根节点下一级
    # 后序遍历可以达到此目的
    def contract(self, threshold):
        keeps = list()
        for i, child in enumerate(self.children):
            # child的children非空
            if not len(child.children):
                child.contract(threshold)
            # 收缩完仍然非空
            if not len(child.children):
                keeps.append(i)
                if not child.is_raw:
                    self.prop_lt.extend(child.prop_lt)
                else:
                    if child.value.number <= threshold: 
                        self.prop_lt.append(child.value)
                        child.is_raw = False
            else:
                if not child.is_raw:
                    self.prop_lt.extend(child.prop_lt)
                else:
                    if child.value.number > threshold:
                        keeps.append(i)
                    else:
                        self.prop_lt.append(child.value)
        
        new_children = [child for i, child in enumerate(self.children) if i in keeps]
        self.children = new_children
        # 如果self是raw，合并value
        if self.is_raw:
            for val in self.prop_lt:
                self.value.merge(val)
            self.prop_lt = list()
            
        return
            
        

# 生成一棵树
def generate_tree(data):
    # data是以code为key的字典，value为字典类型
    root = Node('', None, True, False)
    
    for code, value in data.items():
        value_item = ValueItem(value['code'], value['number'], value['keywords'])
        root.add(code, value_item)
    
    return root
        
            
        