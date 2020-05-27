class Node:
  def __init__(self, id, parent):
    self.id = id
    self.parent = parent
    self.tombstone = False
  
  def __eq__(self, obj):
    return self.id == obj.id

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

  def move_eff(self, id, new_parent):
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
  
  @staticmethod
  def construct_tree(logs):
    pass