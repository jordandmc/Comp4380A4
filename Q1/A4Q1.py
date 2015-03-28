import sys
import os


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
                tree.print_tree(tree.root)


def parse_input(file_name):
    with open(file_name) as input_file:
        instructions = input_file.readlines()
    return instructions


class Node:
    def __init__(self):
        self.keys = []  # Contains the values in index/leaf nodes
        self.data = []  # Points to nodes below this one
        self.parent = None
        self.isLeaf = False


class BPlusTree:
    def __init__(self, degree):
        self.root = None
        self.degree = degree
        self.print_num = 0

    def search(self, value):
        print("\tsearching...")
        return self.recursive_search(self.root, value)

    def recursive_search(self, node, value):
        if node is None: # Empty Tree
            return None
        elif node.isLeaf:
            return node  # Found the leaf node the value could be in, return this node
        else:
            for index, key in node.keys:
                if value < key:
                    return recursive_search(self, data[index], value)  # Search left

            # Bigger than every key in index, Go down the far right
            return recursive_search(self, data[len(data)-1], value)

    def insert(self, data):
        print("insert " + data)
        node = self.search(data)
        if node is None:
            print("\tnode is none, creating root")

    def split(self):
        print("split")

    def delete(self, data):
        print("delete " + data)

    def merge(self):
        print("merge")

    def print_tree(self, root):
        print("B+tree #" + str(self.print_num) + " with order d=" + str(self.degree))
        self.print_num += 1

if __name__ == '__main__':
    main()