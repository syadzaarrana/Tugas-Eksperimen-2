import math
import DatasetHelper

def get_max_degree(vertex_degrees):
    return vertex_degrees.pop(0)

def get_lower_bound(adj):
    max_degree = get_max_degree(DatasetHelper.get_vertex_degrees(adj))[1]

    if max_degree == 0:
        return len(adj) - 1
    
    return math.ceil((len(adj)-1)/max_degree)

def get_vc_size(cover):
	vc_size = 0
	for node in cover:
		vc_size = vc_size + node[1]
	return vc_size

def add_node(adj, deleted_vertices, node):
    edges = deleted_vertices[node]
    deleted_neighbor = []
    
    for x, neighbors in adj.items():
        if x in edges:
            neighbors.append(node)
    
    adj[node] = [node for node in edges if node not in deleted_neighbor]

    return adj

def remove_node(adj, node):
    if node in adj:
        del adj[node]

        for x, neighbors in adj.items():
            adj[x] = [neighbor for neighbor in neighbors if neighbor != node]

    return adj

def min_size_vc(adj):
    cur_adj = adj.copy()
    cur_vertex_degrees = DatasetHelper.get_vertex_degrees(adj)

    opt_cover = []
    cur_cover = []

    deleted_vertices = {}

    v = get_max_degree(cur_vertex_degrees)[0]
    frontier_set = [(v, 0, (-1, -1)), (v, 1, (-1, -1))]
    
    upper_bound = len(cur_adj)

    while frontier_set != []:
        current = frontier_set.pop()
        node = current[0]
        state = current[1]
        cur_cover.append((node, state))
        
        backtrack = False

        if state == 0:
            neighbors = cur_adj[node]
            for neighbor in neighbors:
                cur_cover.append((neighbor, 1))
                deleted_vertices[neighbor] = adj[neighbor]
                cur_adj = remove_node(cur_adj, neighbor)
        
        elif state == 1:
            deleted_vertices[node] = cur_adj[node]
            cur_adj = remove_node(cur_adj, node)
        
        else:
            pass

        vc_size = get_vc_size(cur_cover)

        if all(not bool(v) for v in cur_adj.values()):
            if vc_size < upper_bound:
                opt_cover = cur_cover.copy()
                upper_bound = vc_size
            
            backtrack = True
        
        else:
            if get_lower_bound(cur_adj) + vc_size < upper_bound:
                cur_vertex_degrees = DatasetHelper.get_vertex_degrees(cur_adj)
                vj = get_max_degree(cur_vertex_degrees)[0]
                frontier_set = frontier_set + [(vj, 0, (node, state)), (vj, 1, (node, state))]
            
            else:
                backtrack = True
        
        if backtrack == True and frontier_set != []:
            next_parent = frontier_set[-1][2]

            if next_parent in cur_cover:
                index = cur_cover.index(next_parent) + 1
                while index < len(cur_cover):
                    to_add = cur_cover[index][0]
                    cur_cover.pop(index)

                    if to_add not in cur_adj.keys():
                        cur_adj = add_node(cur_adj, deleted_vertices, to_add)
            
            else:
                cur_cover = []
                cur_adj = adj.copy()
                deleted_vertices = {}
    
    return opt_cover

def vc_bnb(adj):
    vc = min_size_vc(adj)
    solution = []
    for element in vc:
        if element[1]==1:
            solution.append(element[0])
    
    return solution, len(solution)
