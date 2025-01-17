class Node:
  def __init__(self, id, parent):
    self.id = id
    self.parent = parent
    self.tombstone = False
  
  def __eq__(self, obj):
    return self.id == obj.id

  @classmethod
  def serialize(cls, node):
    result = {'id':node.id, 'parent':node.parent, 'tombstone':node.tombstone}
    return result

  @classmethod
  def deserialize(cls, string):
    node = Node(string['id'], string['parent'])
    node.tombstone = string['tombstone']
    return node

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

  def get_all_descendants(self):
    d = {}
    for n in self.nodes:
      d[n] = []
    for n in self.nodes:
      node = self.nodes[n]
      while node != self.root:
        parent = node.parent
        d[parent] += [node]
        node = self.nodes[parent]
    return d

  def get_descendants(self, id):
    # node = self.nodes[id]
    d = self.get_all_descendants()
    return d[id]

  def rank(self, node): 
    if node == self.root.id:
      return 0
    return self.rank(self.nodes[node].parent) + 1

  def add_gen(self, n, p):
    if p in self.nodes and not n in self.nodes: # precondition assertion
      op = 'add'
      args = {'n':n, 'p':p}
      ca = []
      return (op, args, ca, [])

  def remove_gen(self, n, p):
    op = 'remove'
    args = {'n':n, 'p':p}
    ca = []
    return (op, args, ca, [])

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
          desc = self.get_descendants(n)
          return (op, args, ca, desc)  

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
  def get_historical_moves(cls, moves, ts):
    hms = []
    for m in moves:
      if cls.is_greater(ts, moves[m]['ts']):
        hms += [m]
    return hms

  @classmethod
  def construct_tree(cls, logs, tree = None):
    if tree == None:
      tree = Tree_CRDT()
    moves = {}
    for l in logs:
      if l['op'] == 'add':
        tree.add_eff(l['args']['n'], l['args']['p'])
      elif l['op'] == 'remove':
        tree.remove_eff(l['args']['n'])
      elif l['op'] in ['upmove', 'downmove']:
        moves[str(l['ts'])] = {'type':l['op'], 'n':l['args']['n'], 'p':l['args']['p'], 'np':l['args']['np'], 'ca':l['ca'], 'd':l['d'], 'replica':l['replica'], 'ts':l['ts']}
      elif l['op'] in ['moveskip', 'addskip', 'removeskip']:
        pass
      else:
        Exception('Unknown operation')

    skipped_moves = set()
    for m in moves:
      cms = cls.get_concurrent_moves(moves, moves[m]['ts'])
      hms = cls.get_historical_moves(moves, moves[m]['ts'])
      skip = False
      if moves[m]['type'] == 'upmove':
        for cm in cms:
          if moves[cm]['type'] == 'upmove':
            if cls.higher_priority(moves[cm], moves[m]):
              skip = True
        for hm in hms:
          if hm in skipped_moves:
            #  dependency condition
            if moves[hm]['type'] == 'upmove':
              if moves[m]['np'] in moves[hm]['d']:
                skip = True
            else:
              if ((moves[hm]['n'] in moves[m]['d']) and (moves[m]['np'] in moves[hm]['d'])) or (moves[m]['n'] in moves[hm]['d']):
                skip = True
      else:
        for cm in cms:
          if moves[m]['n'] in moves[cm]['ca'] or moves[cm]['n'] in moves[m]['ca']:
            if moves[cm]['type'] == 'upmove':
              skip = True
            else:
              if cls.higher_priority(moves[cm], moves[m]):
                skip = True
        for hm in hms:
          if hm in skipped_moves:
            #  dependency condition
            if moves[hm]['type'] == 'upmove':
              if ((moves[hm]['n'] in moves[m]['d']) and (moves[m]['np'] in moves[hm]['d'])) or (moves[m]['n'] in moves[hm]['d']):
                skip = True
            else:
              if moves[m]['np'] in moves[hm]['d']:
                skip = True
      if not skip:
        tree.move_eff(moves[m]['n'], moves[m]['p'], moves[m]['np'])
      else:
        skipped_moves.add(m)
    return tree

  @classmethod
  def serialize(cls, tree):
    node_list = {}
    for each in tree.nodes:
      node_list[each] = Node.serialize(tree.nodes[each])
    result = {'root':Node.serialize(tree.root), 'nodes':node_list}
    return result

  @classmethod
  def deserialize(cls, string):
    tree = Tree_CRDT()
    for each in string['nodes']:
      tree.nodes[each] = Node.deserialize(string['nodes'][each])
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
  def construct_tree(cls, logs, tree = None):
    if tree == None:
      tree = Tree_Opset()
    for l in logs:
      if l['op'] == 'add':
        tree.add_eff(l['args']['n'], l['args']['p'])
      elif l['op'] == 'remove':
        tree.remove_eff(l['args']['n'])
      elif l['op'] == 'move':
        tree.move_eff(l['args']['n'], l['args']['p'], l['args']['np'])
      elif l['op'] in ['moveskip', 'addskip', 'removeskip']:
        pass
      else:
        Exception('Unknown operation')
    return tree

  @classmethod
  def serialize(cls, tree):
    node_list = {}
    for each in tree.nodes:
      node_list[each] = Node.serialize(tree.nodes[each])
    result = {'root':Node.serialize(tree.root), 'nodes':node_list}
    return result

  @classmethod
  def deserialize(cls, string):
    tree = Tree_Opset()
    for each in string['nodes']:
      tree.nodes[each] = Node.deserialize(string['nodes'][each])
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
  def construct_tree(cls, logs, tree = None):
    if tree == None:
      tree = Tree_Globalock()
    for l in logs:
      if l['op'] == 'add':
        tree.add_eff(l['args']['n'], l['args']['p'])
      elif l['op'] == 'remove':
        tree.remove_eff(l['args']['n'])
      elif l['op'] == 'move':
        tree.move_eff(l['args']['n'], l['args']['p'], l['args']['np'])
      elif l['op'] in ['moveskip', 'addskip', 'removeskip']:
        pass
      else:
        Exception('Unknown operation')
    return tree

  @classmethod
  def serialize(cls, tree):
    node_list = {}
    for each in tree.nodes:
      node_list[each] = Node.serialize(tree.nodes[each])
    result = {'root':Node.serialize(tree.root), 'nodes':node_list}
    return result

  @classmethod
  def deserialize(cls, string):
    tree = Tree_Globalock()
    for each in string['nodes']:
      tree.nodes[each] = Node.deserialize(string['nodes'][each])
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
  def construct_tree(cls, logs, tree=None):
    if tree == None:
      tree = Tree_Sublock()
    for l in logs:
      if l['op'] == 'add':
        tree.add_eff(l['args']['n'], l['args']['p'])
      elif l['op'] == 'remove':
        tree.remove_eff(l['args']['n'])
      elif l['op'] == 'move':
        tree.move_eff(l['args']['n'], l['args']['p'], l['args']['np'])
      elif l['op'] in ['moveskip', 'addskip', 'removeskip']:
        pass
      else:
        Exception('Unknown operation')
    return tree

  @classmethod
  def serialize(cls, tree):
    node_list = {}
    for each in tree.nodes:
      node_list[each] = Node.serialize(tree.nodes[each])
    result = {'root':Node.serialize(tree.root), 'nodes':node_list}
    return result

  @classmethod
  def deserialize(cls, string):
    tree = Tree_Sublock()
    for each in string['nodes']:
      tree.nodes[each] = Node.deserialize(string['nodes'][each])
    return tree
