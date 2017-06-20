#!/usr/bin/env python

import json
import sys
import generategraph
from commonstuff import *
from generategraph import moviesMap, actorMap, getGraph, vertsMap

_genresList = "Short Drama Comedy Documentary Adult Thriller Action Romance Animation Family Horror Music Crime Adventure Fantasy Sci-Fi Mystery Biography History Sport".split(' ')[:15]

def avg(lst):
  return float(sum(lst))/len(lst)

def genreCounts(lst):
  mp = dict([(ge, idx) for idx, ge in enumerate(_genresList)])
  res = [0 for i in range(len(_genresList))]
  for i in lst:
    if mp.has_key(i):
      res[mp[i]] += 1
  return [float(i)/sum(res) for i in res] if sum(res) != 0 else None

toBtw = set()

def _runMovie(movie, fromYear, toYear, min_close=5, betweenness_cutoff=5):
  closeMovies = []
  for actor in moviesMap()[movie]['actors']:
    closeMovies += [i for i in actorMap()[actor] if i[1] in range(fromYear, toYear)]
  if len(closeMovies) < 5:
    return None
  closeVerts = [vertsMap()[i] for i in closeMovies]
  avgRating = avg([moviesMap()[other]['rating'] for other in closeMovies])
  avgDegree = avg(getGraph().degree(closeVerts))
  genres = genreCounts([i for other in closeMovies for i in moviesMap()[other]['genres']])
  thisGenres = genreCounts(moviesMap()[movie]['genres'])
  if genres is None or thisGenres is None:
    return None
  vid = getGraph().vcount()
  getGraph().add_vertices(1)
  getGraph().add_edges(set([(vid, i) for i in closeVerts]))
  thisDegree = getGraph().degree(vid)
  getGraph().delete_vertices(vid)
  btw = [getGraph().vs[i]['btw'] for i in closeVerts]
  return {"target": moviesMap()[movie]['rating'], "attributes":[avgRating, avgDegree, thisDegree] + genres + thisGenres + [avg(btw)]}

def prepareDataset(actors, actresses, directors, rankings, genres, fromYear=1995, toYear=2000):
  generategraph.generateAll(actors, actresses, directors, rankings, genres, fromYear=fromYear, toYear=toYear)
  dataset = []
  log("preparing dataset")
  for idx, movie in enumerate(generategraph.moviesMap()):
    if idx % 10000 == 0:
      logSameLine("{} movies prepared, {} dataset rows".format(idx, len(dataset)))
    if movie[1] == toYear:
      row = _runMovie(movie, fromYear, toYear)
      if row is not None:
        dataset.append(row)
  endLogSameLine()
  log("Dataset created")
  return dataset
      
if __name__ == "__main__":
  if len(sys.argv) == 1:
    sys.stderr.write('actors, actresses, directors, rankings, genres, fromYear, toYear')
  dataset = prepareDataset(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], fromYear=int(sys.argv[6]), toYear=int(sys.argv[7]))
  json.dump({"fromYear":fromYear, "toYear": toYear, "data":dataset}, sys.stdout)
