# coding: utf-8
# date: 20221209

'''
    输入字符串列表，生成前缀树结构。
    该树结构具有向上归并的方法，即当节点的值小于某阈值，归并至父节点上去。
'''


class Node:
    def __init__(self, path, value, is_root=False, is_leaf=False):
        self.path = path  # 父节点路径
        self.value = value  # 记录某些值
        self.is_root = is_root
        self.is_leaf = is_leaf  # leaf的含义有所变化，指对应了实际分类号的节点
        
        self.char = self.path[-1] if self.path else ''
        self.children = list()  # Node类型list
    
    def add(self, code, value):
        head = code[0]
        resi = code[1:]
        for child in self.children:
            if child.char == head:
                if len(resi):
                    child.add(resi, value)
                    return
                if child.is_leaf:
                    raise ValueError('Duplicate leaf node appeared.')
                else:
                    child.is_leaf = True
                    child.value = value
                    return
                
        # self子节点中不存在
        # 包含没有子节点情况
        if len(resi):
            new_child = Node(self.path+head, 0, False, False)
            new_child.add(resi, value)
        else:
            new_child = Node(self.path+head, value, False, True)
        self.children.append(new_child)
        return

    # 获取所有leaf节点
    def traverse_post_order(self):
        r = list()
        for child in self.children:
            r.extend(child.traverse_post_order())
        if self.is_leaf:
            r.append([self.path, self.value])
        return r

    # 根据阈值收缩
    # 直到所有叶子节点在阈值之上，或者收缩到根节点下一级
    # 后序遍历可以达到此目的
    def contract(self, threshold):
        keeps = list()
        

# 生成一棵树
def generate_tree(data):
    # data是以code为key的字典，value根据实际情况而定
    root = Node('', 0, True, True)
    
    for code, value in data.items():
        root.add(code, value)
    
    return root
        
            
        