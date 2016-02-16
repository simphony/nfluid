#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy


class TreeNode(object):
    def __init__(self, data, prev=None, next_l=None, next_r=None):
        self.prev = prev
        self.next_l = next_l
        self.next_r = next_r
        self.data = copy.deepcopy(data)


class TreeBase(object):
    def __init__(self, root):
        self.elements = []
        self.root = copy.deepcopy(root)
        self.elements.append(self.root)

    def get_root(self):
        return self.root

    def depth(self):
        d = 1
        return self._depth(self.root, d)

    def amplitude(sefl):
        pass

    def n_leafs(self):
        d = self.depth()
        level = self.get_level(d)
        return len(level)

    def get_level(self, level):
        res = []
        queue = []
        queue.append((self.root, 1))
        while queue != []:
            (cur_elem, cur_level) = queue.pop(0)
            if cur_level == level:
                res.append(copy.deepcopy(cur_elem))
            left = cur_elem.next_l
            right = cur_elem.next_r
            if left is not None and cur_level < level:
                queue.append((left, cur_level + 1))
            if right is not None and cur_level < level:
                queue.append((right, cur_level + 1))
        return res

    def _depth(self, cur_node, cur_depth):
        if cur_node is None:
            return cur_depth - 1
        d_l = self._depth(cur_node.next_l, cur_depth + 1)
        d_r = self._depth(cur_node.next_r, cur_depth + 1)
        if d_l > d_r:
            return d_l
        else:
            return d_r

    def search(self, value):
        return self.walk_amplitude(value)

    def walk_amplitude(self, value=None, func=None, params=None):
        res = []
        queue = []
        queue.append(self.root)
        while queue != []:
            cur_elem = queue.pop(0)
            if value is not None and value == cur_elem.data:
                return copy.deepcopy(cur_elem)
            res.append(copy.deepcopy(cur_elem))
            if func:
                func(cur_elem, params)
            left = cur_elem.next_l
            right = cur_elem.next_r
            if left is not None:
                queue.append(left)
            if right is not None:
                queue.append(right)
        return res

    def walk_depth(self, value=None, func=None, params=None):
        res = []
        queue = []
        queue.append(self.root)
        while queue != []:
            cur_elem = queue.pop()
            if value is not None and value == cur_elem.data:
                return copy.deepcopy(cur_elem)
            res.append(copy.deepcopy(cur_elem))
            if func:
                func(cur_elem, params)
            left = cur_elem.next_l
            right = cur_elem.next_r
            if right is not None:
                queue.append(right)
            if left is not None:
                queue.append(left)
        return res

    def add_node(self, prev_node, node):
        if prev_node.next_l is not None and prev_node.next_r is not None:
            raise Exception("Full node! Can't add anything to it!")
        # if node.data is None:
            # raise Exception("Empty node!!!!")
        cur_node = TreeNode(copy.deepcopy(node.data))
        cur_node.prev = prev_node
        cur_node.next_l = None
        cur_node.next_r = None
        if prev_node.next_l is None:
            prev_node.next_l = cur_node
        else:
            prev_node.next_r = cur_node
        self.elements.append(cur_node)
        return cur_node

    def add_data(self, prev_data, data):
        prev_node = self.search(prev_data)
        return self.add_node(prev_node, TreeNode(data))
