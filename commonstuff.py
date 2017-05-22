import sys
import time

def _log(x):
  return time.strftime("[%Y-%m-%d %H:%M:%S] ") + str(x)

def logSameLine(x):
  sys.stderr.write(_log(x) + '\r')

def endLogSameLine():
  sys.stderr.write('\n')

def log(x):
  sys.stderr.write(_log(x) + '\n')
