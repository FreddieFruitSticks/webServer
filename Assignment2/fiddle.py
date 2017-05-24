import sys

def method(kwargs):
    dictionary={}
    dictionary.update(**kwargs)
    # print dictionary


method({'a':'a', 'b':'b'})