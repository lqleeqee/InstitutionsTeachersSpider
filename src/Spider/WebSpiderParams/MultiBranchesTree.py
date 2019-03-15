#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/20 10:51
# @Author  : lee
# @Contact : lqleeqee@gmail.com 
# @Site    : 
# @File    : MultiBranchesTree.py
# @license : Copyright(C), Lee
# @Software: PyCharm
import hashlib
from queue import Queue
from src.Spider.WebSpiderParams.PageNode import PageNode
from src.Spider.WebSpiderParams.WebSpiderDriver import SpiderDriver


class MultiWayTree(object):

    def __init__(self, url, school_name, abbreviation_cn, abbreviation_en):
        self.root_node = PageNode(url=url.strip(), title=school_name)
        self.root_node.set_parent(None)
        self.histories = set()
        self.histories.add(hashlib.md5(url.strip().encode("utf-8")).hexdigest())
        self.abbreviation_cn = abbreviation_cn
        self.abbreviation_en = abbreviation_en

    def __add__(self, node, parent_node_url):
        if node.md5String not in self.histories:
            parent_node = self.breadth_first_search(parent_node_url)
            if parent_node is not None:
                parent_node.add_child(node)
                self.histories.add(node.md5String)
            else:
                if '/' not in parent_node_url:
                    return None
                parent_node_url = parent_node_url[:parent_node_url.rindex('/')]
                parent_node = self.breadth_first_search(parent_node_url)
                self.__add__(node, parent_node_url)
                # self.root_node.display()
                # raise ValueError('The parent node has not yet been created: %s' % parent_node_url)
        else:
            '''Nothing to do'''
            pass

    def __creatTree__(self):
        pass

    def __search_parent_node__(self, value):
        path_list = self.deep_first_search(self.root_node, value, [])
        return path_list

    # 深度优先查找,返回从根节点到目标节点的路径
    def deep_first_search(self, current_node, value, path=[]):
        # 当前节点值添加路径列表
        path.append(current_node)
        if current_node.url == value or current_node.md5String == value:
            # 如果找到目标,返回路径列表
            return path
        if current_node.child_list is None or len(current_node.child_list) <= 0:
            # 如果没有孩子列表就返回
            return None
        for node in current_node.child_list:
            # 对孩子列表里的每个孩子进行递归
            res = self.deep_first_search(node, value, path)
            if res is None:
                # 如果返回none,说明找到头没找到,利用临时路径继续找下一个孩子节点
                path.remove(node)   # 删除最新添加得节点
                continue
            else:
                # 如果返回的不是none说明找到了路径
                return res
        return None  # 如果所有孩子都没找到,则回溯

    # 广度优先搜索
    def breadth_first_search(self, value):
        queue = Queue()
        node_set = set()
        if self.root_node is None:
            return None
        queue.put(self.root_node)
        node_set.add(self.root_node)
        while not queue.empty():
            cur = queue.get()   # 弹出元素
            if cur.url == value or cur.md5String == value:
                return cur
            for child in cur.child_list:  # 遍历元素的邻接节点
                if child not in node_set:  # 若邻接节点没有入过队，加入队列并登记
                    node_set.add(child)
                    queue.put(child)
        return None

    def leaf_nodes(self, root_node, path=[]):
        if root_node.child_list is None or len(root_node.child_list) <= 0:
            # 如果是叶子节点就添加进列表
            path.append(root_node)
        for next_layer_node in root_node.child_list:
            self.leaf_nodes(next_layer_node, path)
        return path


if __name__ == "__main__":
    ruc_tree = MultiWayTree(url='https://www.ruc.edu.cn/',
                            school_name='中国人民大学', abbreviation_cn='人大', abbreviation_en='ruc')
    hum = PageNode(url='https://www.ruc.edu.cn/humanities', title='中国人民大学 | RENMIN UNIVERSITY of CHINA')
    ruc_tree.__add__(hum, parent_node_url='https://www.ruc.edu.cn/')
    wen = PageNode(url='http://wenxueyuan.ruc.edu.cn/', title='中国人民大学文学院')
    ruc_tree.__add__(wen, parent_node_url='https://www.ruc.edu.cn/humanities')
    ruc_tree.root_node.display()
    tp_node = ruc_tree.breadth_first_search('c7d3cdd30e1803412b615d7f234cbb5f')
    print(tp_node.title)
    tp_node = ruc_tree.breadth_first_search('https://www.ruc.edu.cn/humanities')
    print(tp_node.title)
    print(ruc_tree.histories)
    pass
    ############################################################################################


