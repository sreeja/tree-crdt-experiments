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

def parse_client_logs(lc_config, exp, conflict):
  data = {}
  directory = 'data'+str(conflict)+'_'+str(exp)
  for r in replicas:
    reg_file = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'lc'+str(lc_config), directory, r, 'register.txt')
    with open(reg_file, 'r') as l:
      lines = l.readlines()
      for each in lines:
        j = json.loads(each)
        if j["ts"][0] > 395 or (j["ts"][0] == 395 and (j["ts"][1] > 0 or j["ts"][2] > 0)): # filter out initial warm up load
          key = str(j["ts"])
          if not key in data:
            data[key] = {} 
          data[key]["requested_time"] = datetime.strptime(j["time"], '%Y-%m-%d %H:%M:%S.%f')
    reg_file = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'lc'+str(lc_config), directory, r, 'done.txt')
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
  total = 0
  responses = [data[ts]["acknowledged"] - data[ts]["requested_time"] for ts in data.keys()]
  assert len(responses) == 150
  average_response_time = sum(responses, timedelta(0)) / len(responses)
  return responses, average_response_time

def parse_replica_logs(lc_config, exp, conflict):
  data = {}
  directory = 'data'+str(conflict)+'_'+str(exp)
  for r in replicas:
    for r1 in replicas:
      file_name = 'time'+r1+'.txt'
      reg_file = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'lc'+str(lc_config), directory, r, file_name)
      with open(reg_file, 'r') as l:
        lines = l.readlines()
        for each in lines:
          j = json.loads(each)
          if j["ts"][0] > 395 or (j["ts"][0] == 395 and (j["ts"][1] > 0 or j["ts"][2] > 0)): # filter out initial warm up load
            key = str(j["ts"])
            if not key in data:
              data[key] = {} 
            data[key][r] = datetime.strptime(j["time"], '%Y-%m-%d %H:%M:%S.%f')
            data[key]["ts"] = j["ts"]
  for r in replicas:
    file_name = r+'.txt'
    reg_file = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'lc'+str(lc_config), directory, 'paris', file_name)
    with open(reg_file, 'r') as l:
      lines = l.readlines()
      for each in lines:
        j = json.loads(each)
        if j["ts"][0] > 395 or (j["ts"][0] == 395 and (j["ts"][1] > 0 or j["ts"][2] > 0)): # filter out initial warm up load
          key = str(j["ts"])
          data[key]["op"] = {"name":j["op"], "n":j["args"]["n"], "ca":j["ca"]}
          data[key]["origin"] = j["replica"]
  return data

def is_concurrent(ts1, ts2):
  if ts1[0] >= ts2[0] and ts1[1] >= ts2[1] and ts1[2] >= ts2[2]:
    return False
  if ts1[0] <= ts2[0] and ts1[1] <= ts2[1] and ts1[2] <= ts2[2]:
    return False
  return True

def is_conflicting(exp, op1, op2):
  if exp ==0: #crdt, only concurrent moves on critical ancestors conflict
    if op1["name"] == "downmove": #possible conflict
      if op2["name"] in ["upmove", "downmove"]:
        if op1["n"] in op2["ca"] or op2["n"] in op1["ca"]:
          return True
    elif op2["name"] == "downmove": #possible conflict
      if op1["name"] in ["upmove", "downmove"]:
        if op1["n"] in op2["ca"] or op2["n"] in op1["ca"]:
          return True
    return False
  elif exp ==1: # opsets, all concurrent moves
    return True
  else: # 
    return False

def get_conflicting_conc_ops(entry, data, exp):
  conflicts = {}
  for each in data:
    if is_concurrent(entry["ts"], data[each]["ts"]) and is_conflicting(exp, entry["op"], data[each]["op"]):
      conflicts[each] = data[each]
  return conflicts

def stabilization_time(exp, data):
  stabilizations = []
  total = 0
  for each in data:
    stabilized_time = 0
    origin = data[each]["origin"]
    conflicts = get_conflicting_conc_ops(data[each], data, exp)
    if conflicts:
      last_conflict_time = max([conflicts[x][origin] for x in conflicts])
      stabilizations += [last_conflict_time - data[each][origin]]
    else:
      stabilizations += [timedelta(0)]
  average_stabilization_time = sum(stabilizations, timedelta(0)) / len(stabilizations)
  return stabilizations, average_stabilization_time


def result(lc_config):
  # return average response time, per experiment
  print("Response time")
  print("=============")
  for i in range(0,4):
    print("Experiment " + str(i))
    for j in range(0,30, 10):
      # print("Conflict %: " + str(j))
      data = parse_client_logs(lc_config, i, j)
      print("Conflict %: " + str(j) + " : " + str(response_time(data)[1]))
  print("=============")
  # return  average stabilization time per experiment
  print("Stabilization time")
  print("=============")
  for i in range(0,4):
    print("Experiment " + str(i))
    for j in range(0,30, 10):
      # print("Conflict %: " + str(j))
      data = parse_replica_logs(lc_config, i, j)
      print("Conflict %: " + str(j) + " : " + str(stabilization_time(i, data)[1]))
  print("=============")

for i in range(1,4):
  print("LATENCY CONFIG " + str(i) + " \n")
  result(i)