
def gen_ops():
  l = ['a','b','c','d','e','f','g']
  ops = [] 
  cmd = 'http://localhost:6001/add?n='
  ops += [cmd+'a&p=root', cmd+'b&p=root', cmd+'c&p=root']
  for each in l:
    for nested in l:
      ops += [cmd+each+nested+'&p='+each]
      p = each+nested
      for n in l:
        ops += [cmd+p+n+'&p='+p]
  return ops

# print(gen_ops())

ops = gen_ops()
with open("base.sh", "w") as f:
  f.writelines(['curl "' + x + '"\n' for x in ops])
