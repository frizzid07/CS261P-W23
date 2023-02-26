# explanations for member functions are provided in requirements.py
from __future__ import annotations

class FibNode:
    def __init__(self, val: int):
        self.val = val
        self.parent = None
        self.children = []
        self.flag = False

    def get_value_in_node(self):
        return self.val

    def get_children(self):
        return self.children

    def get_flag(self):
        return self.flag

    def __eq__(self, other: FibNode):
        return self.val == other.val

class FibHeap:
    def __init__(self):
        # you may define any additional member variables you need
        self.roots = []
        self.min_node = None
        self.min_index = None
        self.nodes = 0

    def get_roots(self) -> list:
        return self.roots

    def insert(self, val: int) -> FibNode:
        newNode = FibNode(val)
        self.roots.append(newNode)
        self.nodes += 1
        if self.min_node is None or val < self.min_node.get_value_in_node():
            self.min_node = newNode
            self.min_index = len(self.roots)-1
        return newNode

    def find_best_root(self) -> FibNode:
        min_node = float("inf")
        for ind, root in enumerate(self.roots):
            if root.get_value_in_node()<min_node:
                min_node = root.get_value_in_node()
                self.min_index = ind
        return self.roots[self.min_index]

    def delete_root_by_index(self, index: int) -> None:
        self.roots[index], self.roots[-1] = self.roots[-1], self.roots[index]
        self.nodes -= 1
        self.roots.pop()

    def delete_min(self) -> None:
        # Merging children of deleted note to list of roots
        if self.min_node.get_children():
            for child in self.min_node.get_children():
                child.parent = None
                child.flag = False
                self.roots.append(child)

        # Removing deleted node from list of roots
        self.delete_root_by_index(self.min_index)
        self.min_node, self.min_index = None, float("inf")

        # Improving Forest Structure
        roots_array = self.roots.copy()
        degree = [None]*(self.nodes+1)

        while roots_array:
            last = roots_array.pop()
            num_children = len(last.get_children())
            if degree[num_children] is None:
                degree[num_children] = last
            else:
                temp = degree[num_children]
                degree[num_children] = None
                if last.val >= temp.val:
                    temp.children.append(last)
                    last.parent = temp
                    roots_array.append(temp)
                else:
                    last.children.append(temp)
                    temp.parent = last
                    roots_array.append(last)
        
        self.roots = [root for root in degree if root is not None]

        # Finding the new best root
        self.min_node = self.find_best_root()

    def find_min(self) -> FibNode:
        return self.min_node

    def make_root(self, node: FibNode) -> None:
        node.parent = None
        node.flag = False
        self.roots.append(node)

    def promote(self, node: FibNode) -> None:
        if node.parent is not None:
            parent_node = node.parent
            parent_node.children.remove(node)
            self.make_root(node)
            self.min_node = self.find_best_root()
            if parent_node.parent is not None:
                if parent_node.flag:
                    self.promote(parent_node)
                else:
                    parent_node.flag = True

    def decrease_priority(self, node: FibNode, new_val: int) -> None:
        node.val = new_val
        if node.parent is None:
            if new_val < self.min_node.get_value_in_node():
                self.min_node = node
                for ind, root in enumerate(self.roots):
                    if root == node:
                        self.min_index = ind
        else:
            self.promote(node)


    # feel free to define new methods in addition to the above
    # fill in the definitions of each required member function (above),
    # and for any additional member functions you define