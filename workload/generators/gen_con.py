import random

def gen_ops(conflict):
  x = 97
  # an op tuple : (replica, operation, args)
  ops = {} 
  # non conflicting operations
  nc_ops = {}
  # conflicting operations
  c_ops = []

  nc = 90 - (3 * conflict)

  for r in range(0,3):
    ops[r] = []
    nc_ops[r] = []

    rep = chr(97 + r)
    # conflict loads
    for j in range(3,(conflict/2) + 3):
      # up-down conflicts
      parent = rep + chr(97 + j)
      node = parent + 'a'
      new_p = rep + chr(97 + j + 1)
      args = ['n='+node, 'p='+parent, 'np='+new_p]
      con_args = ['n='+new_p, 'p='+rep, 'np='+node]
      c_ops += [((r, 'move', '&'.join(args)), ((r+1)%3, 'move', '&'.join(con_args)))]
    for j in range(0, (conflict/2)):
      # up-up conflicts
      parent = rep + 'a'
      node = parent + chr(97+j)
      new_p = rep + 'b'
      args = ['n='+node, 'p='+parent, 'np='+new_p]
      con_args = ['n='+node, 'p='+parent, 'np='+rep+'c']
      c_ops += [((r, 'move', '&'.join(args)), ((r+1)%3, 'move', '&'.join(con_args)))]
    for j in range(0, (conflict/2)):
      # down-down conflicts
      parent = rep + 'b'
      node = parent + chr(97+j)
      new_p = rep + 'c' + chr(97+j)
      args = ['n='+node, 'p='+parent, 'np='+new_p]
      con_args = ['n='+new_p, 'p='+rep+'c', 'np='+node]
      c_ops += [((r, 'move', '&'.join(args)), ((r+1)%3, 'move', '&'.join(con_args)))]
    
    # non-conflicting loads
    rep = chr(97 + 3 + r)
    if conflict%10:
      for i in range(0, nc/14):
        for j in range(0, 7):
          parent = rep + chr(97+j)
          node = parent + chr(97+i)
          new_p = rep
          args = ['n='+node, 'p='+parent, 'np='+new_p]
          nc_ops[r] += [(r, 'move', '&'.join(args))]
          args = ['n='+node, 'p='+new_p, 'np='+parent]
          nc_ops[r] += [(r, 'move', '&'.join(args))]
    else:
      for i in range(0, nc/10):
        for j in range(0, 5):
          parent = rep + chr(97+i)
          node = parent + chr(97+j)
          new_p = rep
          args = ['n='+node, 'p='+parent, 'np='+new_p]
          nc_ops[r] += [(r, 'move', '&'.join(args))]
          args = ['n='+node, 'p='+new_p, 'np='+parent]
          nc_ops[r] += [(r, 'move', '&'.join(args))]

  k0=0
  k1=0
  k2=0
  for j in range(len(c_ops)):
    if c_ops[j][0][0] == 0:
      ops[0] += [c_ops[j][0]]
      if c_ops[j][1][0] == 1:
        ops[1] += [c_ops[j][1]]
        ops[2] += [nc_ops[2][k2]]
        k2 += 1
      else:
        ops[2] += [c_ops[j][1]]
        ops[1] += [nc_ops[1][k1]]
        k1 += 1
    elif c_ops[j][0][0] == 1:
      ops[1] += [c_ops[j][0]]
      if c_ops[j][1][0] == 0:
        ops[0] += [c_ops[j][1]]
        ops[2] += [nc_ops[2][k2]]
        k2 += 1
      else:
        ops[2] += [c_ops[j][1]]
        ops[0] += [nc_ops[0][k0]]
        k0 += 1
    else:
      ops[2] += [c_ops[j][0]]
      if c_ops[j][1][0] == 0:
        ops[0] += [c_ops[j][1]]
        ops[1] += [nc_ops[1][k1]]
        k1 += 1
      else:
        ops[1] += [c_ops[j][1]]
        ops[0] += [nc_ops[0][k0]]
        k0 += 1

  assert(k0 == k1)
  assert(k0 == k2)

  while k0 < len(nc_ops[0]):
    for i in range(0, 3):
      ops[i] += [nc_ops[i][k0]]
    k0 += 1


  # add and remove ops
  for i in range(0,180): 
    for r in range(0, 3): 
      parent = chr(97 + r) + chr(97 + random.randint(0,10)) + chr(97 + random.randint(0,5)) 
      args = ['n='+parent + str(i) + str(r), 'p='+parent]
      ops[r] += [(r, 'add', '&'.join(args))]
      if not i%6: 
        # print('remove this') 
        ops[r] += [(r, 'remove', '&'.join(args))]


  return ops

# ops = gen_ops(2)
# for each in ops:
#   print(ops[each])
#   print(len(ops[each]))

for conflict in [0, 2, 10, 20]:
  ops = gen_ops(conflict)
  file_name = 'conflict'+str(conflict)+'.sh'
  with open(file_name, "w") as f:
    f.writelines(['curl "http://localhost:600' + str(ops[0][o][0]+1) + '/' + ops[0][o][1] + '?' + ops[0][o][2] + '" & curl "http://localhost:600' + str(ops[1][o][0]+1) + '/' + ops[1][o][1] + '?' + ops[1][o][2] + '" & curl "http://localhost:600' + str(ops[2][o][0]+1) + '/' + ops[2][o][1] + '?' + ops[2][o][2] + '"\nwait \n' for o in range(0, len(ops[0]))])
