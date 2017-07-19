# -*- coding: utf-8 -*-
import logging


class JsonParser:
    def __init__(self):
        self._data = None

    """
    方法：loads(self, s)
    输入参数：字符串s
    返回参数：None
    描述：用于将Json格式的字符串s解析为Python对象存储于实例变量之中
    """
    def loads(self, s):
        #如果s是None或是空串""
        if s == None or len(s) == 0:
            self._data = None

        if isinstance(s, str):
            s = str(s).decode('utf-8')

        stack = []
        stack_tmp = []

        try:
            while len(s) > 0:
                if s[0] == "[":
                    stack.append("[")
                    if isinstance(s, unicode):
                        s = s[1:].strip()     #更新s并去除空格

                elif s[0] == "]":
                    #出栈到[，处理生成obj，将obj入栈
                    if isinstance(s, unicode):
                        s = s[1:].strip()     #去除空格
                    tmp = stack.pop()
                    #logging.warning(stack)
                    while tmp != "[":
                        stack_tmp.insert(0, tmp)
                        tmp = stack.pop()

                    newest_obj = []
                    #logging.warning(stack_tmp)
                    if len(stack_tmp) % 2 != 1: #必须是XXX，XXX，XXX的样式
                        raise MyException #抛格式异常
                    idx = 0
                    while idx < len(stack_tmp):
                        if idx % 2 == 0:
                            newest_obj.append(stack_tmp[idx])
                        else :
                            if not self.check_comma(stack_tmp[idx]):
                                raise MyException #抛格式异常
                        idx += 1
                    stack.append(newest_obj)
                    while len(stack_tmp) > 0:
                        stack_tmp.pop()

                elif s[0] == "{":
                    stack.append("{")
                    if isinstance(s, unicode):
                        s = s[1:].strip()    #更新s并去除空格

                elif s[0] == "}":
                    #出栈到{，处理生成obj，将obj入栈
                    if isinstance(s, unicode):
                        s = s[1:].strip()    #更新s并去除空格
                    tmp = stack.pop()
                    while tmp != "{":
                        stack_tmp.insert(0, tmp)
                        tmp = stack.pop()

                    #logging.warning(stack_tmp)
                    newest_obj = {}
                    if len(stack_tmp) % 4 != 3: #必须是key:value,key:value的样式
                        raise MyException #抛格式异常
                    idx = 0
                    while idx < len(stack_tmp):
                        if idx % 4 == 0:
                            newest_obj[stack_tmp[idx]] = stack_tmp[idx + 2]
                        elif idx % 4 == 1:
                            if not self.check_colon(stack_tmp[idx]):
                                raise Exception #抛格式异常
                        elif idx % 4 == 3:
                            if not self.check_comma(stack_tmp[idx]):
                                raise Exception #抛格式异常
                        idx += 1
                    stack.append(newest_obj)
                    while len(stack_tmp) > 0:
                        stack_tmp.pop()

                elif s[0] == ",":
                    stack.append(",")
                    if isinstance(s, unicode):
                        s = s[1:].strip()    #更新s并去除空格

                elif s[0] == ":":
                    stack.append(":")
                    if isinstance(s, unicode):
                        s = s[1:].strip()    #更新s并去除空格

                else:
                    tmp_end_index = self.find_end_index(s)
                    tmp_content = s[:tmp_end_index]
                    if isinstance(tmp_content, unicode):
                        tmp_content = tmp_content.strip()
                        #转义字符处理
                        tmp_content = tmp_content.replace("\\\"", "\"")
                        tmp_content = tmp_content.replace("\\\'", "\'")

                    if isinstance(s, unicode):
                        s = s[tmp_end_index:].strip()    #更新s并去除空格

                    stack.append(self.change_form(tmp_content))
                    #logging.warning(stack)

            if len(stack) != 1: #如果最后stack中不是只有obj自己，那么说明格式错误
                #logging.warning(stack)
                raise MyException #抛格式异常
            self._data = stack[0]
            #打印转化后的_data对象
            #print("loads转化后的_data对象：" + unicode(self._data))
            print self._data
        except MyException:
            print("格式错误")

    """
    内部方法：find_end_index(self, s)
    输入参数：字符串s
    返回参数：位置index
    描述：用于从头开始寻找字符串s第一个特殊符号的位置
    """
    def find_end_index(self, s):
        index = 0
        while index < len(s):
            if s[index] == "[" or s[index] == "]" or s[index] == "{" or s[index] == "}" \
                    or s[index] == "," or s[index] == ":":
                break
            else:
                index += 1
        return index

    """
    内部方法：check_comma(self, c)
    输入参数：字符c
    返回参数：bool值
    描述：判断该字符是否为","
    """
    def check_comma(self, c):
        if c == ",":
            return True
        else:
            return False

    """
    内部方法：check_colon(self, c)
    输入参数：字符c
    返回参数：bool值
    描述：判断该字符是否为":"
    """
    def check_colon(self, c):
        if c == ":":
            return True
        else:
            return False

    """
    内部方法：change_form(self, tmp_content)
    输入参数：字符串tmp_content
    返回参数：Python对象
    描述：用于将字符串转为相应的Python对象
    """
    def change_form(self, tmp_content):
        if isinstance(tmp_content, unicode):
            try:
                if len(tmp_content) >= 2 and tmp_content.startswith("\"") and tmp_content.endswith("\""):
                    return tmp_content[1:-1]
                elif tmp_content == "true":
                    return True
                elif tmp_content == "false":
                    return False
                elif tmp_content == "null":
                    return None
                elif self.is_int(tmp_content):
                    return int(tmp_content)
                elif self.is_float(tmp_content):
                    return float(tmp_content)
                else:
                    raise MyException
            except MyException:
                print("格式错误")

    """
    内部方法：is_float(self, tmp_content)
    输入参数：字符串tmp_content
    返回参数：bool值
    描述：用于判断字符串是否是float类型
    """
    def is_float(self, tmp_content):
        try:
            float(tmp_content)
            return True
        except ValueError:
            return False

    """
    内部方法：is_int(self, tmp_content)
    输入参数：字符串tmp_content
    返回参数：bool值
    描述：用于判断字符串是否是int类型
    """
    def is_int(self, tmp_content):
        try:
            int(tmp_content)
            return True
        except ValueError:
            return False


    """
    方法：dumps(self, obj)
    输入参数：Python对象
    返回参数：Json格式字符串
    描述：对象转Json字符串，返回Json字符串
    """
    def dumps(self, obj):
        #若对象是[]或者是()
        if isinstance(obj, list) or isinstance(obj, tuple):
            index = 0
            length = len(obj)
            tmpstr = ""
            while True:
                if index >= length:
                    break
                if index != 0:
                    tmpstr += ","
                tmpstr += unicode(self.dumps(obj[index]))
                index += 1
            tmpstr = "["+tmpstr+"]"
            return tmpstr

        #若对象是None
        elif obj is None:
            return "null"

        #若对象是bool
        elif isinstance(obj, bool):
            if obj:
                return "true"
            else:
                return "false"

        #若对象是int或float
        elif isinstance(obj, int) or isinstance(obj, float):
            return unicode(obj)

        #若对象是str
        elif isinstance(obj, str):
            obj = obj.decode('utf-8')
            #转义字符处理
            obj = obj.replace("\"", "\\\"")
            obj = obj.replace("\'", "\\\'")

            return "\"" + obj + "\""

        #若对象是unicode
        elif isinstance(obj, unicode):
            #转义字符处理
            obj = obj.replace("\"", "\\\"")
            obj = obj.replace("\'", "\\\'")

            return "\"" + obj + "\""

        #若对象是{key : value, key : value}
        elif isinstance(obj, dict):
            tmpstr = ""
            count = 0
            for key, value in obj.items():
                tmpstr += unicode(self.dumps(key)) + ":" + unicode(self.dumps(value))
                count += 1
                if count < len(obj):
                    tmpstr += ","
            tmpstr = "{" + tmpstr + "}"
            return tmpstr


    """
    方法：load_file(self, f)
    输入参数：路径f
    返回参数：None
    描述：读取路径为f的文件中的Json串，生成一个对象存在实例对象中
    """
    def load_file(self, f):
        try :
            file = open(f, 'r')
            fr = file.read()
            self._data = self.loads(fr)
        except IOError:
            print("找不到文件")
        except KeyboardInterrupt:
            print("你取消了读文件操作")
        finally:
            if file:
                file.close()


    """
    方法：dump_file(self, f)
    输入参数：路径f
    返回参数：None
    描述：将存在于实例对象中的Python对象生成Json字符串存入路径为f的文件中
    """
    def dump_file(self,f):
        file = open(f, 'w')
        #logging.warning(self.dumps(self._data))
        file.write(self.dumps(self._data).encode('utf-8'))
        file.close()


    """
    方法：load_dict(self, d)
    输入参数：字典d
    返回参数：None
    描述：将字典d深拷贝到_data
    """
    def load_dict(self, d):
        if isinstance(d, dict):
            self._data = {}
        else:
            return

        for key, value in d.items():
            if isinstance(key, str):
                self._data[key] = self.deep_copy(value)

        #显示刚存入_data的字典
        print(self._data)

    """
    方法：dump_dict(self)
    输入参数：None
    返回参数：字典
    描述：将实例对象中的_data的深拷贝字典{}返回
    """
    def dump_dict(self):

        if isinstance(self._data, dict):
            d = {}
        else :
            return None
        for key, value in self._data.items():
            if isinstance(key, str):
                d[key] = self.deep_copy(value)
        return d

    """
    方法：update(self, d)
    输入参数：字典d
    返回参数：None
    描述：将字典d中的key与value更新到实例变量中
    """
    def update(self, d):
        if isinstance(d, dict) and isinstance(self._data, dict):
            for key, value in d.items():
                if isinstance(key, str):
                    self._data[key] = self.deep_copy(value)
        else:
            print("_data原格式不是字典，无法更新")

        print(self._data)


    """
    方法：load_list(self, l)
    输入参数：列表l
    返回参数：None
    描述：将列表l深拷贝到_data
    """
    def load_list(self, l):
        if isinstance(l, list):
            self._data = []
        else:
            return

        for value in l:
            self._data.append(self.deep_copy(value))

        #显示刚存入_data的列表
        print(self._data)


    """
    方法：dump_list(self)
    输入参数：None
    返回参数：列表
    描述：将实例对象中的_data的深拷贝列表[]返回
    """
    def dump_list(self):

        if isinstance(self._data, list):
            l = []
        else:
            return None
        for value in self._data:
            l.append(self.deep_copy(value))
        return l


    """
    内部方法：deep_copy(self, value)
    输入参数：Python对象
    返回参数：Python对象
    描述：对于list和dict实行深拷贝，返回深拷贝实例
    """
    def deep_copy(self, value):
        if isinstance(value, list):
            obj = []
            for tmp in value:
                obj.append(self.deep_copy(value))
        elif isinstance(value, dict):
            obj = {}
            for k, v in value.items():
                if isinstance(k, str):
                    obj[k] = self.deep_copy(v)
        else:
            obj = value

        return obj


class MyException(Exception):
    def __init__(self):
        Exception.__init__(self)
