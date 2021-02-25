#!/usr/bin/env python

import sys
import hashlib

def encryuser(char):
    sumstr = ''
    newmd5 = ''
    md5 = hashlib.md5(char).hexdigest().upper()
    for i in md5:
        newmd5 += chr(ord(i) + 1)

    for j in char:
        sumstr += chr(ord(j) + 1)
    return sumstr + newmd5



def decodeuser(char):
    tmp = char[:-32]
    newmd5 = ''
    for i in tmp:
        newmd5 += chr(ord(i) - 1)
    return newmd5
    
if __name__ == '__main__' :

    t = encryuser('yanbo')
    print t
    print decodeuser(t)
