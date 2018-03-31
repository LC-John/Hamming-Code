# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 21:05:21 2018

@author: DrLC
"""

import math
import numpy

class Hamming:
    
    def __init__(self):
        
        self.__code = []
        self.__ori = []
        self.__init = True
        self.__code_len = 0
        self.__parity = 0
        
    def code2ori(self):
        
        err = self.check_code()
        if err is not None:
            if err < len(self.__code):
                self.__code[err] = 1 - self.__code[err]
            else:
                return
        self.__ori = []
        tmp_cnt = 1
        for i in range(len(self.__code)):
            if i == tmp_cnt - 1:
                tmp_cnt *= 2
                continue
            self.__ori.append(self.__code[i])
        
    def ori2code(self):
        
        self.__code = []
        tmp_flag = 1
        code_idx = 0
        ori_idx = 0
        while True:
            if ori_idx >= len(self.__ori):
                break
            if code_idx + 1 == tmp_flag:
                self.__code.append(2)
                tmp_flag *= 2
                code_idx += 1
            else:
                self.__code.append(self.__ori[ori_idx])
                ori_idx += 1
                code_idx += 1
        self.__code_len = int(math.log2(len(self.__code)))
        tmp_flag = 1
        while True:
            tmp = self.get_px_code(tmp_flag)
            if tmp is None:
                break
            if not (numpy.sum(tmp) + self.__parity) % 2 == 0:
                self.__code[2 ** (tmp_flag-1)-1] = 1
            else:
                self.__code[2 ** (tmp_flag-1)-1] = 0
            tmp_flag += 1
                    
        
            
    def get_px_code(self, x):
        
        px = []
        base = 2 ** x
        for i in range(len(self.__code)):
            if (i+1) % base < base / 2:
                px.append(2)
            else:
                px.append(self.__code[i])
        if numpy.sum(px) == 2 * len(px):
            return None
        return px
        
    def check_code(self):
        
        x = 1
        err = []
        while True:
            tmp = self.get_px_code(x)
            if tmp is None:
                break
            if not (numpy.sum(tmp) + self.__parity) % 2 == 0:
                err.append(x-1)
            x += 1
        if len(err) == 0:
            return None
        ret = 0
        for i in err:
            ret += 2 ** i
        return ret-1
        
    def __bytes2bits(self, string):
        
        tmp_code = []
        for b in string:
            if b == '0':
                tmp_code += [0, 0, 0, 0]
            elif b == '1':
                tmp_code += [0, 0, 0, 1]
            elif b == '2':
                tmp_code += [0, 0, 1, 0]
            elif b == '3':
                tmp_code += [0, 0, 1, 1]
            elif b == '4':
                tmp_code += [0, 1, 0, 0]
            elif b == '5':
                tmp_code += [0, 1, 0, 1]
            elif b == '6':
                tmp_code += [0, 1, 1, 0]
            elif b == '7':
                tmp_code += [0, 1, 1, 1]
            elif b == '8':
                tmp_code += [1, 0, 0, 0]
            elif b == '9':
                tmp_code += [1, 0, 0, 1]
            elif b == 'a' or b == 'A':
                tmp_code += [1, 0, 1, 0]
            elif b == 'b' or b == 'B':
                tmp_code += [1, 0, 1, 1]
            elif b == 'c' or b == 'C':
                tmp_code += [1, 1, 0, 0]
            elif b == 'd' or b == 'D':
                tmp_code += [1, 1, 0, 1]
            elif b == 'e' or b == 'E':
                tmp_code += [1, 1, 1, 0]
            elif b == 'f' or b == 'F':
                tmp_code += [1, 1, 1, 1]
            else:
                print ("\""+string+"\" is not a byte code sequence!")
                print ("Error! Abort!")
                return []
        return tmp_code
            
    def __bits2bits(self, bits):
        
        tmp_code = []
        for b in bits:
            if b == '0':
                tmp_code.append(0)
            elif b == '1':
                tmp_code.append(1)
            else:
                print ("\""+bits+"\" is not a bit code sequence!")
                print ("Error! Abort!")
                return []
        return tmp_code
        
    def set_code_bytes(self, string):
        
        tmp = self.__bytes2bits(string)
        if len(tmp) != 0:
            self.__code = tmp
            self.__ori = []
            self.__code_len = int(math.log2(len(self.__code)))
            self.__init = False
            return True
        return False
    
    def set_code_bits(self, string):
        
        tmp = self.__bits2bits(string)
        if len(tmp) != 0:
            self.__code = tmp
            self.__ori = []
            self.__code_len = int(math.log2(len(self.__code)))
            self.__init = False
            return True
        return False
        
    def set_ori_bytes(self, string):
        
        tmp = self.__bytes2bits(string)
        if len(tmp) != 0:
            self.__ori = tmp
            self.__code = []
            self.__init = False
            return True
        return False
    
    def set_ori_bits(self, string):
        
        tmp = self.__bits2bits(string)
        if len(tmp) != 0:
            self.__ori = tmp
            self.__code = []
            self.__init = False
            return True
        return False
            
    def set_parity(self, string):
        
        if string.lower() == "odd".lower():
            self.__parity = 1
        elif string.lower() == "even".lower():
            self.__parity = 0
        else:
            print ("\""+string+"\" is not supported!")
            print ("Use 'odd' or 'even' only.")
            return False
        return True
            
    def get_code(self):
        
        return self.__code

    def get_ori(self):
        
        return self.__ori
        
    def get_length(self):
        
        return self.__code_len
        
    def get_parity(self):
        
        if self.__parity == 0:
            return "even"
        else:
            return "odd"
        
if __name__ == "__main__":
    
    h = Hamming()
    h.set_code_bytes("8AC")
    h.code2ori()
    print (h.get_code())
    print (h.get_ori())
    h.ori2code()
    print (h.get_code())
    print (h.get_ori())