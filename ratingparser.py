#!/usr/bin/env python

import re
import json
import sys
from commonstuff import *
import time

movie = re.compile(r'^ +(?P<distribution>[0-9.*]{10}) +(?P<votes>[0-9]+) +(?P<rank>[0-9.]+) +(?P<name>("..*?")|(..*?)) +(?P<year>\([0-9?]{4}.*?\))(?P<episode> +\{.*\})?')

def parseRankings(filename):
  file = open(filename)
  for i in range(296):
    file.readline()
  result = {}
  movieCount = 0
  log('Rating parsing start')
  for linenumber, line in enumerate(file):
    line = line.decode('iso-8859-1')
    if linenumber % 100000 == 0:
      logSameLine('line: {}\r'.format(linenumber))
    if len(line) < 2:
      continue
    elif line[:2] == u'--':
      break
    else:
      parsed = movie.match(line)
      if parsed.group('year') is not None and parsed.group('year')[1:5] != '????':
        result[(parsed.group('name').strip(), int(parsed.group('year')[1:5]))] = (float(parsed.group('rank')), int(parsed.group('votes')))
  log('Finished with {} movies'.format(len(result)))
  return result
  
if __name__ == "__main__":
  if len(sys.argv) != 3:
    sys.stderr.write('First argument is input rankings, second is output')
    exit(-1)
  f = open(sys.argv[2], 'w')
  f.write('{')
  parsed = parseFile(sys.argv[1])
  for index, val in enumerate(parsed.keys()):
    if index != 0:
      f.write(',')
    f.write('\n')
    f.write(json.dumps(val))
    f.write(': ')
    f.write(json.dumps([i for i in actors[val]]))
  f.write('\n}')
    
  
