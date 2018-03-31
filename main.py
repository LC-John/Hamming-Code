# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 16:40:51 2018

@author: DrLC
"""

from Hamming import Hamming
import numpy
import sys

global h

def encode(ori_byte, bytecode=True, evenparity=True):
    
    global h
    if bytecode:
        if not h.set_ori_bytes(ori_byte):
            return
    else:
        if not h.set_ori_bits(ori_byte):
            return
            
    if evenparity:
        h.set_parity("even")
    else:
        h.set_parity("odd")
        
    h.ori2code()
    
    tmp = h.get_code()
    print ("\nDec\t", end="")
    tmp_flag = 1
    for i in range(len(tmp)):
        if i + 1 == tmp_flag:
            tmp_flag *= 2
            print ("- ", end="")
        else:
            print (str(tmp[i])+" ", end="")
    print ("\n")
    tmp_flag = 1
    while True:
        tmp = h.get_px_code(tmp_flag)
        if tmp is None:
            break
        print ("P"+str(2**(tmp_flag-1))+"\t", end="")
        for i in tmp:
            if i == 2:
                print ("- ", end="")
            else:
                print (str(i)+" ", end="")
        print ("  Put "+str(tmp[2**(tmp_flag-1)-1]))
        tmp_flag += 1
    print ()
    tmp = h.get_code()
    print ("Enc\t", end="")
    for i in tmp:
        print (str(i)+" ", end="")
    print ()
    
def check(code_byte, bytecode=True, evenparity=True):
    
    global h
    if bytecode:
        if not h.set_code_bytes(code_byte):
            return
    else:
        if not h.set_code_bits(code_byte):
            return
            
    if evenparity:
        h.set_parity("even")
    else:
        h.set_parity("odd")
        
    err = h.check_code()
    if err is None:
        print ("\nCorrect Code!")
    elif err >= len(h.get_code()):
        print ("\nWrong parity!")
        if evenparity:
            print ("Should be odd parity checking.")
        else:
            print ("Should be even parity checking.")
        return -1111
    else:
        print ("\nWrong bit at "+str(err)+".")
        
    tmp = h.get_code()
    print ("\nEnc\t", end="")
    for i in tmp:
        print (str(i)+" ", end="")
    print ("\n")
    print ("WBit\t", end="")
    for i in range(len(tmp)):
        if i == err:
            print ("V ", end="")
        else:
            print ("  ", end="")
    print ()
    tmp_flag = 1
    if h.get_parity() == "even":
        tmp_p = 0
    else:
        tmp_p = 1
    while True:
        tmp = h.get_px_code(tmp_flag)
        if tmp is None:
            break
        print ("P"+str(2**(tmp_flag-1))+"\t", end="")
        for i in tmp:
            if i == 2:
                print ("- ", end="")
            else:
                print (str(i)+" ", end="")
        if (numpy.sum(tmp) + tmp_p) % 2 == 0:
            print ("  ")
        else:
            print ("  Wrong bit appear")
        tmp_flag += 1
    
def decode(code_byte, bytecode=True, evenparity=True):
    
    if check(code_byte, bytecode, evenparity) == -1111:
        return
    
    global h
    if bytecode:
        if not h.set_code_bytes(code_byte):
            return
    else:
        if not h.set_code_bits(code_byte):
            return
            
    if evenparity:
        h.set_parity("even")
    else:
        h.set_parity("odd")
        
    h.code2ori()
    
    tmp = h.get_code()
    print ("\nCorrect\t", end="")
    for i in tmp:
        print (str(i)+" ", end="")
    print ("\nDec\t", end="")
    tmp_flag = 1
    for i in range(len(tmp)):
        if i + 1 == tmp_flag:
            tmp_flag *= 2
            print ("- ", end="")
        else:
            print (str(tmp[i])+" ", end="")
    
def help():
    
    print ("----------------------------------------")
    print ("|                                      |")
    print ("|            Simple Hamming            |")
    print ("|                                      |")
    print ("|            by LC (or ZHZ)            |")
    print ("|             zhang_hz@pku.edu.cn      |")
    print ("|                                      |")
    print ("----------------------------------------")
    
    print ("\n")
    print ("Hi, this is LC! And this is a simple demo program to demonstrate Hamming code system. ", end="")
    print ("Encoding, decoding and checking over bit or byte sequences are supported. ")
    print ("\nYou can easily call it by typing  \"python main.py\". ", end="")
    print ("The first parameter is always needed. The choices are \"-C\" for checking, \"-E\" for encoding, \"-D\" for decoding. ", end="")
    print ("The second parameter is your bit/byte sequence. ", end="")
    print ("The third parameter indicates whether the sequence is a bit/byte sequence. \"-b\" stands for bit, and \"-B\" stands for byte. The default flag is \"-B\". ", end="")
    print ("The last parameter indicates whether the coding system is odd/even checking. \"-O\" stands for odd, and \"-E\" stands for even. The default flag is \"-E\". ")
    
    print ("\nAn example is shown as below.\n")
    print ("> python main.py -D AAC -B -E\n")
    print ("Wrong bit at 2.\n")
    print ("Enc     1 0 1 0 1 0 1 0 1 1 0 0 \n")
    print ("WBit        V      ")             
    print ("P1      1 - 1 - 1 - 1 - 1 - 0 -   Wrong bit appear")
    print ("P2      - 0 1 - - 0 1 - - 1 0 -   Wrong bit appear")
    print ("P4      - - - 0 1 0 1 - - - - 0   ")
    print ("P8      - - - - - - - 0 1 1 0 0   \n")
    print ("Correct 1 0 0 0 1 0 1 0 1 1 0 0 ")
    print ("Dec     - - 0 - 1 0 1 - 1 1 0 0 ")
        
def main():
    
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        help()
        return
    
    byte = True
    byte_flag = False
    even = True
    even_flag = False
    if len(sys.argv) >= 4:
        if sys.argv[3] == "-B":
            byte = True
            byte_flag = True
        elif sys.argv[3] == '-b':
            byte = False
            byte_flag = True
        elif sys.argv[3] == '-E':
            even = True
            even_flag = True
        elif sys.argv[3] == '-O':
            even = False
            even_flag = True
        else:
            print ("Unknown flag: "+sys.argv[3])
            return
    if len(sys.argv) >= 5:
        if sys.argv[4] == "-B":
            if byte_flag:
                print ("Duplicated flag: "+sys.argv[3]+" & "+sys.argv[4])
                return
            byte = True
        elif sys.argv[4] == '-b':
            byte = False
            if byte_flag:
                print ("Duplicated flag: "+sys.argv[3]+" & "+sys.argv[4])
                return
        elif sys.argv[4] == '-E':
            even = True
            if even_flag:
                print ("Duplicated flag: "+sys.argv[3]+" & "+sys.argv[4])
                return
        elif sys.argv[4] == '-O':
            even = False
            if even_flag:
                print ("Duplicated flag: "+sys.argv[3]+" & "+sys.argv[4])
                return
        else:
            print ("Unknown flag: "+sys.argv[4])
            return
        
    global h
    h = Hamming()
    
    if sys.argv[1] == '-D':
        decode(sys.argv[2], byte, even)
    elif sys.argv[1] == "-E":
        encode(sys.argv[2], byte, even)
    elif sys.argv[1] == '-C':
        check(sys.argv[2], byte, even)
    else:
        print ("Unknown function selection: "+sys.argv[1])
        return
    
if __name__ == "__main__":
    
    main()