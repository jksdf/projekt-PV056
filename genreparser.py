#!/usr/bin/env python

import re
from commonstuff import *

_line = re.compile(r'^(?P<name>.*?)\((?P<year>[0-9?]{4}).*?\)' + '\t' + r'+(?P<genre>.*)$')

def parseFile(filename):
  file = open(filename)
  for i in range(383):
    file.readline()
  log('Parsing genres')
  movies = {}
  for linenumber, line in enumerate(file):
    line = line.decode('iso-8859-1')
    if linenumber % 100000 == 0:
      logSameLine("line {}".format(linenumber))
    match = _line.match(line)
    if match is not None and match.group('year') != '????':
      movie = match.group('name').strip(), int(match.group('year'))
      genre = match.group('genre').strip()
      if not movies.has_key(movie):
        movies[movie] = []
      movies[movie].append(genre)
  endLogSameLine()
  log('Parsing genres done')
  return movies
