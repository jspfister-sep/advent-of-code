import sys

class Node:
    def __init__(self, num_children, num_metadata):
        self.num_children = num_children
        self.num_metadata = num_metadata
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)
        
    def add_metadata(self, metadata):
        self.metadata = metadata
        
    def is_complete(self):
        return self.num_children == 0 or len(self.children) == self.num_children
        
    def value(self):
        if self.num_children == 0:
            return sum(self.metadata)
        else:
            value = 0
            for index in self.metadata:
                if 0 < index <= self.num_children:
                    value += self.children[index - 1].value()
            return value
        
    def __str__(self):
        return '{} {}'.format(self.num_children, self.metadata)
        
def read_metadata(file, node):
    node.add_metadata(read_n_numbers(file, node.num_metadata))
    
def read_n_numbers(file, n):
    numbers = []
    stream = ''
    while n > 0:
        character = file.read(1)
        if not character or not character.isdigit():
            numbers.append(int(stream))
            stream = ''
            n -= 1
        else:
            stream += character
    return numbers
            
def read_node(file):
    info = read_n_numbers(file, 2)
    if info:
        node = Node(info[0], info[1])
        if node.num_children == 0:
            read_metadata(file, node)
        return node
    else:
        return None

def read_nodes_from_file(file):
    pending_nodes = []
    complete_nodes = []
    
    while(pending_nodes or not complete_nodes):
        node = read_node(file)
        if node.is_complete():
            pending_nodes[-1].add_child(node)
            complete_nodes.append(node)
            while pending_nodes and pending_nodes[-1].is_complete():
                read_metadata(file, pending_nodes[-1])
                node = pending_nodes.pop()
                if pending_nodes:
                    pending_nodes[-1].add_child(node)
                complete_nodes.append(node)
        else:
            pending_nodes.append(node)
            
    return complete_nodes

with open(sys.argv[1], 'r') as file:
    nodes = read_nodes_from_file(file)
        
print(nodes[-1].value())