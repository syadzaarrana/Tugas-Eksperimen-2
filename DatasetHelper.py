import random

class TreeNode:
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent
        self.children = []

def get_tree_adj(node, adj_list=None):
    if adj_list is None:
        adj_list = {}

    if node is not None:
        neighbors = [child.value for child in node.children] + ([node.parent.value] if node.parent else [])
        adj_list[node.value] = neighbors
        for child in node.children:
            get_tree_adj(child, adj_list)

    return adj_list

def get_vertex_degrees(adj_list):
    vertex_degrees = []

    for vertex, neighbors in adj_list.items():
        degree = len(neighbors)
        vertex_degrees.append((vertex, degree))

    vertex_degrees.sort(key=lambda x: x[1], reverse=True)
    return vertex_degrees

def generate_dataset(num_v1, num_v2):
    root = TreeNode(1)
    vertices = [root]

    for i in range(2, num_v1 + 1):
        parent = random.choice(vertices)
        new_node = TreeNode(i, parent)
        parent.children.append(new_node)
        vertices.append(new_node)
    
    tree1 = get_tree_adj(root)

    for i in range(num_v1 + 1, num_v2 + 1):
        parent = random.choice(vertices)
        new_node = TreeNode(i, parent)
        parent.children.append(new_node)
        vertices.append(new_node)
    
    tree2 = get_tree_adj(root)

    return tree1, tree2

def generate_tree(N):
    root = TreeNode(1)
    vertices = [root]

    for i in range(2, N + 1):
        parent = random.choice(vertices)
        new_node = TreeNode(i, parent)
        parent.children.append(new_node)
        vertices.append(new_node)

    return root

def print_tree(node, level=0):
    if node is not None:
        connection = f" <-- parent is {node.parent.value}" if node.parent is not None else ""
        print("  " * level + f"{node.value}{connection}")
        for child in node.children:
            print_tree(child, level + 1)

# adj1, adj2 = generate_dataset(100, pow(10, 4))
# print(adj1)
# print(adj2)
# print("done")
