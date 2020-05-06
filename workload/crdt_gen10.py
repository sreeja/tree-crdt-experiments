'''
30 adds, 6 removes, 3 up, 3 down conflicting moves, 4 up and 4 down non-conflicting moves
'''

import random


def gen_ops(): 
  ops = [[],[],[]]
  cmd = 'http://localhost:600'
  l = ['a','b','c'] 
  n = ['a','b','c','d','e','f','g']
  for i in range(0,30): 
    for r in range(1,4): 
      parent = random.choice(l) + random.choice(l+['']) + random.choice(l+['']) 
      # print(parent, parent + str(i) + str(r)) 
      ops[r-1] += [cmd+str(r)+'/add?n='+parent + str(i) + str(r)+'&p='+parent]
      if not i%5: 
        # print('remove this') 
        ops[r-1] += [cmd+str(r)+'/remove?n='+parent + str(i) + str(r)+'&p='+parent]
  for r in range(1,4):
    for c in range(0,3): 
      ops[r-1] += [cmd+str(r)+'/upmove?n='+n[r-1]+n[c]+'a'+'&p='+n[r-1]+n[c]+'&np='+n[r-1]+n[c+1]]
      ops[r%3] += [cmd+str(r%3+1)+'/downmove?n='+n[r-1]+n[c+1]+'&p='+n[r-1]+'&np='+n[r-1]+n[c]+'a']

  for i in range(0,4):
    for r in range(1,4):
      parent = n[r-1]+'f'
      child = parent+random.choice(n)
      ops[r-1] += [cmd+str(r)+'/upmove?n='+child+'&p='+parent+'&np='+n[r-1]]
      ops[r-1] += [cmd+str(r)+'/downmove?n='+child+'&p='+n[r-1]+'&np='+parent]
  
  return ops

# print(gen_ops())
# for each in gen_ops():
#   print(each, len(each))

ops = gen_ops()
for i, each in enumerate(ops):
  file_name = "crdt_10_load"+str(i)+".sh"
  with open(file_name, "w") as f:
    f.writelines(['curl "' + x + '"\n' for x in ops[i]])
