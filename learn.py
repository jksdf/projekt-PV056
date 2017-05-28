#!/usr/bin/env python

import matplotlib.pyplot as plt
import json
from commonstuff import *
from sklearn.naive_bayes import GaussianNB
import sys
import numpy

def run(datafilename, testdataset, divisor=1):
  with open(datafilename) as file:
    data = json.load(file)
  with open(testdataset) as file:
    test = json.load(file)
  log('Working with data from date range {}  to {}'.format(data['fromYear'], data['toYear']))
  target = numpy.array(map(lambda x: int(round(x['target']/divisor)), data['data']))
  source = numpy.array(map(lambda x: numpy.array(x['attributes'], dtype = 'f'), data['data']))
  target = target.reshape(target.size,1).ravel()
  print str(target), type(target)
  bayes = GaussianNB()
  bayes.fit(source, target)
  y_pred = bayes.predict(numpy.array(map(lambda x: x['attributes'], test['data'])))
  test_target = numpy.array(map(lambda x: int(round(x['target'])), test['data']))
  dist = {i:0 for i in range(-10,10)}
  for i in test_target - y_pred:
    dist[i] += 1
  print "distances: {}\nabsolute distances: {}".format(dist, {i: (dist[i] + dist[-i]) if i != 0 else dist[i] for i in range(0,10)})
  dist = map(lambda x: x[1], sorted([(i,dist[i]) for i in dist]))
  plt.bar(range(-10,10), [float(i)/sum(dist) for i in dist])
  
  
  


if __name__ == "__main__":
  run(sys.argv[1], sys.argv[2])
  plt.grid()
  plt.show()
