# -*- coding: utf-8 -*-
from jsonparser import JsonParser
import unittest

class TestJsonParser(unittest.TestCase):
    #初始化工作
    def setUp(self):
        self.jp = JsonParser()

    #退出清理工作
    def tearDown(self):
        pass

    #测试loads函数
    def testloads1(self):
        self.jp.loads('["foo", {"bar":["ba z","呵呵", null,"ab\"c",[true, 333], 1.0, 2], "se" : "ttt"}]')

    def testloads2(self):
        self.jp.loads('{"abb":664,788:{"btt":["ba22z","王者荣耀", null,"ss\"b\"c",[true, 666], 1.232340, 2234], "b" : false}}')

    #测试dumps函数
    def testdumps(self):
        self.assertEqual(self.jp.dumps(["foo",{u"bar":("baz",u"张竞豪", None, 1.0, 2), "c\"c": 123}]),
                         u'["foo",{"c\\\"c":123,"bar":["baz","张竞豪",null,1.0,2]}]')

    #测试load_dump函数
    def testdump_file(self):
        self.testloads1()
        self.jp.dump_file("./abc.txt")

    #测试load_file函数
    def testload_file(self):
        self.jp.load_file("./abc.txt")

    #测试load_dict函数
    def testload_dict(self):
        self.jp.load_dict({"a":1,"b":2,3:3,"d":{"a":1,"b":2, 3: 33,"bb":"dd"}})

    #测试dump_dict函数
    def testdump_dict(self):
        self.testload_dict()
        self.assertEqual(self.jp.dump_dict(),
                         {'a': 1, 'b': 2, 'd': {'a': 1, 'b': 2, 'bb': 'dd'}})

    #测试update函数
    def testupdate(self):
        self.testload_dict()
        self.jp.update({"cccc":12312312,"tt":"bbbcswdf","a":1111})

    #测试load_list函数
    def testload_list(self):
        self.jp.load_list(["foo", 123, None, {"abc": 123, "tt" : 23}])

    #测试dump_list函数
    def testdump_list(self):
        self.testload_list()
        self.assertEqual(self.jp.dump_list(),
                         ['foo', 123, None, {'tt': 23, 'abc': 123}])

    #测试实例对象利用[]获取或者修改值
    def testspecial_getter_and_setter(self):
        self.testload_dict()
        print(self.jp["a"]) #测试[]获取值

        self.jp["b"] = "new BB" #测试通过[]修改值
        print(self.jp["b"])

if __name__ == '__main__' :
    unittest.main()







