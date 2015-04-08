import sys
import os
import math
from collections import deque

def main():
    try:
        degree = int(sys.argv[1])
        file_name = sys.argv[2]
    except(ValueError, IndexError):
        print("*** Error: first arg should be an integer, second arg is the input file")
        print("*** ie. python " + sys.argv[0] + " 1 input.txt")
        sys.exit(2)

    if degree > 0 and os.path.isfile(file_name):
        instructions = parse_input(file_name)

        tree = BPlusTree(degree)
        for operation in instructions:
            op, value = operation.split()
            
            if op.upper() == "INSERT":
                tree.insert(int(value))
            elif op.upper() == "DELETE":
                tree.delete(value)
            elif op.upper() == "PRINT":
                tree.print_tree()


def parse_input(file_name):
    with open(file_name) as input_file:
        instructions = input_file.readlines()
    return instructions

class Node:
    def __init__(self, keys=[], children=[], parent=None, is_leaf=None):
        self.keys = keys  # Contains the values in index/leaf nodes
        self.children = children  # Points to nodes below this one
        self.parent = parent
        self.is_leaf = is_leaf
        self.has_vacancy = True

class BPlusTree:
    def __init__(self, degree):
        self.root = None
        self.degree = degree
        self.print_num = 0
    
    def evaluate_vacancy(self, node):
        if self.degree+1 < len(node.keys):
            node.has_vacancy = False
    
    def search(self, value):
        print("    searching...")
        return self.recursive_search(self.root, value)

    def recursive_search(self, node, value):
        if node is None: # Empty Tree
            return None
        elif node.is_leaf:
            return node  # Found the leaf node the value could be in, return this node
        else:
            for index, key in enumerate(node.keys):
                if value < key:
                    return self.recursive_search(node.children[index], value)  # Search left

            # Bigger than every key in index, Go down the far right
            return self.recursive_search(node.children[len(node.children)-1], value)
    
    def insert(self, value):
        print("insert " + str(value))
        node = self.search(value)
        if node is None:
            print("    node is none, creating root")
            self.root = Node(keys=[value], is_leaf=True)
        else:
            node.keys.append(value)
            node.keys.sort()
            self.evaluate_vacancy(node)
            if not node.has_vacancy:
                self.split(node)

    def split(self, node):
        print("split")
        if not node.has_vacancy:
            half = math.floor(len(node.keys)/2)
            
            if node.is_leaf:
                left_child = Node(keys=node.keys[0:half], is_leaf=True)
                right_child = Node(keys=node.keys[half:len(node.keys)], is_leaf=True)
                parent = node.parent
                if parent is None:
                    parent = Node(keys=[right_child.keys[0]], children=[left_child, right_child], is_leaf=False)
                    self.root = parent
                elif parent.has_vacancy:
                    parent.keys.append(right_child.keys[0])
                    parent.children.remove(node)
                    parent.children.append(left_child)
                    parent.children.append(right_child)
                else:
                    print("parent full")
                    #self.split(parent)
                left_child.parent = parent
                right_child.parent = parent

    def delete(self, value):
        print("delete " + value)

    def merge(self):
        print("merge")

    def print_tree(self):
        print("B+tree #" + str(self.print_num) + " with order d=" + str(self.degree))
        self.print_num += 1

        if self.root is None:
            print("Empty Root\n")
            return

        tree_string = "Root "
        height = 0
        queue = deque([])  # Each entry in the queue will store a list that contains [node, height]
        queue.append([self.root, 0])

        while queue:
            queue_entry = queue.popleft()
            node, node_height = queue_entry[0], queue_entry[1]
            if height != node_height:
                tree_string += "\n"
                height += 1

            if node is not None:
                tree_string += "["
                for key in node.keys:
                    tree_string += " " + str(key)
                    if node.is_leaf:
                        tree_string += "*"
                tree_string += " ]  "

                for child in node.children:
                    queue.append([child, height + 1])

        print(tree_string)

if __name__ == '__main__':
    main()