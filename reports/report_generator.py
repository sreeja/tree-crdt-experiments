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

experiments = ['CRDT Tree', 'Opsets based tree', 'Tree with global lock', 'Tree with subtree locks']

def parse_logs(lc_config, exp, conflict):
  data = {}
  for r in replicas:
    reg_file = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'lc'+str(lc_config), 'data'+str(conflict), str(exp), r, 'register.txt')
    with open(reg_file, 'r') as l:
      lines = l.readlines()
      for each in lines:
        j = json.loads(each)
        if j["ts"][0] > 352 or j["ts"][1] > 352 or j["ts"][2] > 352: # filter out initial warm up load
          key = str(j["ts"])
          if not key in data:
            data[key] = {} 
          try:
            data[key]["requested_time"] = datetime.strptime(j["time"], '%Y-%m-%d %H:%M:%S.%f')
          except:
            data[key]["requested_time"] = datetime.strptime(j["time"], '%Y-%m-%d %H:%M:%S')
    reg_file = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'lc'+str(lc_config), 'data'+str(conflict), str(exp), r, 'done.txt')
    with open(reg_file) as l:
      lines = l.readlines()
      for each in lines:
        j = json.loads(each)
        if j["ts"][0] > 352 or j["ts"][1] > 352 or j["ts"][2] > 352: # filter out initial warm up load
          key = str(j["ts"])
          if not key in data:
            data[key] = {} 
          try:
            data[key]["acknowledged"] = datetime.strptime(j["time"], '%Y-%m-%d %H:%M:%S.%f')
          except:
            data[key]["acknowledged"] = datetime.strptime(j["time"], '%Y-%m-%d %H:%M:%S')
    for r1 in replicas:
      file_name = 'time'+r1+'.txt'
      reg_file = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'lc'+str(lc_config), 'data'+str(conflict), str(exp), r, file_name)
      with open(reg_file, 'r') as l:
        lines = l.readlines()
        for each in lines:
          j = json.loads(each)
          if j["ts"][0] > 352 or j["ts"][1] > 352 or j["ts"][2] > 352: # filter out initial warm up load
            key = str(j["ts"])
            if not key in data:
              data[key] = {} 
            try:
              data[key][r] = datetime.strptime(j["time"], '%Y-%m-%d %H:%M:%S.%f')
            except:
              data[key][r] = datetime.strptime(j["time"], '%Y-%m-%d %H:%M:%S')
            data[key]["ts"] = j["ts"]
  skipmove_count = 0
  for r in replicas:
    file_name = r+'.txt'
    reg_file = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'lc'+str(lc_config), 'data'+str(conflict), str(exp), 'paris', file_name)
    with open(reg_file, 'r') as l:
      lines = l.readlines()
      for each in lines:
        j = json.loads(each)
        if j["ts"][0] > 352 or j["ts"][1] > 352 or j["ts"][2] > 352: # filter out initial warm up load
          key = str(j["ts"])
          if not("skip" in j["op"]):
            data[key]["op"] = {"name":j["op"], "n":j["args"]["n"], "ca":j["ca"]}
          else:
            if j["op"] in ["addskip", "removeskip"]:
              print("issue: " + j)
            else:
              skipmove_count += 1
            data[key]["op"] = {"name":j["op"], "n":None, "ca":None}
          data[key]["origin"] = j["replica"]
  # print([data[x]["ts"][0] for x in data.keys()])
  for each in range(353,653):
    assert(each in [data[x]["ts"][0] for x in data.keys()])
    assert(each in [data[x]["ts"][1] for x in data.keys()])
    assert(each in [data[x]["ts"][2] for x in data.keys()])
  # print(data.keys(), len(data))
  assert len(data) == 900
  # print ("skipmoves : " + str(skipmove_count))
  return data

def parse_replica_logs(lc_config, exp, conflict):
  data = {}
  for r in replicas:
    for r1 in replicas:
      file_name = 'time'+r1+'.txt'
      reg_file = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'lc'+str(lc_config), 'data'+str(conflict), str(exp), r, file_name)
      with open(reg_file, 'r') as l:
        lines = l.readlines()
        for each in lines:
          j = json.loads(each)
          if j["ts"][0] > 352 or j["ts"][1] > 352 or j["ts"][2] > 352: # filter out initial warm up load
            key = str(j["ts"])
            if not key in data:
              data[key] = {} 
            try:
              data[key][r] = datetime.strptime(j["time"], '%Y-%m-%d %H:%M:%S.%f')
            except:
              data[key][r] = datetime.strptime(j["time"], '%Y-%m-%d %H:%M:%S')
            data[key]["ts"] = j["ts"]
  for r in replicas:
    file_name = r+'.txt'
    reg_file = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'lc'+str(lc_config), 'data'+str(conflict), str(exp), 'paris', file_name)
    with open(reg_file, 'r') as l:
      lines = l.readlines()
      for each in lines:
        j = json.loads(each)
        if j["ts"][0] > 352 or j["ts"][1] > 352 or j["ts"][2] > 352: # filter out initial warm up load
          key = str(j["ts"])
          if not("skip" in j["op"]):
            data[key]["op"] = {"name":j["op"], "n":j["args"]["n"], "ca":j["ca"]}
          else:
            data[key]["op"] = {"name":j["op"], "n":None, "ca":None}          
          data[key]["origin"] = j["replica"]
  return data


def response_time(data):
  total = 0
  responses = [data[ts]["acknowledged"] - data[ts]["requested_time"] for ts in data.keys()]
  assert len(responses) == 900
  average_response_time = sum(responses, timedelta(0)) / len(responses)
  # print([data[ts]["op"]["name"] for ts in data.keys()])
  conflict_responses = [data[ts]["acknowledged"] - data[ts]["requested_time"] for ts in data.keys() if data[ts]["op"]["name"] in ["upmove", "downmove", "move", "moveskip"]]
  average_conflict_response_time = sum(conflict_responses, timedelta(0)) / len(conflict_responses)
  nonconflict_responses = [data[ts]["acknowledged"] - data[ts]["requested_time"] for ts in data.keys() if not(data[ts]["op"]["name"] in ["upmove", "downmove", "move", "moveskip"])]
  average_nonconflict_response_time = sum(nonconflict_responses, timedelta(0)) / len(nonconflict_responses)
  return [(ts, data[ts]["op"]["name"], (data[ts]["acknowledged"] - data[ts]["requested_time"]).total_seconds()*1000) for ts in data.keys()], average_response_time, average_conflict_response_time, average_nonconflict_response_time

def is_concurrent(ts1, ts2):
  if ts1[0] >= ts2[0] and ts1[1] >= ts2[1] and ts1[2] >= ts2[2]:
    return False
  if ts1[0] <= ts2[0] and ts1[1] <= ts2[1] and ts1[2] <= ts2[2]:
    return False
  return True

def is_conflicting(exp, op1, op2):
  if exp ==0: #crdt, only concurrent moves on critical ancestors conflict
    if op1["name"] in ["downmove", "upmove", "move", "moveskip"]: #possible conflict
      # if op2["name"] in ["upmove", "downmove"]:
      #   if op1["n"] in op2["ca"] or op2["n"] in op1["ca"]:
      return True
    # elif op2["name"] == "downmove": #possible conflict
    #   if op1["name"] in ["upmove", "downmove"]:
    #     if op1["n"] in op2["ca"] or op2["n"] in op1["ca"]:
    #       return True
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
  stabilizations_moves = []
  stabilizations_nonmoves = []

  stabs = []

  total = 0
  for each in data:
    stabilized_time = 0
    origin = data[each]["origin"]
    conflicts = get_conflicting_conc_ops(data[each], data, exp)
    if conflicts:
      last_conflict_time = max([conflicts[x][origin] for x in conflicts])
      st = last_conflict_time - data[each][origin]
      stabilizations += [st]
    else:
      st = timedelta(0)
      stabilizations += [st]
    # print(data[each], st.total_seconds()*1000)
    if data[each]["op"]["name"] in ["upmove", "downmove", "move", "moveskip"]:
      stabilizations_moves += [st]
    else:
      stabilizations_nonmoves += [st]
    stabs += [(each, data[each]["op"]["name"], st)]
  average_stabilization_time = sum(stabilizations, timedelta(0)) / len(stabilizations)
  average_stabilization_time_moves = sum(stabilizations_moves, timedelta(0)) / len(stabilizations_moves)
  average_stabilization_time_nonmoves = sum(stabilizations_nonmoves, timedelta(0)) / len(stabilizations_nonmoves)
  return stabs, average_stabilization_time, average_stabilization_time_moves, average_stabilization_time_nonmoves


def result(lc_config):
  # latex output
  # return average response time, per experiment
  print("Response time")
  print("=============")
  rl = []
  for j in [0, 2, 10, 20]:
    print("Conflict %: " + str(j) + " : ")
    row = []
    for i in [0, 1, 2, 3]:
      # print("Experiment " + str(i))
      # print("Conflict %: " + str(j))
      data = parse_logs(lc_config, i, j)
      rt = response_time(data)
      print(experiments[i] + " All: " + str(rt[1].total_seconds()*1000) + " :: Moves: " + str(rt[2].total_seconds()*1000) + " :: Nonmoves: " + str(rt[3].total_seconds()*1000))
      row += [experiments[i] + ' & ' +str(rt[1].total_seconds()*1000) + ' & ' +str(rt[2].total_seconds()*1000) + ' & ' + str(rt[3].total_seconds()*1000) + '\\\\']
      file_name = "response"+str(lc_config)+"con"+str(j)+"exp"+str(i)+".json"
      with open(file_name, "w") as f:
        f.write("\n".join([str(r) for r in rt[0]]))
    # rl += [row]
    file_name = "response"+str(lc_config)+"con"+str(j)+".tex"
    with open(file_name, "w") as f:
      f.write("\n".join(row))
  print("=============")
  # return  average stabilization time per experiment
  print("Stabilization time")
  print("=============")
  sl = []
  for i in [0, 1, 2, 3]:
    print(experiments[i])
    row = []
    for j in [0, 2, 10, 20]:
      # print("Conflict %: " + str(j))
      data = parse_replica_logs(lc_config, i, j)
      res = stabilization_time(i, data)
      print("Conflict %: " + str(j) + " : " + "All: " + str(res[1].total_seconds()*1000) + " moves: " + str(res[2].total_seconds()*1000) + " other operations: " + str(res[3].total_seconds()*1000))
      row += [str(stabilization_time(i, data)[1].total_seconds()*1000)]
      file_name = "stab"+str(lc_config)+"con"+str(j)+"exp"+str(i)+".json"
      with open(file_name, "w") as f:
        f.write("\n".join([str(s) for s in res[0]]))
    sl += [experiments[i] + " & " + " & ".join(row)]
  file_name = "stabilization"+str(lc_config)+".tex"
  with open(file_name, "w") as f:
    f.write("\\\\ \n".join(sl) + "\\\\")
  print("=============")


for i in [1, 2, 3]:
  print("LATENCY CONFIG " + str(i) + " \n")
  result(i,)