#!/usr/bin/python
# -*- coding: utf-8 -*-

# from nfluid.core.gate_base import Gate
# from nfluid.shapes.shapes import Shape, CreateShape
from nfluid.util.vector import is_colinear
from nfluid.util.rotations import (
    GetRotationMatrixVectorToVector, GetRotationMatrixVectorFaceToVector)


# Base class of Channel Elements

class ChannelElement(object):

    assembly = None
    __id_cnt = 0

    def __init__(self):
        ChannelElement.assembly.add_element(self)
        self.heads = []
        self.tails = []
        self.changed = True
        self.shape = None
        self.__id = ChannelElement.__id_cnt
        ChannelElement.__id_cnt += 1
        self.IsAxialSym = False
        self.IsEqualGateSize = False

        self.RotationOperator = None
        self.CenterPos = None

    def get_name(self):
        return 'ChannelElement'

    def get_chain_str(self):
        prev = self.get_prev_element()
        if prev is not None:
            return prev.get_chain_str() + '|' + self.get_name()
        else:
            return self.get_name()

    def get_id(self):
        return self.__id

    def get_head_gate(self, n=0):
        return self.heads[n]

    def get_tail_gate(self, n=0):
        return self.tails[n]

    def get_pos_head(self, n=0):
        return self.get_head_gate(n).Pos

    def get_pos_tail(self, n=0):
        return self.get_tail_gate(n).Pos

    def get_normal_head(self, n=0):
        return self.get_head_gate(n).Normal

    def get_normal_tail(self, n=0):
        return self.get_tail_gate(n).Normal

    def get_next_element(self, n=0):
        gt = self.get_tail_gate(n)
        if gt is None:
            return None
        gtb = gt.buddy
        if gtb is None:
            return None
        return gtb.element

    def get_prev_element(self, n=0):
        gh = self.get_head_gate(n)
        if gh is None:
            return None
        ghb = gh.buddy
        if ghb is None:
            return None
        return ghb.element

    def link(
        self,
        next,
        gateTail=0,
        gateHead=0,
    ):
        self.get_tail_gate(gateTail).link(next.get_head_gate(gateHead))
        return next

    def print_info(self):
        print 'id=', self.__id
        self.for_each_gate(fcn_print_info_xxx)

#     print "ChannelElement"

    def print_info_channel(self):
        self.print_info()
        next = self.get_next_element()
        if next is not None:
            next.print_info_channel()

#  "" nothing changed
#  "ok" something changed
#  "other text" - fatal error

    def resolve_geometry(self):
        print '+++++++++++++ resolve_geometry beg', self.get_name(), \
            '+++++++++++++'
        ret = ''
        res = self.resolve_geometry_base()
        print 'resolve_geometry_base=', res
        if res == '':
            pass
        elif res == 'ok':
            ret = 'ok'
        else:
            return res

        print 'self.IsEqualGateSize', self.IsEqualGateSize
        if self.IsEqualGateSize:
            res = self.set_equal_gate_size()
            print 'set_equal_gate_size res=', res
            if res == '':
                pass
            elif res == 'ok':
                ret = 'ok'
            else:
                return res

        res = self.resolve_geometry_child()
        print 'resolve_geometry_child res=', res
        if res == '':
            pass
        elif res == 'ok':
            ret = 'ok'
        else:
            return res

        res = self.resolve_geometry_pos_norm_generic()
        print 'resolve_geometry_pos_norm_generic res=', res
        if res == '':
            pass
        elif res == 'ok':
            ret = 'ok'
        else:
            return res

        res = self.resolve_geometry_pos_norm()
        print 'resolve_geometry_pos_norm res=', res
        if res == '':
            pass
        elif res == 'ok':
            ret = 'ok'
        else:
            return res

        res = self.resolve_geometry_set_gates_norm_pos()
        print 'resolve_geometry_set_gates_norm_pos res=', res
        if res == '':
            pass
        elif res == 'ok':
            ret = 'ok'
        else:
            return res

        print 'resolve_geometry ret=', ret
        return ret

    def resolve_geometry_child(self):
        return ''

    def resolve_geometry_pos_norm(self):
        return ''

    def resolve_geometry_pos_norm_generic(self):
        pairs_normal = self.collect_gate_pairs_normal()

        print '$$$$$$$$$$$$$$$$$$$$$$ pairs_normal'

        #  Non collinear vectors

        pairs_normal_nc = []

        for pair in pairs_normal:
            print pair[0], pair[1]
            nc_flag = True
            for nc_pair in pairs_normal_nc:
                if is_colinear(pair[0], nc_pair[0]):
                    nc_flag = False

            if nc_flag:
                pairs_normal_nc.append(pair)

        print '$$$$$$$$$$$$$$$$$$$$$$ pairs_normal_nc'
        for pair in pairs_normal_nc:
            print pair[0], pair[1]

        pairs_pos = self.collect_gate_pairs_pos()

        print '$$$$$$$$$$$$$$$$$$$$$$ pairs_pos'

        for pair in pairs_pos:
            print pair[0], pair[1]

        #  Resolving of orientation

        print 'Resolving of orientation'
        print 'IsAxialSym=', self.IsAxialSym
        if self.IsAxialSym:
            print 'IsAxialSym'
            if len(pairs_normal_nc) >= 1:
                print 'Normal exists'
                self.RotationOperator = \
                    GetRotationMatrixVectorToVector(pairs_normal_nc[0][0],
                                                    pairs_normal_nc[0][1])
            else:
                print 'Check positions'
                if len(pairs_pos) >= 2:
                    print 'More than 1 positions'
                    DiffElement = pairs_pos[1][0] - pairs_pos[0][0]
                    RealElement = pairs_pos[1][1] - pairs_pos[0][1]
                    self.RotationOperator = \
                        GetRotationMatrixVectorToVector(DiffElement,
                                                        RealElement)
        else:
            print 'no IsAxialSym'
            if len(pairs_normal_nc) >= 2:
                print 'Two Normal exists'
                axis = pairs_normal_nc[0][1]
                rot1 = GetRotationMatrixVectorToVector(pairs_normal_nc[0][0],
                                                       axis)
                print 'Rot1'
                rot1.trace()

                (rot2, res2) = GetRotationMatrixVectorFaceToVector(
                    rot1 * pairs_normal_nc[1][0], pairs_normal_nc[1][1],
                    axis)
                if res2 != '':
                    return res2
                rot2.trace()
                print 'Rot2'
                rot2.trace()

                self.RotationOperator = rot2 * rot1
            elif len(pairs_pos) >= 3:
                print '3  positions'
                DiffElement1 = pairs_pos[1][0] - pairs_pos[0][0]
                RealElement1 = pairs_pos[1][1] - pairs_pos[0][1]  # axis
                DiffElement2 = pairs_pos[2][0] - pairs_pos[0][0]
                RealElement2 = pairs_pos[2][1] - pairs_pos[0][1]

                rot1 = GetRotationMatrixVectorToVector(DiffElement1,
                                                       RealElement1)
                print 'Rot1'
                rot1.trace()

                (rot2, res2) = GetRotationMatrixVectorFaceToVector(
                    rot1 * DiffElement2, RealElement2,
                    RealElement1)
                if res2 != '':
                    return res2
                print 'Rot2'
                rot2.trace()

                self.RotationOperator = rot2 * rot1
            elif len(pairs_normal_nc) == 1 and len(pairs_pos) >= 2:
                print 'Normal and pos'
                pos_nc = None
                for i in range(0, len(pairs_pos) - 1):
                    DiffElement0 = pairs_pos[i + 1][0] - pairs_pos[i][0]
                    print 'DiffElement0 ', DiffElement0
                    if not is_colinear(DiffElement0,
                                       pairs_normal_nc[0][0]):
                        pos_nc = i
                        break

                if pos_nc is not None:
                    DiffElement = pairs_pos[pos_nc + 1][0] \
                        - pairs_pos[pos_nc][0]
                    RealElement = pairs_pos[pos_nc + 1][1] \
                        - pairs_pos[pos_nc][1]

                    axis = pairs_normal_nc[0][1]
                    rot1 = \
                        GetRotationMatrixVectorToVector(pairs_normal_nc[0][0],
                                                        axis)
                    rot1.trace()

                    (rot2, res2) = \
                        GetRotationMatrixVectorFaceToVector(
                            rot1 * DiffElement, RealElement, axis)
                    if res2 != '':
                        return res2
                    rot2.trace()

                    self.RotationOperator = rot2 * rot1

        if self.RotationOperator is not None:
            print 'Orientation Resolved'
            self.RotationOperator.trace()
        else:

            print 'Orientation not Resolved'

        #  Resolving of positions

        print 'Resolving of positions'
        if len(pairs_pos) > 0:
            print 'pairs_pos > 0'
            if self.RotationOperator is not None:
                print 'RotationOperator is not None'
                RealShift = self.RotationOperator * pairs_pos[0][0]
                print 'RealShift, pairs_pos[0][1]', RealShift, \
                    pairs_pos[0][1]
                self.CenterPos = pairs_pos[0][1] - RealShift
                self.CenterPos.round()

        if self.CenterPos is not None:
            print 'CenterPos Resolved CenterPos', self.CenterPos
        else:
            print 'CenterPos not Resolved'

        return ''

    def resolve_geometry_set_gates_norm_pos(self):
        if self.RotationOperator is None:
            return ''

        ret = ''

        res = \
            self.for_each_gate_err_ok(resolve_geometry_set_gates_norm_fcn,
                                      self)
        if res == '':
            pass
        elif res == 'ok':
            ret = 'ok'

        else:
            return res

        res = \
            self.for_each_gate_err_ok(resolve_geometry_set_gates_pos_fcn,
                                      self)
        if res == '':
            pass
        elif res == 'ok':
            ret = 'ok'

        else:
            return res

        print 'resolve_geometry_set_gates_norm_pos ret=', ret
        return ret

#  "" nothing changed
#  "ok" something changed
#  "other text" - fatal error

    def resolve_geometry_base(self):
        return self.for_each_gate_err_ok(resolve_geometry_base_fcn)

    def is_resolved_geometry(self):
        return self.for_each_gate_err(is_resolved_geometry_fcn)

    def set_equal_gate_size(self):
        return self.for_each_gate_err_ok(set_equal_gate_size_fcn)

    def set_gate_size_all(self, Size):
        return self.for_each_gate_err_ok(set_gate_size_fcn, Size)

    # @staticmethod

    def fcn_clear_geometry(gate):
        gate.clear_geometry()

    def clear_geometry(self):
        self.for_each_gate(fcn_clear_geometry_xxx)

        # self.for_each_gate(ChannelElement.fcn_clear_geometry)

    def for_each_gate(self, fcn):

        for gate in self.heads:
            fcn(gate)
        for gate in self.tails:
            fcn(gate)

    def for_each_gate_err(self, fcn, arg=None):
        for i in xrange(0, len(self.heads)):
            res = fcn(self.heads[i], self, arg)
            if res != '':
                return 'Head gate # ' + str(i) + ': ' + str(res)

        for i in xrange(0, len(self.tails)):
            res = fcn(self.tails[i], self, arg)
            if res != '':
                return 'Tail gate # ' + str(i) + ': ' + str(res)

        return ''

    def for_each_gate_err_ok(self, fcn, arg=None):
        ret = ''

        for i in xrange(0, len(self.heads)):
            res = fcn(self.heads[i], self, arg)
            if res == '':
                pass
            elif res == 'ok':
                ret = 'ok'
            else:
                print 'for_each_gate_err_ok  !!!'
                return 'Head gate # ' + str(i) + ': ' + str(res)

        for i in xrange(0, len(self.tails)):
            res = fcn(self.tails[i], self, arg)
            if res == '':
                pass
            elif res == 'ok':
                ret = 'ok'
            else:
                return 'Tail gate # ' + str(i) + ': ' + str(res)

        return ret

    def collect_gate_pairs_normal(self):
        pairs = []
        for gate in self.heads:
            if (gate.NormalElement is not None and
                    gate.Normal.is_not_none()):
                pairs.append((gate.NormalElement, gate.Normal))
        for gate in self.tails:
            if (gate.NormalElement is not None and
                    gate.Normal.is_not_none()):
                pairs.append((gate.NormalElement, gate.Normal))
        return pairs

    def collect_gate_pairs_pos(self):
        pairs = []
        for gate in self.heads:
            if gate.PosElement is not None and gate.Pos.is_not_none():
                pairs.append((gate.PosElement, gate.Pos))
        for gate in self.tails:
            if gate.PosElement is not None and gate.Pos.is_not_none():
                pairs.append((gate.PosElement, gate.Pos))
        return pairs

    def detach(self):
        gates_tails = []
        for gate in self.tails:
            gates_tails.append(gate.detach())

        gates_heads = []
        for gate in self.heads:
            gates_heads.append(gate.detach())

        return (gates_tails, gates_heads)

    def create_shape(self):
        self.shape = self.create_shape_child()

        for gate in self.heads:
            if gate.buddy is not None:
                element = gate.buddy.element
                if self.shape is not None:
                    self.shape.add_link_head(element.shape)
                n = element.tails.index(gate.buddy)
                if element.shape is not None:
                    element.shape.set_link_tail(n, self.shape)

        return ''

    def create_shape_child(self):
        return None

    def release_shape(self):
        print 'release_shape'
        self.shape = None

    def export(self, file):
        if self.shape is not None:
            self.shape.export(file)

    def show_shape(self):
        if self.shape is not None:
            self.shape.show()


def resolve_geometry_base_fcn(gate, elem, arg):
    return gate.resolve_geometry()


def is_resolved_geometry_fcn(gate, elem=None, arg=None):
    return gate.is_resolved_geometry()


def set_equal_gate_size_fcn(gate, elem, arg):
    return elem.set_gate_size_all(gate.Size)


def set_gate_size_fcn(gate, elem, arg):
    return gate.set_size(arg)


def resolve_geometry_set_gates_norm_fcn(gate, elem, arg=None):
    if gate.NormalElement is not None:
        RealNormal = elem.RotationOperator * gate.NormalElement
        return gate.set_normal(RealNormal)


def resolve_geometry_set_gates_pos_fcn(gate, elem, arg=None):
    if elem.CenterPos is not None and gate.PosElement is not None:
        RealShift = elem.RotationOperator * gate.PosElement
        return gate.set_pos(elem.CenterPos + RealShift)


def fcn_clear_geometry_xxx(gate):
    gate.clear_geometry()


def fcn_print_info_xxx(gate):
    print 'Gate --------------------'
    gate.print_info()
