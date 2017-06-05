#!/usr/bin/env python

import matplotlib.pyplot as plt
import json
from commonstuff import *
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import mean_squared_error, accuracy_score, roc_curve
from sklearn.preprocessing import normalize
import sys
import numpy

def run(datafn, testfn):
  data = test = None
  with open(datafn) as file:
    data = json.load(file)
  with open(testfn) as file:
    test = json.load(file)
  log('Working with data from date range {}  to {}'.format(data['fromYear'], data['toYear']))
  target = numpy.array(map(lambda x: int(round(x['target'])), data['data']))
  source = numpy.array(map(lambda x: numpy.array(x['attributes'], dtype = 'f'), data['data']))
  sourceNorm = normalize(source, axis=0)
  target = target.reshape(target.size,1).ravel()
  test_target = numpy.array(map(lambda x: int(round(x['target'])), test['data']))
  test_target = test_target.reshape(test_target.size,1).ravel()
  print "BAYES"
  bayesfn(target, source, test_target, test['data'])
  print "SVM"
  linSVM(target, sourceNorm, test_target, test['data'])

def applyLearning(target, source, test_target, test_data, model, norm=False):
  model.fit(source, target)
  testY = numpy.array(map(lambda x: x['attributes'], test_data))
  if norm:
    testY = normalize(testY,axis=0)
  y_pred = model.predict(testY)
  dist = {i:0 for i in range(-10,11)}
  for i in test_target - y_pred:
    dist[i] += 1
  print "distances: {}\nabsolute distances: {}\nacc: {}\nmean sq err:{}".format(dist, {i: (dist[i] + dist[-i]) if i != 0 else dist[i] for i in range(0,10)}, accuracy_score(test_target, y_pred), mean_squared_error(test_target, y_pred))
  dist = map(lambda x: x[1], sorted([(i,dist[i]) for i in dist]))
  plt.bar(range(-10,11), [float(i)/sum(dist) for i in dist])
  plt.grid()
  plt.show()

def linSVM(target, source, test_target, test_data):
  for i in "linear poly rbf sigmoid".split(' '):
    print "SVM", i
    applyLearning(target, source, test_target, test_data, SVC(kernel=i, max_iter=100000), norm=True)
  

def bayesfn(target, source, test_target, test_data):
  applyLearning(target, source, test_target, test_data, GaussianNB())
  
  


if __name__ == "__main__":
  run(sys.argv[1], sys.argv[2])
