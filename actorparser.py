#!/usr/bin/env python

import re
import json
import sys
import time
from commonstuff import *

movie = re.compile(r'(?P<name>("..*?")|([^"].*?))( +\((?P<year>[0-9?]{4}[^)]*)\))( +\(.*?\))*?(?P<episode> +\{.*\})?(?P<character> +\[.*\])?( +<(?P<credits>[0-9]*)>)?')
dir_regex = re.compile(r'^(?P<name>.*)\((?P<year>[0-9?]{4}).*?\)')

def addToMultimap(mp, key, value):
  if mp.has_key(key):
    mp[key].add(value)
  else:
    mp[key] = set([value])
  
def addMovie(mp, lastActor, parsed, credits_only):
  if not credits_only or parsed.group('credits') is not None:
    addToMultimap(mp, parsed.group('name').strip() + ' (' + (parsed.group('year')[:4] if parsed.group('year') is not None else '????') + ')', (lastActor, parsed.group('credits')))  

def addDirector(mp, director, parsed):
  addToMultimap(mp, parsed.group('name').strip() + ' (' + parsed.group('year') + ')', (director, 0))

def parseFile(results, filename, actors, credits_only):
  file = open(filename, 'r')
  for i in range(239 if actors else 241):
    file.readline()
  lastActor = None
  actorCount = 0
  log('Starting')
  for linenumber, line in enumerate(file):
    line = line.decode('iso-8859-1')
    if linenumber % 100000 == 0:
      logSameLine('line: {}\r'.format(linenumber))
    if len(line) == 0:
      pass
    elif line == u'-----------------------------------------------------------------------------\n':
      break
    else:
      parts = [i.strip() for i in line.split('\t') if i.strip() != '']
      if len(parts) == 1:
        parsed = movie.match(parts[0])
        if parsed is None:
          endLogSameLine()
          log('Error on |{}| {}'.format(line, linenumber))
        addMovie(results, lastActor, parsed, credits_only)
      elif len(parts) == 2:
        actorCount += 1
        lastActor = parts[0]
        parsed = movie.match(parts[1])
        if parsed is None:
          endLogSameLine()
          log('Error on {}'.format(line))
        addMovie(results, lastActor, parsed, credits_only)
  endLogSameLine()
  log('Finished with {} movies and {} actors'.format(len(results), actorCount))
  
def parseDirectors(results, filename):
  file = open(filename)
  for i in range(235):
    file.readline()
  director = None
  dir_count = 0
  for ln, line in enumerate(file):
    line = line.decode('iso-8859-1')
    if ln % 100000 == 0:
      logSameLine('line: {}\r'.format(ln))
    if len(line) == 0:
      pass
    elif line[:10] == u'-'*10:
      break
    else:
      parts = [i.strip() for i in line.split('\t') if i.strip() != '']
      if len(parts) == 1:
        parsed = dir_regex.match(parts[0])
      elif len(parts) == 2:
        dir_count += 1
        director = parts[0]
        parsed = dir_regex.match(parts[1])
      if parsed is None:
        endLogSameLine()
        log('Error on |{}| {}'.format(line, ln))
      else:
        addDirector(results, director, parsed)
  endLogSameLine()
  log("Finished with {} directors".format(dir_count))
  

def parseActors(actors, actresses, directors, credits_limit=None):
  results = {}
  log('Parsing actors')
  parseFile(results, actors, True, credits_limit is not None)
  log('Actors done.')
  log('Parsing actresses.')
  parseFile(results, actresses, False, credits_limit is not None)
  log('Actresses done')
  log('Parsing directors')
  parseDirectors(results, directors)
  log('directors done')
  if credits_limit is not None:
    results = {i: sorted(results[i], key=lambda x:int(x[1]))[:credits_limit] for i in results}
  return results
  
if __name__ == "__main__":
  if len(sys.argv) != 4:
    sys.stderr.write('First argument is input actors, second is inputs actresses, 3. is directors, 4. is output')
    exit(-1)
  
  f = open(sys.argv[3], 'w')
  f.write('{')
  actors = parseActors(sys.argv[1], sys.argv[2], sys.argv[3], 5)
  for index, val in enumerate(actors.keys()):
    if index != 0:
      f.write(',')
    f.write('\n')
    f.write(json.dumps(val))
    f.write(': ')
    f.write(json.dumps([i for i in actors[val]]))
  f.write('\n}')
    
  
