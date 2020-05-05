import random

def gen_ops(): 
  ops = []
  cmd = 'http://localhost:600'
  l = ['a','b','c'] 
  for i in range(0,40): 
    for r in range(1,4): 
      parent = random.choice(l) + random.choice(l+['']) + random.choice(l+['']) 
      print(parent, parent + str(i) + str(r)) 
      ops += [cmd+str(r)+'/add?n='+parent + str(i) + str(r)+'&p='+parent]
      if not i%4: 
        print('remove this') 
        ops += [cmd+str(r)+'/remove?n='+parent + str(i) + str(r)+'&p='+parent]
  return ops

for each in gen_ops():
  print(each)