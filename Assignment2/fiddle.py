import sys, re
pattern = re.compile('^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$')
isB64 = pattern.match("AQIDBAUGBwgJCgsMDQ4PEC==")
print isB64