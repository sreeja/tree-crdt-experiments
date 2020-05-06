'''
30 adds, mixed with 6 removes and then 14 moves
'''
import random


def gen_ops(): 
  ops = [[],[],[]]
  cmd = 'http://localhost:600'
  l = ['a','b','c'] 
  for i in range(0,30): 
    for r in range(1,4): 
      parent = random.choice(l) + random.choice(l+['']) + random.choice(l+['']) 
      # print(parent, parent + str(i) + str(r)) 
      ops[r-1] += [cmd+str(r)+'/add?n='+parent + str(i) + str(r)+'&p='+parent]
      if not i%5: 
        # print('remove this') 
        ops[r-1] += [cmd+str(r)+'/remove?n='+parent + str(i) + str(r)+'&p='+parent]
  n = ['a','b','c','d','e','f']
  for i in range(0,7):
    parent = random.choice(n)
    child = parent+random.choice(n)
    for r in range(1,4):
      ops[r-1] += [cmd+str(r)+'/upmove?n='+l[r-1]+child+'&p='+l[r-1]+parent+'&np='+l[r-1]]
      ops[r-1] += [cmd+str(r)+'/downmove?n='+l[r-1]+child+'&p='+l[r-1]+'&np='+l[r-1]+parent]
  
  return ops

print(gen_ops())