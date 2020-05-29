'''
150 adds, mixed with 30 removes and then 70 moves for 3 replicas
250 ops per replica = 750 ops together
'''
import random


def gen_ops(): 
  ops = [[],[],[]]
  cmd = 'http://localhost:600'
  l = ['a','b','c','d','e','f','g'] 
  for i in range(0,150): 
    for r in range(1,4): 
      parent = l[r-1] + random.choice(l+['']) + random.choice(l+['']) 
      # print(parent, parent + str(i) + str(r)) 
      ops[r-1] += [cmd+str(r)+'/add?n='+parent + str(i) + str(r)+'&p='+parent]
      if not i%5: 
        # print('remove this') 
        ops[r-1] += [cmd+str(r)+'/remove?n='+parent + str(i) + str(r)+'&p='+parent]
  n = ['a','b','c','d','e','f','g']
  for i in range(0,35):
    parent = random.choice(l)
    child = parent+random.choice(l)
    for r in range(1,4):
      # up
      ops[r-1] += [cmd+str(r)+'/move?n='+l[r-1]+child+'&p='+l[r-1]+parent+'&np='+l[r-1]]
      # down
      ops[r-1] += [cmd+str(r)+'/move?n='+l[r-1]+child+'&p='+l[r-1]+'&np='+l[r-1]+parent]
  return ops

# print(gen_ops())
ops = gen_ops()
for i, each in enumerate(ops):
  # print(each, len(each))
  file_name = "conflict0_load"+str(i)+".sh"
  with open(file_name, "w") as f:
    f.writelines(['curl "' + x + '"\n' for x in ops[i]])

