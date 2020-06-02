def gen_ops(conflict):
  x = 97
  # an op tuple : (replica, operation, args)
  ops = {} 
  # non conflicting operations
  nc_ops = {}
  # conflicting operations
  c_ops = []

  for r in range(0,3):
    ops[r] = []
    nc_ops[r] = []

  for r in range(0,3):
      rep = chr(97 + 3 + r)
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


  return c_ops

for conflict in [20]:
  ops = gen_ops(conflict)
  for each in ops:
    print(each)
  print(len(ops))

# for conflict in [0, 2, 10, 20]:
#   ops = gen_ops(conflict)
#   with open("base.sh", "w") as f:
#     f.writelines(['curl "http://localhost:600' + str(ops[0][o][0]+1) + '/' + ops[0][o][1] + '?' + ops[0][o][2] + '" & curl "http://localhost:600' + str(ops[1][o][0]+1) + '/' + ops[1][o][1] + '?' + ops[1][o][2] + '" & curl "http://localhost:600' + str(ops[2][o][0]+1) + '/' + ops[2][o][1] + '?' + ops[2][o][2] + '"\nwait \n' for o in range(0, len(ops[0]))])
