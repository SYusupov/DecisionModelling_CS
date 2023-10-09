import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from itertools import combinations, combinations_with_replacement
import string
from collections import defaultdict, deque
import sys

def reading_excel(input):
    """
    read matrix form of binary relation which is in excel
    input
    - is an excel file where rows and columns are the beginning and the end of the relation respectively
    - should not have headers(labels for the nodes) for both columns and rows
    
    matrix_np - the matrix form of the binary relation as numpy array
    nodes - alphabetical labels of the nodes"""

    df = pd.read_excel(input, header=None)
    matrix_np = df.to_numpy()

    # getting node labels as letters
    nodes = list(string.ascii_lowercase)[:len(matrix_np)]

    return matrix_np, nodes


def Visualizebinaryrelation(matrix_np,nodes):
    """
    visualize the binary relation in a graphical form
    """
    G = nx.DiGraph()

    # Adding nodes
    for i in range(len(matrix_np)):
        G.add_node(nodes[i])
    
    # Adding edges based on the binary relation matrix
    for i in range(len(matrix_np)):
        for j in range(len(matrix_np)):
            if matrix_np[i][j] == 1:
                G.add_edge(nodes[i], nodes[j])
    
    # Draw the graph of the relation
    nx.draw(G, with_labels=True, arrows=True)
    plt.show(block=True)


def ReflexiveCheck(matrix_np,nodes):
    """check reflexivity - if all nodes have edges to themselves"""
    for i in range(len(matrix_np)):
        if matrix_np[i][i] == 0:
            print(f"Reflexive? No. Node #{nodes[i]} has no edge to itself")
            return False
    print("Reflexive? Yes.")
    return True


def CompleteCheck(matrix_np,nodes):
    """check completeness - if all pairs of nodes have at least one edge with each other"""
    for (i,j) in combinations(range(len(matrix_np)), 2):
        if matrix_np[i][j] == 0 and matrix_np[j][i] == 0:
            print(f"Complete? No. No relation for nodes #{nodes[i]} and #{nodes[j]}")
            return False
        
    if ReflexiveCheck(matrix_np,nodes) == False:
        print(f"Complete? No. Reflexivity is not supported")
        return False
    
    print(f"Complete? Yes.")
    return True


def AsymmetricCheck(matrix_np,nodes):
    """check if asymmetric - each pair of nodes can have at most one relation with each other"""
    for (i,j) in combinations(range(len(matrix_np)), 2):
        if matrix_np[i][j] == 1 and matrix_np[j][i] == 1:
            print(f"Asymmetric? No. Node combination {nodes[i]}, {nodes[j]} have both side relations")
            return False
    
    # check if nodes have relations to itself 
    for i in range(len(matrix_np)):
        if matrix_np[i][i] == 1:
            print(f"Asymmetric? No. Node {nodes[i]} has a relation to itself")
    
    print("Asymmetric? Yes.")
    return True


def SymmetricCheck(matrix_np,nodes):
    """check if symmetric - each pair of nodes have either 2 or 0 relations with each other"""
    for (i,j) in combinations(range(len(matrix_np)), 2):
        if not (
            (matrix_np[i][j]==1 and matrix_np[j][i]==1) or 
            (matrix_np[i][j]==0 and matrix_np[j][i]==0)
        ):
            print(f"Symmetric? No. Node combination {nodes[i]}, {nodes[j]} don't have both side relations")
            return False
    print("Symmetric? Yes.")
    return True


def AntisymmetricCheck(matrix_np,nodes):
    """check if antisymmetric"""
    for (i,j) in combinations(range(len(matrix_np)), 2):
        if (matrix_np[i][j]==1 and matrix_np[j][i]==1):
            print(f"Antisymmetric? No. Node combination {nodes[i]}, {nodes[j]} have both side relations")
            return False
    print("Antisymmetric? Yes.")
    return True


def TransitiveCheck(matrix_np, nodes):
    """check if transitive: xRy, yRz --> xRz"""
    for x in range(len(matrix_np)):
        for y in range(len(matrix_np)):

            # checking the first condition
            if matrix_np[x][y] == 1:

                # checking the 2nd and 3rd conditions
                for z in range(len(matrix_np)):
                    if (matrix_np[y][z]==1 and matrix_np[x][z]==0):
                        print(f"Transitive? No. Node combination {nodes[x]}, {nodes[y]}, {nodes[z]} doesn't satisfy the condition.")
                        return False
    print("Transitive? Yes.")
    return True


def NegativetransitiveCheck(matrix_np, nodes):
    """check if negatively transitive: not(xRy), not(yRz) --> not(xRz)"""
    for x in range(len(matrix_np)):
        for y in range(len(matrix_np)):

            # checking the 1st condition
            if matrix_np[x][y] == 0:

                # checking the 2nd and 3rd conditions
                for z in range(len(matrix_np)):
                    if matrix_np[y][z] == 0 and matrix_np[x][z] == 1:
                        print(f"NegativelyTransitive? No. Node combination {nodes[x]}, {nodes[y]}, {nodes[z]} doesn't satisfy the condition.")
                        return False
    print("NegativelyTransitive? Yes.")
    return True


def CompleteOrderCheck(matrix_np, nodes):
    """check if total order: complete, antisymmetric and transitive"""
    if CompleteCheck(matrix_np, nodes)==False:
        print("TotalOrder? No. It's not complete.")
        return False
    if AntisymmetricCheck(matrix_np, nodes)==False:
        print("TotalOrder? No. It's not antisymmetric.")
        return False
    if TransitiveCheck(matrix_np, nodes)==False:
        print("TotalOrder? No. It's not transitive.")
        return False
    print("TotalOrder? Yes.")
    return True


def CompletePreOrderCheck(matrix_np, nodes):
    """check if complete pre-order: complete and transitive"""
    if CompleteCheck(matrix_np, nodes)==True and TransitiveCheck(matrix_np,nodes)==True:
        print("Complete Pre-order? Yes.")
        return True
    print("Complete Pre-order? No.")
    return False


def StrictRelation(matrix_np):
    """getting the asymmetric part of the relation: for a and b, aRb but NOT bRa"""
    asymmetric_np =np.zeros((len(matrix_np),len(matrix_np)))

    for (i,j) in combinations_with_replacement(range(len(matrix_np)),2):
        if matrix_np[i][j]==1 and matrix_np[j][i]==0:
            asymmetric_np[i][j] = 1

        elif matrix_np[i][j]==0 and matrix_np[j][i]==1:
            asymmetric_np[j][i] = 1

    return asymmetric_np


def IndifferenceRelation(matrix_np):
    """getting the symmetric part of the relation: for a and b, aRb AND bRa, includes aRa"""
    symmetric_np = np.zeros((len(matrix_np),len(matrix_np)))

    for (i,j) in combinations_with_replacement(range(len(matrix_np)),2):
        if matrix_np[i][j]==1 and matrix_np[j][i]==1:
                symmetric_np[i][j] = 1
                symmetric_np[j][i] = 1

    return symmetric_np


def Topologicalsorting(matrix_np):
    """Perform topological sorting
    returns the order if you have no cycles, returns None if you have cycles"""
    topological_order = [] # to store the final order

    # Counting number of incoming edges for each node
    # changes with each step
    n_incoming_edges = defaultdict(int)
    for i in range(len(matrix_np)):
        for j in range(len(matrix_np)):
            if i == j: # edge to itself is not important
                continue
            n_incoming_edges[j] += matrix_np[i][j]
    # print(n_incoming_edges)

    # Store the nodes with no incoming edges in a queue
    no_incoming = deque([i for i, n_incoming in n_incoming_edges.items() if n_incoming==0])
    # print(no_incoming)

    while no_incoming:
        curr_i = no_incoming.popleft()
        topological_order.append(curr_i)

        # update incoming edges for the remaining nodes 
        # when removign the current node
        for j in range(len(matrix_np)):

            if j in topological_order:
                continue
            
            if matrix_np[curr_i][j] == 1:
                n_incoming_edges[j] -= 1
                if n_incoming_edges[j] == 0:
                    no_incoming.append(j)
        # print('n_incoming',n_incoming_edges)
        # print('no_incoming', no_incoming)
        # print('order', topological_order)
    
    # the node without incoming edges finished too soon --> cycles
    if len(topological_order) != len(matrix_np):
        print("Couldn't compute topological order. The relation has cycles.")
        return None # so return None
    else:
        print(f"Topological order: {topological_order}")
        return topological_order

if __name__ == "__main__":
    """run as python check_binaryRelation_properties.py <filename>
    where <filename> is the name of the spreadsheet to take the binary relation from"""
    # the path to the excel file
    input = sys.argv[1]

    # input = 'matrix_input.xlsx'
    matrix_np,nodes = reading_excel(input)
    Visualizebinaryrelation(matrix_np,nodes)
    ReflexiveCheck(matrix_np,nodes)
    CompleteCheck(matrix_np,nodes)
    AsymmetricCheck(matrix_np,nodes)
    SymmetricCheck(matrix_np,nodes)
    AntisymmetricCheck(matrix_np,nodes)
    TransitiveCheck(matrix_np,nodes)
    NegativetransitiveCheck(matrix_np, nodes)
    CompleteOrderCheck(matrix_np, nodes)
    CompletePreOrderCheck(matrix_np,nodes)
    asymmetric_np = StrictRelation(matrix_np)
    print(f"Asymmetric part:\n {asymmetric_np}")
    symmetric_np = IndifferenceRelation(matrix_np)
    print(f"Symmetric part:\n {symmetric_np}")
    topological_order = Topologicalsorting(matrix_np)