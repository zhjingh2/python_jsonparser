# -*- coding: utf-8 -*-
import logging


class JsonParser:
    def __init__(self):
        self._data = None

    #######################################################
    # loads(self, s)
    # json字符串转对象，存储在_data中
    #######################################################
    def loads(self, s):
        #打印输入的json串
        #print("loads输入的json串:" + s)

        #如果s是None或是空串""
        if s == None or len(s) == 0 :
            self._data = None

        stack = []
        stack_tmp = []

        while len(s) > 0 :
            if s[0] == "[" :
                stack.append("[")
                if isinstance(s, str) :
                    s = s[1:].strip()     #更新s并去除空格

            elif s[0] == "]" :
                #出栈到[，处理生成obj，将obj入栈
                if isinstance(s, str) :
                    s = s[1:].strip()     #去除空格
                tmp = stack.pop()
                #logging.warning(stack)
                while tmp != "[" :
                    stack_tmp.insert(0, tmp)
                    tmp = stack.pop()
                    #logging.warning(tmp != "[")

                newest_obj = []
                #logging.warning(stack_tmp)
                if len(stack_tmp) % 2 != 1 : #必须是XXX，XXX，XXX的样式
                    raise Exception #抛格式异常
                idx = 0
                while idx < len(stack_tmp) :
                    if idx % 2 == 0 :
                        newest_obj.append(stack_tmp[idx])
                    else :
                        if not self.check_comma(stack_tmp[idx]) :
                            raise Exception #抛格式异常
                    idx += 1
                stack.append(newest_obj)
                while len(stack_tmp) > 0 :
                    stack_tmp.pop()

            elif s[0] == "{" :
                stack.append("{")
                if isinstance(s, str) :
                    s = s[1:].strip()    #更新s并去除空格

            elif s[0] == "}" :
                #出栈到{，处理生成obj，将obj入栈
                if isinstance(s, str) :
                    s = s[1:].strip()    #更新s并去除空格
                tmp = stack.pop()
                while tmp != "{" :
                    stack_tmp.insert(0, tmp)
                    tmp = stack.pop()

                #logging.warning(stack_tmp)
                newest_obj = {}
                if len(stack_tmp) % 4 != 3 : #必须是key:value,key:value的样式
                    raise Exception #抛格式异常
                idx = 0
                while idx < len(stack_tmp) :
                    if idx % 4 == 0 :
                        newest_obj[stack_tmp[idx]] = stack_tmp[idx + 2]
                    elif idx % 4 == 1 :
                        if not self.check_colon(stack_tmp[idx]) :
                            raise Exception #抛格式异常
                    elif idx % 4 == 3 :
                        if not self.check_comma(stack_tmp[idx]) :
                            raise Exception #抛格式异常
                    idx += 1
                stack.append(newest_obj)
                while len(stack_tmp) > 0 :
                    stack_tmp.pop()

            elif s[0] == "," :
                stack.append(",")
                if isinstance(s, str) :
                    s = s[1:].strip()    #更新s并去除空格

            elif s[0] == ":" :
                stack.append(":")
                if isinstance(s, str) :
                    s = s[1:].strip()    #更新s并去除空格

            else :
                tmp_end_index = self.find_end_index(s)
                tmp_content = s[:tmp_end_index]
                if isinstance(tmp_content, str) :
                    tmp_content = tmp_content.strip()
                    #转义字符处理
                    tmp_content = tmp_content.replace("\\\"", "\"")
                    tmp_content = tmp_content.replace("\\\'", "\'")

                if isinstance(s, str) :
                    s = s[tmp_end_index:].strip()    #更新s并去除空格

                stack.append(self.change_form(tmp_content))
                #logging.warning(stack)

        if len(stack) != 1 : #如果最后stack中不是只有obj自己，那么说明格式错误
            #logging.warning(stack)
            raise Exception #抛格式异常
        self._data = stack[0]
        #打印转化后的_data对象
        #print("loads转化后的_data对象：" + str(self._data))

    def find_end_index(self, s) :
        index = 0
        while index < len(s) :
            if s[index] == "[" or s[index] == "]" or s[index] == "{" or s[index] == "}" \
                    or s[index] == "," or s[index] == ":" :
                break
            else :
                index += 1
        return index

    def check_comma(self, c) :
        if c == "," :
            return True
        else :
            return False

    def check_colon(self, c) :
        if c == ":" :
            return True
        else :
            return False

    def change_form(self, tmp_content) :
        if isinstance(tmp_content, str) :
            if len(tmp_content) >= 2 and tmp_content.startswith("\"") and tmp_content.endswith("\""):
                return tmp_content[1:-1]
            elif tmp_content == "true" :
                return True
            elif tmp_content == "false" :
                return False
            elif tmp_content == "null" :
                return None
            elif self.is_int(tmp_content) :
                return int(tmp_content)
            elif self.is_float(tmp_content) :
                return float(tmp_content)
            else :
                #抛出格式异常
                #logging.warning(tmp_content)
                return None

    def is_float(self, tmp_content) :
        try:
            float(tmp_content)
            return True
        except ValueError :
            return False

    def is_int(self, tmp_content) :
        try:
            int(tmp_content)
            return True
        except ValueError :
            return False


    #######################################################
    # dumps(self, obj)
    # 对象转Json字符串，返回Json字符串
    #######################################################
    def dumps(self, obj):
        #若对象是[]或者是()
        if isinstance(obj, list) or isinstance(obj, tuple):
            index = 0
            length = len(obj)
            tmpstr = ""
            while True:
                if index >= length :
                    break
                if index != 0 :
                    tmpstr += ","
                tmpstr += str(self.dumps(obj[index]))
                index += 1
            tmpstr = "["+tmpstr+"]"
            return tmpstr
        #若对象是None
        elif obj is None :
            return "null"
        #若对象是bool
        elif isinstance(obj, bool) :
            if obj :
                return "true"
            else :
                return "false"
        #若对象是int或float
        elif isinstance(obj, int) or isinstance(obj, float) :
            return str(obj)
        #若对象是str
        elif isinstance(obj, str) :
            #logging.warning(obj)
            #转义字符处理
            obj = obj.replace("\"", "\\\"")
            obj = obj.replace("\'", "\\\'")

            return "\"" + obj + "\""
        #若对象是{key : value, key : value}
        elif isinstance(obj, dict) :
            tmpstr = ""
            count = 0
            for key, value in obj.items() :
                tmpstr += str(self.dumps(key)) + ":" + str(self.dumps(value))
                count += 1
                if count < len(obj) :
                    tmpstr += ","
            tmpstr = "{" + tmpstr + "}"
            return tmpstr


    #######################################################
    # load_file(self, f)
    # 读取路径为f的文件中的Json串，返回一个对象
    #######################################################
    def load_file(self, f):
        try :
            file = open(f, 'r')
            fr = file.read()
            self._data = self.loads(fr)
        except IOError :
            print("找不到文件")
        except KeyboardInterrupt :
            print("你取消了读文件操作")
        finally :
            if file:
                file.close()



    #######################################################
    # dump_file(self, f)
    # 将_data转为Json串存入路径为f的文件
    #######################################################
    def dump_file(self,f):
        file = open(f, 'w')
        #logging.warning(self.dumps(self._data))
        file.write(self.dumps(self._data))
        file.close()


    #######################################################
    # load_dict(self, d)
    # 将字典d深拷贝到_data
    #######################################################
    def load_dict(self, d):
        if isinstance(d, dict) :
            self._data = {}
        else :
            return

        for key, value in d.items() :
            if isinstance(key, str):
                self._data[key] = self.deep_copy(value)

        #显示刚存入_data的字典
        print(self._data)

    def deep_copy(self, value):
        if isinstance(value, list):
            obj = []
            for tmp in value :
                obj.append(self.deep_copy(value))
        elif isinstance(value, dict):
            obj = {}
            for k, v in value.items() :
                if isinstance(k, str) :
                    obj[k] = self.deep_copy(v)
        else :
            obj = value

        return obj


    #######################################################
    # dump_dict(self)
    # 将_data的深拷贝返回
    #######################################################
    def dump_dict(self):

        if isinstance(self._data, dict) :
            d = {}
        else :
            return None
        for key, value in self._data.items() :
            if isinstance(key, str):
                d[key] = self.deep_copy(value)
        return d
