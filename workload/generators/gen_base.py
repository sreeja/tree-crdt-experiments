
def gen_ops():
  x = 97
  # an op tuple : (replica, operation, args)
  ops = {} 
  for r in range(0,3):
    ops[r] = []
    for i in range(0,2):
      node = chr(97 + (3*i) + r)
      args = ['n='+node, 'p=root']
      ops[r] += [(r, 'add', '&'.join(args))]
      for j in range(0, 15):
        subnode = node + chr(97 + j)
        args = ['n='+subnode, 'p='+node]
        ops[r] += [(r, 'add', '&'.join(args))]
        for k in range(0,10):
          subsubnode = subnode + chr(97+k)
          args = ['n='+subsubnode, 'p='+subnode]
          ops[r] += [(r, 'add', '&'.join(args))]
    for i in range(15, 20):
      grand = chr(97+r)
      parent = grand+'n'
      node = parent+chr(97+i)
      ops[r] += [(r, 'add', '&'.join(['n='+node, 'p='+parent]))]
      ops[r] += [(r, 'move', '&'.join(['n='+node, 'p='+parent, 'np='+grand]))]
      ops[r] += [(r, 'move', '&'.join(['n='+node, 'p='+grand, 'np='+parent]))]
      ops[r] += [(r, 'remove', '&'.join(['n='+node, 'p='+parent]))]
  return ops

# print(gen_ops())

ops = gen_ops()
with open("base.sh", "w") as f:
  f.writelines(['curl "http://localhost:600' + str(ops[0][o][0]+1) + '/' + ops[0][o][1] + '?' + ops[0][o][2] + '" & curl "http://localhost:600' + str(ops[1][o][0]+1) + '/' + ops[1][o][1] + '?' + ops[1][o][2] + '" & curl "http://localhost:600' + str(ops[2][o][0]+1) + '/' + ops[2][o][1] + '?' + ops[2][o][2] + '"\nwait \n' for o in range(0, len(ops[0]))])
