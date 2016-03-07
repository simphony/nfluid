#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy


class TreeFunctions(object):
    n_bifs = 0

    @classmethod
    def reset(cls):
        TreeFunctions.n_bifs = 0

    @classmethod
    def n_bifurcations(cls, elem, params=None):
        if elem.next_l is not None and elem.next_r is not None:
            TreeFunctions.n_bifs += 1


class TreeNode(object):
    def __init__(self, data, prev=None, next_l=None, next_r=None):
        self.prev = prev
        self.next_l = next_l
        self.next_r = next_r
        self.data = data


class TreeBase(object):
    def __init__(self, root):
        # self.elements = []
        self.root = root
        # self.elements.append(self.root)

    def get_root(self):
        return self.root

    def depth(self):
        d = 0
        return self._depth(self.root, d)

    def _depth(self, cur_node, cur_depth):
        if cur_node is None:
            return cur_depth - 1
        d_l = self._depth(cur_node.next_l, cur_depth + 1)
        d_r = self._depth(cur_node.next_r, cur_depth + 1)
        if d_l > d_r:
            return d_l
        else:
            return d_r

    def amplitude(self):
        print "amplitude -------"
        TreeFunctions.reset()
        self.walk_amplitude(func=TreeFunctions.n_bifurcations)
        print TreeFunctions.n_bifs
        return TreeFunctions.n_bifs

    def n_leafs(self):
        d = self.depth()
        level = self.get_level(d)
        return len(level)

    def get_level(self, level):
        res = []
        queue = []
        queue.append((self.root, 0))
        while queue != []:
            (cur_elem, cur_level) = queue.pop(0)
            if cur_level == level:
                res.append(cur_elem)
            left = cur_elem.next_l
            right = cur_elem.next_r
            if left is not None and cur_level < level:
                queue.append((left, cur_level + 1))
            if right is not None and cur_level < level:
                queue.append((right, cur_level + 1))
        return res

    def search(self, value):
        return self.walk_amplitude(value)

    def walk_amplitude(self, value=None, func=None, params=None):
        res = []
        queue = []
        queue.append(self.root)
        while queue != []:
            cur_elem = queue.pop(0)
            if value is not None and value == cur_elem.data:
                return cur_elem
            res.append(cur_elem)
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
                return cur_elem
            res.append(cur_elem)
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
        cur_node = TreeNode(node.data)
        cur_node.prev = prev_node
        cur_node.next_l = None
        cur_node.next_r = None
        if prev_node.next_l is None:
            prev_node.next_l = cur_node
        else:
            prev_node.next_r = cur_node
        # self.elements.append(cur_node)
        return cur_node

    def add_data(self, prev_data, data):
        prev_node = self.search(prev_data)
        return self.add_node(prev_node, TreeNode(data))

    def strings_structure(self, name_space):
        res = []
        depth = self.depth()
        n_bifurcations = self.amplitude()
        mid = (n_bifurcations + 1) * name_space
        self._strings_structure(self.root, 0, mid, mid, depth, res)
        return res

    def _strings_structure(self, elem, cur_level, cur_tabs, total, depth, res):
        if elem is not None:
            res.append((elem, cur_level, cur_tabs))
            left = elem.next_l
            right = elem.next_r
            if left is not None:
                if right is not None:
                    total = total / 2
                    self._strings_structure(left, cur_level + 1,
                                            cur_tabs - total,
                                            total, depth, res)
                    self._strings_structure(right, cur_level + 1,
                                            cur_tabs + total,
                                            total, depth, res)
                else:
                    self._strings_structure(left, cur_level + 1, cur_tabs,
                                            total, depth, res)
            elif right is not None:
                self._strings_structure(right, cur_level + 1, cur_tabs,
                                        total, depth, res)

    def tree_as_str(self):
        name_len = 16
        strings = self.strings_structure(name_len)
        cur_level = 0
        res = ''
        tab_value = 2
        tab = ' '
        prev_tabs = 0
        prev_len = 0
        d = self.depth()
        by_levels = {}
        arrow = '|'
        for i in xrange(d+1):
            by_levels[i] = []
        for (elem, level, tabs) in strings:
            by_levels[level].append((elem, level, tabs))
        strings_ord = []
        for i in xrange(d+1):
            strings_ord = strings_ord + by_levels[i]
        print "strings_ord"
        for e in strings_ord:
            print e[0].data.get_name(), e
        for (elem, level, tabs) in strings_ord:
            if cur_level != level:
                res += '\n'
                prev_tabs = 0
                prev_len = 0
                cur_level = level
                # insert arrows
                cur_elems_level = by_levels[cur_level-1]
                prev_tabs2 = 0
                prev_len2 = 0
                arrows_str_prev = ''
                arrows_str_after = ''
                horizontal = ''
                for (elem2, level2, tabs2) in cur_elems_level:
                    cur_tabs2 = tabs2 - prev_tabs2
                    name = elem2.data.get_name()
                    # name = str(elem2.data.get_id())
                    total_chars = (cur_tabs2 * tab_value + name_len/2 -
                                   prev_len2)
                    if elem2.next_l is not None:
                        arrows_str_prev += total_chars * tab + arrow
                    else:
                        arrows_str_prev += (total_chars+1) * tab
                    prev_tabs2 += cur_tabs2
                    prev_len2 = name_len/2 + len(arrow)

                prev_tabs = 0
                prev_len = 0
                cur_level = level
                # insert arrows
                cur_elems_level = by_levels[cur_level]
                prev_tabs2 = 0
                prev_len2 = 0
                for (elem2, level2, tabs2) in cur_elems_level:
                    cur_tabs2 = tabs2 - prev_tabs2
                    name = elem2.data.get_name()
                    # name = str(elem2.data.get_id())
                    total_chars = (cur_tabs2 * tab_value + name_len/2 -
                                   prev_len2)
                    arrows_str_after += total_chars * tab + arrow

                    parent = elem2.prev
                    if parent.next_l is not None and parent.next_r is elem2:
                        horizontal += arrow + (total_chars) * '=' + arrow
                    elif parent.next_l is not None and parent.next_r is None:
                        horizontal += (total_chars) * tab + arrow
                    else:
                        horizontal += (total_chars) * tab

                    prev_tabs2 += cur_tabs2
                    prev_len2 = name_len/2 + len(arrow)

                res += arrows_str_prev + '\n' + horizontal + \
                    '\n' + arrows_str_after + '\n'

            cur_tabs = tabs - prev_tabs
            name = elem.data.get_name()
            # name = str(elem.data.get_id())
            # res += (cur_tabs * tab_value - prev_len)* tab + name
            res += (cur_tabs * tab_value - prev_len +
                    (name_len - len(name)) / 2) * tab + name
            prev_tabs += cur_tabs
            prev_len = len(name) + (name_len - len(name)) / 2
        return res
