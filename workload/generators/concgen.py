import os

def combine(f1,f2,f3, res):
  fp1 = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'workload', f1+'.sh')
  fp2 = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'workload', f2+'.sh')
  fp3 = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'workload', f3+'.sh')
  with open(fp1) as file1:
    lines1 = file1.readlines()
  with open(fp2) as file2:
    lines2 = file2.readlines()
  with open(fp3) as file3:
    lines3 = file3.readlines()
  
  load = []
  for i in range(0, 50):
    load += [lines1[i].strip() + ' & ' + lines2[i].strip() + ' & ' + lines3[i].strip()]
    load += ['\nwait \n']
  
  rp = os.path.join('/', 'Users', 'snair', 'works', 'tree-crdt-experiments', 'workload', res+'.sh')
  with open(rp, 'w') as result:
    result.writelines(load)


combine('conflict0_load0', 'conflict0_load1', 'conflict0_load2', 'conflict0')
combine('conflict2_load0', 'conflict2_load1', 'conflict2_load2', 'conflict2')
combine('conflict10_load0', 'conflict10_load1', 'conflict10_load2', 'conflict10')
combine('conflict20_load0', 'conflict20_load1', 'conflict20_load2', 'conflict20')
