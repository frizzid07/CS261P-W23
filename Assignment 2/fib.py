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
        pass

    def get_roots(self) -> list:
        return self.roots

    def insert(self, val: int) -> FibNode:
        newNode = FibNode(val)
        self.roots.append(newNode)
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
        self.roots.pop()

    def delete_min(self) -> None:
        # Removing deleted node from list of roots
        self.delete_root_by_index(self.min_index)

        # Merging children of deleted note to list of roots
        if self.min_node.get_children():
            for child in self.min_node.get_children():
                child.parent = None
                child.flag = False
                self.roots.append(child)
        
        # Improving Forest Structure
        for pos_1, first_root in enumerate(self.roots[:-1]):
            if len(self.roots) == pos_1+1:
                break
            for pos_2, second_root in enumerate(self.roots[pos_1+1:]):
                if len(first_root.get_children()) == len(second_root.get_children()):
                    if first_root.get_value_in_node()<=second_root.get_value_in_node():
                        first_root.children.append(second_root)
                        second_root.parent = first_root
                        self.delete_root_by_index(pos_2)
                    else:
                        second_root.children.append(first_root)
                        first_root.parent = second_root
                        self.delete_root_by_index(pos_1)

        # Finding the new best root
        self.min_node = self.find_best_root()

    def find_min(self) -> FibNode:
        return self.min_node

    def decrease_priority(self, node: FibNode, new_val: int) -> None:
        if node.parent is None:
            if new_val < self.min_node.get_value_in_node():
                self.min_node = node
                for ind, root in enumerate(self.roots):
                    if root == node:
                        self.min_index = ind
            node.val = new_val
        else:
            if node.parent.parent is not None:
                if not node.parent.get_flag():
                    node.parent.flag = True
                else:
                    self.decrease_priority(node.parent, node.parent.val)
            node.parent.children.remove(node)
            self.roots.append(node)
            node.parent = None


    # feel free to define new methods in addition to the above
    # fill in the definitions of each required member function (above),
    # and for any additional member functions you define