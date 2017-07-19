from jsonparser import JsonParser

jp = JsonParser()
jp.loads('["foo", {"bar":["ba z", null,"abc",[true, 333], 1.0, 2], "se" : "ttt"}]')

ob = ['foo',{'bar':('baz', None, 1.0, 2)}]
ob2 = ['foo','abc',{"a":"c","d":"e","cc":['baz',False,1]}, None,("a","b")]
print(jp.dumps(ob))
print(jp.dumps(ob2))
