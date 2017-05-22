#!/usr/bin/env python

import re
from commonstuff import *

regex = re.compile(r'^(?P<name>.*)\((?P<year>([0-9?]{4}).*?\)')

def parseFile(filename):
  file = open(filename)
  for i in range(256):
    file.readline()
  directorname = None
  result = {}
  for ln, line, in enumerate(file): 
    line = line.decode('iso-8859-1')
    if ln % 100000 == 0:
      logSameLine('line: {}\r'.format(ln))
    if len(line) == 0:
      pass
    elif line[:2] == u'--':
      break
    else:
      parts = [i.strip() for i in line.split('\t') if i.strip() != '']
      if len(parts) == 1:
        match = regex.match(parts[0])
        
