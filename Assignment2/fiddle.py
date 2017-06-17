import sys, re, hashlib, base64, binascii

m = re.compile("(a)n")

print m.search("A chance of success grows with each day of hard work").group(1)