class Node:
  def __init__(self, parent, name):
    self.name = name
    # self.children = []
    self.parent = parent
    # self.tombstone = False

class Tree:
  def __init__(self):
    self.root = Node('root', None)
    self.nodes = {}
    self.tombstones = {}

  def add_eff(self, parent, node):
    self.nodes.add(node)

  def remove_eff(self, parent, node):
    self.tombstones.add(node)

  def upmove_eff(self, parent, node, new_parent):
    node.parent = new_parent

  def downmove_eff(self, parent, node, new_parent):
    pass
    # if concurrent upmove or downmove with high priority on critical ancestors:
    #   skip
    # else:
    #   node.parent = new_parent

  def add(self, parent, name):
    node = Node(parent, name)
    self.add_eff(parent, node)

  def remove(self, parent, node):
    self.remove_eff(parent, node)

  def move(self, parent, node, new_parent):
    pass
    # if moving up:
    #   self.upmove_eff(parent, node, new_parent)
    # else:
    #   self.downmove_eff(parent, node, new_parent)