'''
for each set of experimental results, calculate response time and stabilization time per operation, also average

response time = time when done - time when registered

stabilization time = 
for each op:
  if needs total order:
    time when last conflict logged - time when logged at origin

'''
import os
import json
from datetime import datetime, timedelta

replicas = ['paris','bangalore','newyork']

def parse_client_logs(exp, conflict):
  # for one experiment, populate the following data
  # data = {ts : [requested_time, response time]}
  data = {}
  directory = 'data'+str(conflict)+'_'+str(exp)
  for r in replicas:
    reg_file = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', directory, r, 'register.txt')
    with open(reg_file, 'r') as l:
      lines = l.readlines()
      for each in lines:
        j = json.loads(each)
        if j["ts"][0] > 395 or (j["ts"][0] == 395 and (j["ts"][1] > 0 or j["ts"][2] > 0)): # filter out initial warm up load
          key = str(j["ts"])
          if not key in data:
            data[key] = {} 
          data[key]["requested_time"] = datetime.strptime(j["time"], '%Y-%m-%d %H:%M:%S.%f')
    reg_file = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', directory, r, 'done.txt')
    with open(reg_file) as l:
      lines = l.readlines()
      for each in lines:
        j = json.loads(each)
        if j["ts"][0] > 395 or (j["ts"][0] == 395 and (j["ts"][1] > 0 or j["ts"][2] > 0)): # filter out initial warm up load
          key = str(j["ts"])
          if not key in data:
            data[key] = {} 
          data[key]["acknowledged"] = datetime.strptime(j["time"], '%Y-%m-%d %H:%M:%S.%f')
  assert len(data) == 150
  return data


def response_time(data):
  # responses = {}
  total = 0
  responses = [data[ts]["acknowledged"] - data[ts]["requested_time"] for ts in data.keys()]
  assert len(responses) == 150
  average_response_time = sum(responses, timedelta(0)) / len(responses)
  return responses, average_response_time

# def parse_replica_logs(exp, conflict):
#   pass

# def stabilization_time():
#   stabilizations = {}
#   total = 0
#   for ts, time in data:
#     if ts[0] > 395: # filter out initial warm up load
#       stabilized_time = get_next_causally_stable_time(ts)


def result():
  # return average response time, per experiment
  for i in range(0,1):
    for j in range(0,30, 10):
      data = parse_client_logs(i, j)
      print(response_time(data)[1])
  # return  average stabilization time per experiment
  # for i in range(0,1):
  #   for j in range(0,30, 10):
  #     data = parse_replica_logs(i, j)
  #     print(stabilization_time(data)[1])

result()