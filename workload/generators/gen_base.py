
def gen_ops():
  l = ['a','b','c','d','e','f','g']
  ops = [] 
  cmd = 'http://localhost:6001/add?n='
  ops += [cmd+x+'&p=root' for x in l]
  for each in l:
    for nested in l:
      ops += [cmd+each+nested+'&p='+each]
      p = each+nested
      ops += [cmd+p+n+'&p='+p for n in l]
  ops += [cmd+'h&p=root']
  ops += ['http://localhost:6002/remove?n=h&p=root']
  ops += ['http://localhost:6003/move?n=ggg&p=gg&np=g']
  ops += ['http://localhost:6003/move?n=ggg&p=g&np=gg']
  return ops

# print(gen_ops())

ops = gen_ops()
with open("base.sh", "w") as f:
  f.writelines(['curl "' + x + '"\n' for x in ops])
