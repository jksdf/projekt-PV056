#!/usr/bin/env python

import sys
import igraph
import actorparser
import ratingparser
import genreparser
from commonstuff import *
from collections import defaultdict
import json
from apyori import apriori

_movies = None
_actors = None

def _genMovies(actorsfilename, actressesfilename, directorsfilename, rankingfilename, genresfilename, credits_limit, min_votes, no_short):
  global _movies
  global _actors
  if _movies is None:
    log("gen Movies triggered")
    genres = genreparser.parseFile(genresfilename)
    ratings = ratingparser.parseRankings(rankingfilename)
    movies = actorparser.parseActors(actorsfilename, actressesfilename, directorsfilename, credits_limit=credits_limit)
    _movies = {(i[:-7], int(i[-5:-1])): {"actors": movies[i]} for i in movies if '?' not in i[-5:-1]}
    log('Filling values')
    for i in _movies:
      _movies[i]["rating"] = ratings[i][0] if ratings.has_key(i) else 0
      _movies[i]["votes"] = ratings[i][1] if ratings.has_key(i) else 0
      _movies[i]['genres'] = genres[i] if genres.has_key(i) else []
    log('Values filled')
    log('Filtering')
    for i in [i for i in _movies.keys()]:
      if _movies[i]['votes'] is None or _movies[i]['votes'] <= min_votes or len(_movies[i]['genres']) == 0 or (no_short and ("Short" in _movies[i]['genres'])): # TODO: more filtering, eg. genres
        del _movies[i]
    log('Done filterng')
    _actors = {}
    for movie in _movies:
      for actor in _movies[movie]['actors']:
        if not _actors.has_key(actor):
          _actors[actor] = []
        _actors[actor].append(movie)
    log("gen Movies done")


def generateDataset(actorsfilename, actressfilename, directorsfilename, rankingfilename, genresfilename, fromYear=1990, toYear=2000, credits_limit=5, min_votes=10, no_short=True, btw_cutoff=10):
  _genMovies(actorsfilename, actressfilename, directorsfilename, rankingfilename, genresfilename, credits_limit, min_votes, no_short)
  global _movies
  log("Filtering movies in the year range {} to {}".format(fromYear, toYear))
  movies = [(movie, _movies[movie]['actors']) for movie in _movies if movie[1] in range(fromYear, toYear)]
  log("Filtering done")
  log("Generating actors")
  actors = {}
  for movie, actorsInMovie in movies:
    for actor in actorsInMovie:
      if not actors.has_key(actor):
        actors[actor] = []
      actors[actor].append(movie)
  log("Actors done")
  log("Generating dataset")
  mvCounter = 0
  dataset = []
  for movie, actorsInMovie in movies:
    if mvCounter % 500 == 0:
      logSameLine("{} movies out of {} loaded".format(mvCounter, len(movies)))
    mvCounter+=1
    closeMovies = set()
    for actor in actorsInMovie:
      for othermovie in actors[actor]:
        if movie != othermovie:
          closeMovies.add(othermovie)
    this_genres = map(lambda x: x+'1', _movies[movie]['genres'])
    for i in closeMovies:
      dataset.append(this_genres + map(lambda x:x+'2',_movies[i]['genres']))
  endLogSameLine()
  log("All edges added")
  return dataset



if __name__ == "__main__":
  if len(sys.argv) == 1:
    print "actors, actresses, directors, rankings, genres, fromYear, toYear"
    exit(-2)
  dataset = generateDataset(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], fromYear=int(sys.argv[6]), toYear=int(sys.argv[7]))
  res2 = set(((tuple(sorted(i.items)), i.support) for i in apriori(dataset, min_support=0.001) if any(map(lambda x: '1' in x, i.items)) and any(map(lambda x: '2' in x, i.items)) ))
  res = set()
  for i in res2:
    if tuple(sorted(map(lambda x: x.replace('1','9').replace('2','1').replace('9', '2'), i[0]))) not in res:
      res.add(i)
  print '['
  for idx, i in enumerate(res2):
    if idx != 0:
      print ',',
    print json.dumps({'items':list(i[0]),'support':i[1]})
  print ']'
