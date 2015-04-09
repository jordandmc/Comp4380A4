import sys
import os
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
                tree.insert(value)
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


class BPlusTree:
    def __init__(self, degree):
        self.root = None
        self.degree = degree
        self.print_num = 0

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
        print("insert " + value)
        node = self.search(value)
        if node is None:
            print("    node is none, creating root")
            self.root = Node(keys=[value], is_leaf=True)
        elif self.root == node:
            print("    the root is still a leaf node")
        else:
            print("    insert data and propagate the changes up")

    def split(self):
        print("split")

    def delete(self, value):
        print("delete " + str(value))

        node = self.search(value)
        self.delete_recursive(node, value)


    def delete_recursive(self, node, value):
        if node is None:
            return        
        if value in node.keys:
            node.keys.remove(value)
        if node.parent is None:
            return
        if len(node.keys) >= self.degree:
            return

        self.borrow(node)
        self.merge(node)

    def borrow(self, node):
        parent = node.parent
                    
        node_position = parent.children.index(node)

        if node_position > 0:
            left_sibling = parent.children[node_position - 1]

            if len(left_sibling.keys) > self.degree:
                if node.is_leaf:
                    transfered_key = left_sibling.keys.pop() #highest value in left sibling
                    node.keys.insert(0, transfered_key)
                    parent.keys[node_position - 1] = transfered_key #fix parent's key                
                else:
                    left_to_parent_key = left_sibling.keys.pop()
                    parent_to_node_key = parent.keys.pop()
                    left_to_node_child = left_sibling.children.pop()
                    
                    parent.keys.insert(node_position - 1, left_to_parent_key)
                    node.keys.insert(0, parent_to_node_key)
                    node.children.insert(0, left_to_node_child)
                return
                

        if node_position < len(parent.children) - 1:
            right_sibling = parent.children[node_position + 1]

            if len(right_sibling.keys) > self.degree:
                if node.is_leaf:
                    transfered_key = right_sibling.keys.pop(0)
                    node.keys.append(transfered_key)
                    parent.keys[node_position] = right_sibling.keys[0]
                else:
                    right_to_parent_key = right_sibling.keys.pop(0)
                    parent_to_node_key = parent.keys.pop(0)
                    right_to_node_child = right_sibling.children.pop(0)

                    parent.keys.insert(node_position, right_to_parent_key)
                    node.keys.append(parent_to_node_key)
                    node.children.append(right_to_node_child)    
                return        

    def merge(self, node):
        parent = node.parent
        node_position = parent.children.index(node)
        if len(node.keys) >= self.degree:
            return
        if node_position > 0:
            print("reached merge")
            left_sibling = parent.children[node_position - 1]
            node.keys.extend(left_sibling.keys)
            if not node.is_leaf:
                node.keys.append(parent.keys[node_position - 1])
                left_sibling.children.extend(node.children) #puts children in correct order
                node.children = left_sibling.children
                for child in node.children:
                    child.parent = node

            node.keys.sort()
        
            if parent is self.root and len(parent.keys) == 1:
                self.root = node
                return

            parent.children.remove(left_sibling)
            self.delete_recursive(parent, parent.keys[node_position - 1])
            return

        if node_position < len(parent.children) - 1:
            print("reached merge")
            right_sibling = parent.children[node_position + 1]
            node.keys.extend(right_sibling.keys)
            if not node.is_leaf:
                node.keys.append(parent.keys[node_position])
                node.children.extend(right_sibling.children)
                for child in node.children:
                    child.parent = node
            
            node.keys.sort()

            if parent is self.root and len(parent.keys) == 1:
                self.root = node
                return

            parent.children.remove(right_sibling)
            self.delete_recursive(parent, parent.keys[node_position])
            return

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