#!/usr/bin/env python

import matplotlib.pyplot as plt
import json
from commonstuff import *
from sklearn.naive_bayes import GaussianNB
import sys
import numpy

def run(datafilename, divisor=1):
  with open(datafilename) as file:
    data = json.load(file)
  log('Working with data from date range {}  to {}'.format(data['fromYear'], data['toYear']))
  target = numpy.array(map(lambda x: int(round(x['target']/divisor)), data['data']))
  source = numpy.array(map(lambda x: numpy.array(x['attributes'], dtype = 'f'), data['data']))
  target = target.reshape(target.size,1).ravel()
  print str(target), type(target)
  bayes = GaussianNB()
  bayes.fit(source, target)
  y_pred = bayes.predict(source)
  dist = [0 for i in range(21)]
  for i in target - y_pred:
    dist[i+10] += 1
  print "Number of mislabeled points out of a total {} points : {}".format(len(target), [dist[i+10] + dist[10-i] for i in range(0,10)])
  plt.plot([i-10 for i in range(21)], [float(i)/sum(dist) for i in dist])
  
  
  


if __name__ == "__main__":
  for i in sys.argv[1:]:
    run(i)
    run(i, divisor=3)
  plt.grid()
  plt.show()
