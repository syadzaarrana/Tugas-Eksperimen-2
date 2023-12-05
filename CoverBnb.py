import networkx as nx
import DatasetHelper

# USE THE ADJACENCY LIST TO CREATE A GRAPH
def create_graph(adj_list):
	G = nx.Graph()
	for i in adj_list:
		for j in adj_list[i]:
			G.add_edge(i, j)
	return G

def BnB(adj_list):
	# CREATE GRAPH
	G = create_graph(adj_list)

	# INITIALIZE SOLUTION VC SETS AND FRONTIER SET TO EMPTY SET
	OptVC = []
	CurVC = []
	Frontier = []
	neighbor = []

	# ESTABLISH INITIAL UPPER BOUND
	UpperBound = G.number_of_nodes()

	CurG = G.copy()  # make a copy of G
	# sort dictionary of degree of nodes to find node with highest degree
	v = find_maxdeg(CurG)

	# APPEND (V,1,(parent,state)) and (V,0,(parent,state)) TO FRONTIER
	Frontier.append((v[0], 0, (-1, -1)))  # tuples of node,state,(parent vertex,parent vertex state)
	Frontier.append((v[0], 1, (-1, -1)))

	while Frontier!=[]:
		(vi,state,parent)=Frontier.pop() #set current node to last element in Frontier
		backtrack = False
		
		if state == 0:  # if vi is not selected, state of all neighbors=1
			neighbor = CurG.neighbors(vi)  # store all neighbors of vi
			for node in list(neighbor):
				CurVC.append((node, 1))
				CurG.remove_node(node)  # node is in VC, remove neighbors from CurG
		elif state == 1:  # if vi is selected, state of all neighbors=0
			CurG.remove_node(vi)  # vi is in VC,remove node from G
		else:
			pass

		CurVC.append((vi, state))
		CurVC_size = VC_Size(CurVC)
		if CurG.number_of_edges() == 0:  # end of exploring, solution found
			if CurVC_size < UpperBound:
				OptVC = CurVC.copy()
				UpperBound = CurVC_size
			backtrack = True
				
		else:   #partial solution
			CurLB = Lowerbound(CurG) + CurVC_size

			if CurLB < UpperBound:  # worth exploring
				vj = find_maxdeg(CurG)
				Frontier.append((vj[0], 0, (vi, state)))#(vi,state) is parent of vj
				Frontier.append((vj[0], 1, (vi, state)))
			else:
				# end of path, will result in worse solution,backtrack to parent
				backtrack=True


		if backtrack==True:
			if Frontier != []:	#otherwise no more candidates to process
				nextnode_parent = Frontier[-1][2]	#parent of last element in Frontier (tuple of (vertex,state))

				# backtrack to the level of nextnode_parent
				if nextnode_parent in CurVC:
					
					id = CurVC.index(nextnode_parent) + 1
					while id < len(CurVC):	#undo changes from end of CurVC back up to parent node
						mynode, mystate = CurVC.pop()	#undo the addition to CurVC
						CurG.add_node(mynode)	#undo the deletion from CurG
						
						# find all the edges connected to vi in Graph G
						# or the edges that connected to the nodes that not in current VC set.
						
						curVC_nodes = list(map(lambda t:t[0], CurVC))
						for nd in G.neighbors(mynode):
							if (nd in CurG.nodes()) and (nd not in curVC_nodes):
								CurG.add_edge(nd, mynode)	#this adds edges of vi back to CurG that were possibly deleted

				elif nextnode_parent == (-1, -1):
					# backtrack to the root node
					CurVC.clear()
					CurG = G.copy()
				else:
					print('error in backtracking step')

	return OptVC

#TO FIND THE VERTEX WITH MAXIMUM DEGREE IN REMAINING GRAPH
def find_maxdeg(g):
	deglist = g.degree
	deglist_sorted = sorted(deglist, key=lambda x: x[1], reverse=True)  # sort in descending order of node degree
	v = deglist_sorted[0]  # tuple - (node,degree)
	return v

#EXTIMATE LOWERBOUND
def Lowerbound(graph):
	lb=graph.number_of_edges() / find_maxdeg(graph)[1]
	lb=ceil(lb)
	return lb

def ceil(d):
    if d > int(d):
        return int(d) + 1
    else:
        return int(d)
    
#CALCULATE SIZE OF VERTEX COVER (NUMBER OF NODES WITH STATE=1)
def VC_Size(VC):
	vc_size = 0
	for element in VC:
		vc_size = vc_size + element[1]
	return vc_size

root = DatasetHelper.generate_tree(10)
adj = DatasetHelper.get_tree_adj(root)
DatasetHelper.print_tree(root)
print(adj)
print(BnB(adj))