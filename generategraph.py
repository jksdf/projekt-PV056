#!/usr/bin/env python

import sys
import json
import igraph
import actorparser
import ratingparser
import genreparser
from commonstuff import *
from collections import defaultdict

_movies = None
_actors = None
_graph = None
_verts = None

def _genMovies(actorsfilename, actressesfilename, directorsfilename, rankingfilename, genresfilename, credits_limit, min_votes, no_short):
  global _movies
  global _actors
  if _movies is None:
    log("gen Movies triggered")
    genres = genreparser.parseFile(genresfilename)
    ratings = ratingparser.parseRankings(rankingfilename)
    movies = actorparser.parseActors(actorsfilename, actressesfilename, directorsfilename, credits_limit=credits_limit)
    _movies = {(i[:-7], int(i[-5:-1])): {"actors": movies[i]} for i in movies if '?' not in i[-5:-1]}
    for i in _movies:
      _movies[i]["rating"] = ratings[i][0] if ratings.has_key(i) else 0
      _movies[i]["votes"] = ratings[i][1] if ratings.has_key(i) else 0
      _movies[i]['genres'] = genres[i] if genres.has_key(i) else []
    for i in [i for i in _movies.keys()]:
      if _movies[i]['votes'] is None or _movies[i]['votes'] <= min_votes or len(_movies[i]['genres']) == 0 or (no_short and ("Short" in _movies[i]['genres'])): # TODO: more filtering, eg. genres
        del _movies[i]
    _actors = {}
    for movie in _movies:
      for actor in _movies[movie]['actors']:
        if not _actors.has_key(actor):
          _actors[actor] = []
        _actors[actor].append(movie)
    log("gen Movies done")

def moviesMap():
  global _movies
  return _movies

def actorMap():
  global _actors
  return _actors

def getGraph():
  global _graph
  return _graph

def vertsMap():
  global _verts
  return _verts

def generateAll(actorsfilename, actressfilename, directorsfilename, rankingfilename, genresfilename, fromYear=1990, toYear=2000, credits_limit=5, min_votes=10, no_short=True, btw_cutoff=10):
  _genMovies(actorsfilename, actressfilename, directorsfilename, rankingfilename, genresfilename, credits_limit, min_votes, no_short)
  _generateGraph(fromYear, toYear, credits_limit, min_votes, btw_cutoff)

def _generateGraph(fromYear, toYear, credits_limit, min_votes, btw_cutoff):
  global _graph
  global _verts
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
  log("Generating verts map")
  _verts = {movie[0]: idx for idx, movie in enumerate(movies)}
  log("Verts map done")
  log("Generating Graph")
  graph = igraph.Graph()
  log("Adding vertices")
  for idx, movie in enumerate(movies):
    graph.add_vertex(movie[0])
    graph.vs[idx]["properties"] = {"rating": _movies[movie[0]]['rating'], "votes": _movies[movie[0]]["votes"], "actors": movie[1], "genres":_movies[movie[0]]['genres']}
  log("Vertices added")
  mvCounter = 0
  edges = defaultdict(lambda: 0)
  for movie, actorsInMovie in movies:
    if mvCounter % 500 == 0:
      logSameLine("{} movies out of {} added".format(mvCounter, len(movies)))
    mvCounter+=1
    for actor in actorsInMovie:
      for othermovie in actors[actor]:
        if _verts[movie] != _verts[othermovie]:
          aidx, bidx = _verts[movie], _verts[othermovie]
          edges[(aidx, bidx)] += 1
  graph.add_edges(edges.keys())
  graph.es['weight'] = edges.values()
  endLogSameLine()
  _graph = graph
  log("All edges added")
  log("Generating betweenness with cutoff={}".format(btw_cutoff))
  btw = _graph.betweenness(cutoff=btw_cutoff)
  for idx, i in enumerate(btw):
    _graph.vs[idx]['btw'] = i
  log("Betweenness generated")



if __name__ == "__main__":
  if sys.platform == 'win32': # fix for stdout binary 
    import os, msvcrt
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
  if len(sys.argv) == 1:
    log("actors, actresses, directors, rankings, genres, fromYear, toYear")
    exit(-2)
  generateAll(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], fromYear=int(sys.argv[6]), toYear=int(sys.argv[7]))
  _graph.save(sys.stdout, format='pickle')
  
