import sys, re, hashlib, base64, binascii


# print len("this is a string that is over 125 chars in length. Well maybe that is not true at this point but it sure is greater than 125 chars at this point.")
# print '\x01' & 127
# e = enumerate(['\x03'])
# print chr(ord('\x03') ^ ord('\xe8'))
# for index, char in e:
#     print index, chr(ord(char) ^ ord('\xe8'))

message = [chr(ord(byte) ^ ord('\x10')) for index, byte in enumerate(['\x03'])]
for indx, byte in enumerate(['\x03']):
    print ord(byte) ^ ord('\x10')

print message
