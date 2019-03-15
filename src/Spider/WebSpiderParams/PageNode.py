#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/20 10:04
# @Author  : lee
# @Contact : lqleeqee@gmail.com 
# @Site    : 
# @File    : PageNode.py
# @license : Copyright(C), Lee
# @Software: PyCharm
import hashlib
import zlib
import re
import os


# 页面节点数据结构
class PageNode(object):
    # 初始化一个节点
    def __init__(self, url=None, title=None, html=None, parent=None):
        self.parent = parent    # 指向父节点 Node
        self.url = url.strip()  # 记录当前节点得url
        self.title = title.strip()
        self.md5String = hashlib.md5(self.url.encode("utf-8")).hexdigest()
        self.depth = 0  # 节点层次
        self.child_list = []    # 子节点列表
        self.is_teacher_page = False
        self.html = html

    # 添加一个孩子节点
    def add_child(self, node):
        node.set_parent(self)
        node.depth = node.parent.depth + 1
        self.child_list.append(node)

    def set_html(self, page_source):
        self.html = zlib.compress(page_source.encode("utf-8"))
        pass

    def get_html(self):
        return zlib.decompress(self.html).decode("utf-8")
        pass

    def set_parent(self, parent):
        # 修改或设置父节点
        self.parent = parent

    def get_parent(self):
        return self.parent

    def set_url(self, url):
        self.url = url.strip()
        self.md5String = hashlib.md5(self.url.encode("utf-8")).hexdigest()

    def set_title(self, title):
        self.title = title

    # 判断节点是否是当前节点的子节点
    def node_is_child(self, name):
        type_name = type(name).__name__
        if isinstance(type_name, self.__class__.__name__):
            # 通过对象名称(节点名称)来判断
            for i in range(len(self.child_list)):
                if name.url == self.child_list[i].url\
                        or name.md5String == self.child_list[i].md5String:
                    return i
            return False
        # 通过value字符串字面值来对比和操作
        if isinstance(type_name, type("abc").__name__):
            for i in range(len(self.child_list)):
                if name == self.child_list[i].value\
                        or name == self.child_list[i].md5String:
                    return i
            return False
        raise TypeError("Bad Type of %s" % name)

    # 删除子节点
    def delete(self, name):
        mark = self.node_is_child(name)
        if mark >= 0:
            self.child_list.remove(self.child_list[mark])
        else:
            raise Exception("Node:%s not in the %s .child_list!" % (name, self.__class__.__name__))

    def save_to_disk(self, out_fd, depth=0):
        # out_fd = open(filename,'w', encoding='UTF-8')
        out_fd.flush()
        if self.url is not None \
                and self.title is not None :
            out_fd.write('- ' * depth + self.title
                         + '\t' + self.url
                         + '\n')
        elif self.url is not None\
                and self.title is None:
            out_fd.write('- ' * depth + "title: None"
                         + '\t' + self.url
                         + '\n')
        for child in self.child_list:
            child.save_to_disk(out_fd, depth + 2)

    def save_page(self, data_dir):
        domain_name = self.get_domain_name()
        cur_data_dir = os.path.abspath(os.path.join(data_dir, domain_name))
        if not os.path.exists(cur_data_dir):
            os.mkdir(cur_data_dir)
        file_name = os.path.join(cur_data_dir, self.md5String)
        if self.html:
            with open(file_name, 'w', encoding='utf-8') as page_fd:
                page_fd.write(self.url)
                page_fd.write('\n')
                page_fd.write(self.html)
                page_fd.write('\n')
            pass
        pass

    def get_domain_name(self):
        re_matcher = re.compile(r"""(?xi)\A
        [a-z][a-z0-9+\-.]*://                                # Scheme
        ([a-z0-9\-._~%!$&'()*+,;=]+@)?                       # User
        ([a-z0-9\-._~%]+                                     # Named or IPv4 host
        |\[[a-z0-9\-._~%!$&'()*+,;=:]+\])                    # IPv6+ host
        """)
        match = re_matcher.search(self.url)
        if match:
            dn = match.group(2)
            return dn[dn.index('.')+1:]

    # 展示树形结构
    def display(self, depth=0):
        if self.url is not None \
                and self.title is not None:
            print('- ' * depth + self.title + '\t' + self.url + '\t' + self.md5String + '\t' + str(self.depth))
        elif self.url is not None\
                and self.title is None:
            print('- ' * depth + "title: None" + '\t' + self.url + '\t' + self.md5String + '\t' + str(self.depth))
        for child in self.child_list:
            child.display(depth + 2)


if __name__ == "__main__":
    ruc = PageNode(url='https://www.ruc.edu.cn/', title='中国人民大学 | RENMIN UNIVERSITY of CHINA')
    hum = PageNode(url='https://www.ruc.edu.cn/humanities', title='中国人民大学 | RENMIN UNIVERSITY of CHINA')
    wen = PageNode(url='http://wenxueyuan.ruc.edu.cn/', title='中国人民大学文学院')
    ruc.add_child(hum)
    hum.add_child(wen)
    shizi = PageNode(url='http://wenxueyuan.ruc.edu.cn/sz/', title='中国人民大学文学院 - 师资团队 - 在职教师')
    wen.add_child(shizi)
    cheng = PageNode(url='http://wenxueyuan.ruc.edu.cn/sz/show/?106', title='中国人民大学文学院 - 师资团队 - 在职教师')
    shizi.add_child(cheng)
    ruc.display()
    print(hum.parent.url)
    pass
