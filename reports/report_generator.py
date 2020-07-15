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

def parse_logs(lc_config, exp, conflict, run):
  data = {}
  for r in replicas:
    reg_file = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'run'+str(run), 'lc'+str(lc_config), 'data'+str(conflict), str(exp), r, 'register.txt')
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
    reg_file = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'run'+str(run), 'lc'+str(lc_config), 'data'+str(conflict), str(exp), r, 'done.txt')
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
      reg_file = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'run'+str(run), 'lc'+str(lc_config), 'data'+str(conflict), str(exp), r, file_name)
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
    reg_file = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'run'+str(run), 'lc'+str(lc_config), 'data'+str(conflict), str(exp), 'paris', file_name)
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
              print("issue: " + str(j))
            else:
              skipmove_count += 1
            data[key]["op"] = {"name":j["op"], "n":None, "ca":None}
          data[key]["origin"] = j["replica"]
  # print([data[x]["ts"][0] for x in data.keys()])
  print(run, lc_config, exp, conflict)
  for each in range(353,653):
    assert(each in [data[x]["ts"][0] for x in data.keys()])
    assert(each in [data[x]["ts"][1] for x in data.keys()])
    assert(each in [data[x]["ts"][2] for x in data.keys()])
  # print(data.keys(), len(data))
  assert len(data) == 900
  # print ("skipmoves : " + str(skipmove_count))
  return data

def parse_replica_logs(lc_config, exp, conflict, run):
  data = {}
  for r in replicas:
    for r1 in replicas:
      file_name = 'time'+r1+'.txt'
      reg_file = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'run'+str(run), 'lc'+str(lc_config), 'data'+str(conflict), str(exp), r, file_name)
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
    reg_file = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'run'+str(run), 'lc'+str(lc_config), 'data'+str(conflict), str(exp), 'paris', file_name)
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


def result(lc_config, run):
  # latex output
  # return average response time, per experiment
  # print("Response time")
  # print("=============")
  responses = {}
  move_responses = {}
  stabilizations = {}
  rl = []
  for j in [0, 2, 10, 20]:
    responses[j] = {}
    move_responses[j] = {}
    stabilizations[j] = {}
    # print("Conflict %: " + str(j) + " : ")
    row = []
    for i in [0, 1, 2, 3]:
      # print("Experiment " + str(i))
      # print("Conflict %: " + str(j))
      data = parse_logs(lc_config, i, j, run)
      rt = response_time(data)
      # print(experiments[i] + " All: " + str(rt[1].total_seconds()*1000) + " :: Moves: " + str(rt[2].total_seconds()*1000) + " :: Nonmoves: " + str(rt[3].total_seconds()*1000))
      row += [experiments[i] + ' & ' +str(rt[1].total_seconds()*1000) + ' & ' +str(rt[2].total_seconds()*1000) + ' & ' + str(rt[3].total_seconds()*1000) + '\\\\']
      file_name = "response"+str(lc_config)+"con"+str(j)+"exp"+str(i)+".json"
      file_to_write = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'run'+str(run), 'lc'+str(lc_config), 'data'+str(j), str(i), file_name)
      with open(file_to_write, "w") as f:
        f.write("\n".join([str(r) for r in rt[0]]))
      responses[j][i] = rt[1].total_seconds()*1000
      move_responses[j][i] = rt[2].total_seconds()*1000
    # rl += [row]
    # file_name = "response"+str(lc_config)+"con"+str(j)+".tex"
    # with open(file_name, "w") as f:
    #   f.write("\n".join(row))
  # print("=============")
  # return  average stabilization time per experiment
  # print("Stabilization time")
  # print("=============")
  sl = []
  for i in [0, 1, 2, 3]:
    # print(experiments[i])
    row = []
    for j in [0, 2, 10, 20]:
      # print("Conflict %: " + str(j))
      data = parse_replica_logs(lc_config, i, j, run)
      res = stabilization_time(i, data)
      # print("Conflict %: " + str(j) + " : " + "All: " + str(res[1].total_seconds()*1000) + " moves: " + str(res[2].total_seconds()*1000) + " other operations: " + str(res[3].total_seconds()*1000))
      row += [str(res[1].total_seconds()*1000)]
      file_name = "stab"+str(lc_config)+"con"+str(j)+"exp"+str(i)+".json"
      file_to_write = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'run'+str(run), 'lc'+str(lc_config), 'data'+str(j), str(i), file_name)
      with open(file_to_write, "w") as f:
        f.write("\n".join([str(s) for s in res[0]]))
      stabilizations[j][i] = res[1].total_seconds()*1000
    sl += [experiments[i] + " & " + " & ".join(row)]
  # file_name = "stabilization"+str(lc_config)+".tex"
  # with open(file_name, "w") as f:
  #   f.write("\\\\ \n".join(sl) + "\\\\")
  # print("=============")
  return responses, stabilizations, move_responses

import random
responses = {}
stabilizations = {}
move_responses = {}
for l in [1, 2, 3]:
  responses[l] = {}
  move_responses[l] = {}
  stabilizations[l] = {}
  for c in [0, 2, 10, 20]:
    responses[l][c] = {}
    move_responses[l][c] = {}
    stabilizations[l][c] = {}
    for e in range(4):
      responses[l][c][e] = []
      move_responses[l][c][e] = []
      stabilizations[l][c][e] = []

for run in range(15, 16):
  for i in [1, 2, 3]:
    # print("LATENCY CONFIG " + str(i) + " \n")
    res0, res1, resm = result(i,run)
    for con in [0, 2, 10, 20]:
      for exp in range(4):
        responses[i][con][exp] += [res0[con][exp]]
        move_responses[i][con][exp] += [resm[con][exp]]
        stabilizations[i][con][exp] += [res1[con][exp]]
    # for con in [0, 2, 10, 20]:
    #   for e in range(4):
    #     responses[con][e] += [random.randint(0,5)]

# print(responses, stabilizations)

import numpy as np
import matplotlib.pyplot as plt

x_pos = np.arange(4)
width = 0.2
resp0 = [np.mean(np.array(responses[2][con][0])) for con in responses[2]]
resperr0 = [np.std(np.array(responses[2][con][0])) for con in responses[2]]
resp1 = [np.mean(np.array(responses[2][con][1])) for con in responses[2]]
resperr1 = [np.std(np.array(responses[2][con][1])) for con in responses[2]]
resp2 = [np.mean(np.array(responses[2][con][2])) for con in responses[2]]
resperr2 = [np.std(np.array(responses[2][con][2])) for con in responses[2]]
resp3 = [np.mean(np.array(responses[2][con][3])) for con in responses[2]]
resperr3 = [np.std(np.array(responses[2][con][3])) for con in responses[2]]

# Build the plot
fig, ax = plt.subplots()
bar0 = ax.bar(x_pos - 1.5*width, resp0, width, yerr=resperr0, align='center', alpha=0.5, ecolor='black', capsize=2)
bar1 = ax.bar(x_pos - width/2, resp1, width, yerr=resperr1, align='center', alpha=0.5, ecolor='black', capsize=2)
bar2 = ax.bar(x_pos + width/2, resp2, width, yerr=resperr2, align='center', alpha=0.5, ecolor='black', capsize=2)
bar3 = ax.bar(x_pos + 1.5*width, resp3, width, yerr=resperr3, align='center', alpha=0.5, ecolor='black', capsize=2)
ax.set_ylabel('Response time in ms')
ax.set_xticks(x_pos)
ax.set_xticklabels([0, 2, 10, 20])
ax.set_title('Response time for varying conflict rates')
ax.legend((bar0[0], bar1[0], bar2[0], bar3[0]), ('CRDT', 'Opsets', 'global', 'subtree'))
ax.yaxis.grid(True)

# Save the figure and show
plt.tight_layout()
plt.savefig('response_time.png')
# plt.show()

mresp0 = [np.mean(np.array(move_responses[2][con][0])) for con in move_responses[2]]
mresperr0 = [np.std(np.array(move_responses[2][con][0])) for con in move_responses[2]]
mresp1 = [np.mean(np.array(move_responses[2][con][1])) for con in move_responses[2]]
mresperr1 = [np.std(np.array(move_responses[2][con][1])) for con in move_responses[2]]
mresp2 = [np.mean(np.array(move_responses[2][con][2])) for con in move_responses[2]]
mresperr2 = [np.std(np.array(move_responses[2][con][2])) for con in move_responses[2]]
mresp3 = [np.mean(np.array(move_responses[2][con][3])) for con in move_responses[2]]
mresperr3 = [np.std(np.array(move_responses[2][con][3])) for con in move_responses[2]]

# Build the plot
fig, ax = plt.subplots()
bar0 = ax.bar(x_pos - 1.5*width, mresp0, width, yerr=mresperr0, align='center', alpha=0.5, ecolor='black', capsize=2)
bar1 = ax.bar(x_pos - width/2, mresp1, width, yerr=mresperr1, align='center', alpha=0.5, ecolor='black', capsize=2)
bar2 = ax.bar(x_pos + width/2, mresp2, width, yerr=mresperr2, align='center', alpha=0.5, ecolor='black', capsize=2)
bar3 = ax.bar(x_pos + 1.5*width, mresp3, width, yerr=mresperr3, align='center', alpha=0.5, ecolor='black', capsize=2)
ax.set_ylabel('Response time in ms')
ax.set_xticks(x_pos)
ax.set_xticklabels([0, 2, 10, 20])
ax.set_title('Response time for varying conflict rates')
ax.legend((bar0[0], bar1[0], bar2[0], bar3[0]), ('CRDT', 'Opsets', 'global', 'subtree'))
ax.yaxis.grid(True)

# Save the figure and show
plt.tight_layout()
plt.savefig('response_time_moves.png')
# plt.show()


x_pos = np.arange(3)
stab0 = [np.mean(np.array(stabilizations[l][0][0])) for l in stabilizations]
staberr0 = [np.std(np.array(stabilizations[l][0][0])) for l in stabilizations]
stab1 = [np.mean(np.array(stabilizations[l][0][1])) for l in stabilizations]
staberr1 = [np.std(np.array(stabilizations[l][0][1])) for l in stabilizations]

# print(stab0, staberr0)
# print(stab1, staberr1)

# Build the plot
fig, ax = plt.subplots()
bar0 = ax.bar(x_pos - width/2, stab0, width, yerr=staberr0, align='center', alpha=0.5, ecolor='black', capsize=2)
bar1 = ax.bar(x_pos + width/2, stab1, width, yerr=staberr1, align='center', alpha=0.5, ecolor='black', capsize=2)
ax.set_ylabel('Stabilization time in ms')
ax.set_xticks(x_pos)
ax.set_xticklabels([1, 2, 3])
ax.set_title('Stabilization time for varying latency configurations')
ax.legend((bar0[0], bar1[0]), ('CRDT', 'Opsets'))
ax.yaxis.grid(True)
plt.yscale('log') #logarithmic scale
# Save the figure and show
plt.tight_layout()
plt.savefig('stabilization_time.png')
# plt.show()