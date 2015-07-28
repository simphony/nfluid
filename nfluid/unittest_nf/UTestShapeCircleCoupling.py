#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from nfluid.unittest_nf.unittest_base import *
from nfluid.elements.circle_coupling import *


class NFT_CircleCoupling(NFT_UnittestBase):

    def test_all_forward(self):
        print 'Hello test_all_forward'
        print 'Test Normal - forward, Pos - backward'

        create_channel(Coupling(R=10, L=45, PosH=Vector(0, 20, 30),
                       Normal=Vector(1, 0,
                       0))).link(Coupling(PosT=Vector(400, 20, 0)))
        self.process_chain()

    def test_bbb(self):
        print 'Hello test_bbb'
        self.process_chain()

    @staticmethod
    def suite():
        suite = unittest.TestSuite()
        suite.addTest(NFT_CircleCoupling('test_all_forward'))
        suite.addTest(NFT_CircleCoupling('test_bbb'))
        return suite


if __name__ == '__main__':

    print os.path.basename(__file__), '------------------------\n'

    if len(sys.argv) == 1:
        GetHelp(NFT_CircleCoupling)
        exit(0)

    if sys.argv[1] == '0':
        test = NFT_CircleCoupling('test_all_forward')

    #    test.test_all_forward()

        test.run()
    elif sys.argv[1] == '1':

        test = NFT_CircleCoupling('test_bbb')
        test.run()
    elif sys.argv[1] == '*':

        print 'Test_All'
        RunAllTests(NFT_CircleCoupling)
    else:

        print 'Incorrect argument value'
        exit(0)
