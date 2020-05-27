class Node:
  def __init__(self, id, parent):
    self.id = id
    self.parent = parent
    self.tombstone = False
  
  def __eq__(self, obj):
    return self.id == obj.id

#########################################################################################################
# CRDT tree
class Tree_CRDT:
  def __init__(self):
    self.root = Node('root', None)
    self.nodes = {}
    self.nodes['root'] = self.root

  def add_eff(self, id, parent):
    node = Node(id, parent)
    self.nodes[id] = node

  def remove_eff(self, id):
    removed_node = self.nodes[id]
    removed_node.tombstone = True

  def move_eff(self, id, p, new_parent):
    node = self.nodes[id]
    node.parent = new_parent

  def get_ancestors(self, id):
    node = self.nodes[id]
    a = set()
    while node != self.root:
      parent = node.parent
      node = self.nodes[parent]
      a.add(node.id)
    return a

  def get_critical_ancestors(self, source, destination):
    ca = set()
    source_ancestors = self.get_ancestors(source)
    destination_ancestors = self.get_ancestors(destination)
    ca = destination_ancestors.union({destination}) - source_ancestors
    return ca

  def rank(self, node): 
    if node == self.root.id:
      return 0
    return self.rank(self.nodes[node].parent) + 1

  def add_gen(self, n, p):
    if p in self.nodes and not n in self.nodes: # precondition assertion
      op = 'add'
      args = {'n':n, 'p':p}
      ca = []
      return (op, args, ca)

  def remove_gen(self, n, p):
    op = 'remove'
    args = {'n':n, 'p':p}
    ca = []
    return (op, args, ca)

  def move_gen(self, n, p, np):
    if p in self.nodes and np in self.nodes and n in self.nodes:
      node = self.nodes[n]
      if node.parent == p:
        if not n in self.get_ancestors(np):
          if self.rank(n) > self.rank(np):
            op = 'upmove'
          else:
            op = 'downmove'
          args = {'n':n, 'p':p, 'np':np}
          ca = list(self.get_critical_ancestors(n, np))
          return (op, args, ca)  

  @classmethod
  def is_greater(cls, ts1, ts2):
    if len(ts1) != len(ts2):
      return False
    for i in range(len(ts1)):
      if ts1[i] < ts2[i]:
        return False
    return True

  @classmethod
  def get_concurrent_moves(cls, moves, ts):
    cms = []
    for m in moves:
      if not cls.is_greater(moves[m]['ts'], ts) and not cls.is_greater(ts,moves[m]['ts']):
        cms += [m]
    return cms

  @classmethod
  def higher_priority(cls, m1, m2):
    if m1['replica'] < m2['replica']:
      return True
    return False

  @classmethod
  def construct_tree(cls, tree = Tree_CRDT(), logs):
    moves = {}
    for l in logs:
      if l['op'] == 'add':
        tree.add_eff(l['args']['n'], l['args']['p'])
      elif l['op'] == 'remove':
        tree.remove_eff(l['args']['n'])
      elif l['op'] in ['upmove', 'downmove']:
        moves[str(l['ts'])] = {'type':l['op'], 'n':l['args']['n'], 'np':l['args']['np'], 'ca':l['ca'], 'replica':l['replica'], 'ts':l['ts']}
      else:
        Exception('Unknown operation')

    for m in moves:
      cms = cls.get_concurrent_moves(moves, moves[m]['ts'])
      flag = False
      if moves[m]['type'] == 'upmove':
        for cm in cms:
          if moves[cm]['type'] == 'upmove':
            if cls.higher_priority(moves[cm], moves[m]):
              flag = True
      else:
        for cm in cms:
          if moves[m]['n'] in moves[cm]['ca'] or moves[cm]['n'] in moves[m]['ca']:
            if moves[cm]['type'] == 'upmove':
              flag = True
            else:
              if cls.higher_priority(moves[cm], moves[m]):
                flag = True
      if not flag:
        tree.move_eff(moves[m]['n'], moves[m]['p'], moves[m]['np'])
    return tree

#########################################################################################################
# Tree based on Opsets
class Tree_Opset:
  def __init__(self):
    self.root = Node('root', None)
    self.nodes = {}
    self.nodes['root'] = self.root

  def get_ancestors(self, id):
    node = self.nodes[id]
    a = set()
    while node != self.root:
      parent = node.parent
      node = self.nodes[parent]
      a.add(node.id)
    return a

  def add_eff(self, n, p):
    if p in self.nodes and not n in self.nodes: # precondition assertion
      node = Node(n, p)
      self.nodes[n] = node

  def remove_eff(self, n):
    removed_node = self.nodes[n]
    removed_node.tombstone = True

  def move_eff(self, n, p, np):
    if p in self.nodes and np in self.nodes and n in self.nodes:
      node = self.nodes[n]
      if node.parent == p:
        if not n in self.get_ancestors(np):
          node = self.nodes[n]
          node.parent = np 

  def add_gen(self, n, p):
    if p in self.nodes and not n in self.nodes: # precondition assertion
      op = 'add'
      args = {'n':n, 'p':p}
      ca = []
      return (op, args, ca)

  def remove_gen(self, n, p):
    op = 'remove'
    args = {'n':n, 'p':p}
    ca = []
    return (op, args, ca)

  def move_gen(self, n, p, np):
    if p in self.nodes and np in self.nodes and n in self.nodes:
      node = self.nodes[n]
      if node.parent == p:
        if not n in self.get_ancestors(np):
          op = 'move'
          args = {'n':n, 'p':p, 'np':np}
          ca = []
          return (op, args, ca)  
  
  @classmethod
  def construct_tree(cls, tree = Tree_Opset(), logs):
    for l in logs:
      if l['op'] == 'add':
        tree.add_eff(l['args']['n'], l['args']['p'])
      elif l['op'] == 'remove':
        tree.remove_eff(l['args']['n'])
      elif l['op'] == 'move':
        tree.move_eff(l['args']['n'], l['args']['p'], l['args']['np'])
      else:
        Exception('Unknown operation')
    return tree

#########################################################################################################
# tree where move acquires a single lock every time
class Tree_Globalock:
  def __init__(self):
    self.root = Node('root', None)
    self.nodes = {}
    self.nodes['root'] = self.root

  def get_ancestors(self, id):
    node = self.nodes[id]
    a = set()
    while node != self.root:
      parent = node.parent
      node = self.nodes[parent]
      a.add(node.id)
    return a

  def add_eff(self, n, p):
    node = Node(n, p)
    self.nodes[n] = node

  def remove_eff(self, n):
    removed_node = self.nodes[n]
    removed_node.tombstone = True

  def move_eff(self, n, p, np):
    node = self.nodes[n]
    node.parent = np

  def add_gen(self, n, p):
    if p in self.nodes and not n in self.nodes: # precondition assertion
      op = 'add'
      args = {'n':n, 'p':p}
      ca = []
      return (op, args, ca)

  def remove_gen(self, n, p):
    op = 'remove'
    args = {'n':n, 'p':p}
    ca = []
    return (op, args, ca)

  def move_gen(self, n, p, np):
    if p in self.nodes and np in self.nodes and n in self.nodes:
      node = self.nodes[n]
      if node.parent == p:
        if not n in self.get_ancestors(np):
          op = 'move'
          args = {'n':n, 'p':p, 'np':np}
          ca = []
          return (op, args, ca)  

  @classmethod
  def construct_tree(cls, tree = Tree_Globalock(), logs):
    for l in logs:
      if l['op'] == 'add':
        tree.add_eff(l['args']['n'], l['args']['p'])
      elif l['op'] == 'remove':
        tree.remove_eff(l['args']['n'])
      elif l['op'] == 'move':
        tree.move_eff(l['args']['n'], l['args']['p'], l['args']['np'])
      else:
        Exception('Unknown operation')
    return tree

#########################################################################################################
# tree with move acquiring lock on subtree
class Tree_Sublock:
  def __init__(self):
    self.root = Node('root', None)
    self.nodes = {}
    self.nodes['root'] = self.root

  def add_eff(self, id, parent):
    node = Node(id, parent)
    self.nodes[id] = node

  def remove_eff(self, id):
    removed_node = self.nodes[id]
    removed_node.tombstone = True

  def move_eff(self, id, p, new_parent):
    node = self.nodes[id]
    node.parent = new_parent

  def get_ancestors(self, id):
    node = self.nodes[id]
    a = set()
    while node != self.root:
      parent = node.parent
      node = self.nodes[parent]
      a.add(node.id)
    return a

  def get_critical_ancestors(self, source, destination):
    ca = set()
    source_ancestors = self.get_ancestors(source)
    destination_ancestors = self.get_ancestors(destination)
    ca = destination_ancestors.union({destination}) - source_ancestors
    return ca

  def add_gen(self, n, p):
    if p in self.nodes and not n in self.nodes: # precondition assertion
      op = 'add'
      args = {'n':n, 'p':p}
      ca = []
      return (op, args, ca)

  def remove_gen(self, n, p):
    op = 'remove'
    args = {'n':n, 'p':p}
    ca = []
    return (op, args, ca)

  def move_gen(self, n, p, np):
    if p in self.nodes and np in self.nodes and n in self.nodes:
      node = self.nodes[n]
      if node.parent == p:
        if not n in self.get_ancestors(np):
          op = 'move'
          args = {'n':n, 'p':p, 'np':np}
          ca = list(self.get_critical_ancestors(n, np))
          return (op, args, ca)  
  
  @classmethod
  def construct_tree(cls, tree = Tree_Sublock(), logs):
    for l in logs:
      if l['op'] == 'add':
        tree.add_eff(l['args']['n'], l['args']['p'])
      elif l['op'] == 'remove':
        tree.remove_eff(l['args']['n'])
      elif l['op'] == 'move':
        tree.move_eff(l['args']['n'], l['args']['p'], l['args']['np'])
      else:
        Exception('Unknown operation')
    return tree