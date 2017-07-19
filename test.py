# -*- coding: utf-8 -*-
from jsonparser import JsonParser

jp = JsonParser()
jp.loads('["foo", {"bar":["ba z","呵呵", null,"ab\"c",[true, 333], 1.0, 2], "se" : "ttt"}]')

ob = ['foo',{'bar':('baz',"张竞豪", None, 1.0, 2), "c\"c": 123}]
ob2 = ['foo','abc',{"a":"c","d":"e","cc":['baz',False,1]}, None,("a","b")]
print(jp.dumps(ob))
print(jp.dumps(ob2))

s1 = "[abc呵呵".decode('utf-8')
s2 = "[abc"
print(s1[4] == u"呵")
print(type(s1))

my_dict = {
    "number": 163,
    "float": 1.63,
    "null": None,
    "true": True,
    "false": False,
    "array": [1, 6, 3],
    "empty array": [],
    "empty object": {},
    "object": {
        "space": " ",
        "backslash": "\\",
        "controls": "\b\f\n\r\t"
    },
    "one item array": ["a"],
    "one item object": {
        "key": "value"
    },
    "Chinese": "网易CC"
}
my_dict2 = {"Self":None,"UID":"6f50b429-5c13-4875-a29a-e4bd8d7b2772",\
            "Name":"blqw","Birthday":"1986-10-29 18:00:00","Sex":"Male","IsDeleted":False,\
            "LoginHistory":["2013-08-22 08:00:00","2013-08-22 10:10:10",\
                            "2013-08-22 12:33:56","2013-08-22 17:25:18","2013-08-22 23:06:59"],\
            "Info":{"Address":"广东省广州市","Phone":{"手机":"18688888888","电话":"82580000","短号":"10086","QQ":"21979018"},"ZipCode":510000},"Double":-333}
print(jp.dumps(my_dict2))

print ("abc\"abc".replace("\"", "\\\""))
