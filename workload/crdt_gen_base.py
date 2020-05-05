
def populate():
  l = ['a','b','c']
  ops = [] 
  cmd = 'http://localhost:6001/add?n='
  ops += [cmd+'a&p=root', cmd+'b&p=root', cmd+'c&p=root']
  for each in l:
    ops += [cmd+each+'a&p='+each, cmd+each+'b&p='+each, cmd+each+'c&p='+each]
    for nested in l:
      ops += [cmd+each+nested+'a&p='+each+nested, cmd+each+nested+'b&p='+each+nested, cmd+each+nested+'c&p='+each+nested]
  return ops

print(populate())