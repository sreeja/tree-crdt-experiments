import uuid

class Node:
  def __init__(self, parent, id, name):
    self.id = id
    self.name = name
    # self.children = []
    self.parent = parent
    # self.tombstone = False
  
  def __eq__(self, obj):
    return self.id = obj.id

class Tree:
  def __init__(self):
    self.root = Node('root', None, 0)
    self.tombstones = {}
    self.log = []

  def add_eff(self, parent, id, name):
    node = Node(parent, id, name)

  def remove_eff(self, node):
    self.tombstones.add(node)

  def move_eff(self, node, new_parent):
    node.parent = new_parent

  # def downmove_eff(self, node, new_parent, critical_ancestors):
  #   node.parent = new_parent
  # #   if concurrent upmove or downmove with high priority on critical ancestors:
  # #     skip
  # #   else:
  # #     node.parent = new_parent

  def construct(self):
    for l in self.log:
      if l[0] == "add":
        self.add_eff(l[2][0], l[2][1], l[2][2])
      elif l[0] == "remove":
        self.remove_eff(l[2][1])
      elif l[0] == "upmove":
        self.move_eff(l[2][1], l[2][2])
      else:
        conc_move = self.get_concurrent_move(l)
        if conc_move:
          if conc_move[0] == "upmove":
            pass
          elif conc_move[2][1] in l[3]: # concurrent down move on critical ancestors
            if l[2][3] == min(l[2][3], conc_move[2][3]): # high priority move
              self.move_eff(l[2][1], l[2][2])

  def get_ancestors(self, node):
    # self.construct()
    a = {}
    while node != self.root:
      a.add(node)
      node = node.parent
    return a

  def get_critical_ancestors(self, source, destination):
    ca = {}
    source_ancestors = self.get_ancestors(source)
    destination_ancestors = self.get_ancestors(destination)
    ca = destination_ancestors - source_ancestors
    return ca

  def rank(self, node): 
    self.construct()
    if node == root:
      return 0
    return self.rank(node.parent) + 1

  def add(self, parent, name, replica, ts):
    id = str(replica) + '-' + uuid.uuid1()
    # node = Node(parent, id, name)
    ts[replica] += 1
    self.log += ["add", ts, [parent, id, name, replica], {}]
    # self.nodes.add(node)

  def remove(self, parent, node, replica, ts):
    self.log += ["remove", ts, [parent, node, replica], {}]
    # self.tombstones.add(node)

  def move(self, parent, node, new_parent, replica, ts):
    if self.rank(node) > self.rank(new_parent):
      self.log += ["upmove", ts, [parent, node, new_parent, replica], {}]
    else:
      self.log += ["downmove", ts, [parent, node, new_parent, replica], self.get_critical_ancestors(node, new_parent)]
    # node.parent = new_parent
