#!/usr/bin/env python

import json
import sys
import generategraph
from commonstuff import *
import actorparser
import ratingparser
import genreparser
import igraph

def nameConvert(x):
  return u'{} ({})'.format(x[0], x[1])

def prepareDataset(actors, actresses, directors, rankings, genres, graph):
  log('actors')
  actors = actorparser.parseActors(actors, actresses, directors, credits_limit=5)
  log('genres')
  genres = genreparser.parseFile(genres)
  log('graph')
  graph = igraph.Graph.Load(open(graph), format='pickle')
  for v in graph.vs:
    v['properties']['btw'] = v['btw']
  del graph.vs['btw']
  mov2data = {}
  for v in graph.vs:
    name = nameConvert(v['name'])
    mov2data[name] = v['properties']
    mov2data[name]['year'] = v['name'][1]
  for movie in actors:
    if mov2data.has_key(movie):
      mov2data[movie]['actors'] = actors[movie]
  for movie in genres:
    name = nameConvert(v['name'])
    if mov2data.has_key(name):
      mov2data[name]['genres'] = genres[movie]
  return mov2data
      
if __name__ == "__main__":
  if len(sys.argv) == 1:
    log('actors, actersses, directors, ratings, genres, graph')
    exit(1)
  dataset = prepareDataset(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
  log('saving')
  json.dump({"data":dataset}, sys.stdout)
