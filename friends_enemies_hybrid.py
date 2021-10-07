# Copyright 2021 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

## ------- import packages -------
import random

import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

import dimod
import networkx as nx
from dwave.system import LeapHybridSampler

def get_token():
    '''Returns personal access token. Only required if submitting to autograder.'''
    
    # TODO: Enter your token here
    return 'YOUR-TOKEN-HERE'

def get_graph():
    """ Randomly generats a graph that represents a social network (nodes will
    represent people and edges represent relationships between people)
    """

    # TODO: Change this parameter to change the size of the graph
    graph_size = 4

    # Generate a random graph (with a 60% probability of edge creation)
    G = nx.gnp_random_graph(graph_size, 0.60)

    return G

# TODO: Add code here to define a BQM
def get_bqm(G):
    """ Randomly assign a friendly or hostile relationship to edges in the dictionary.

    Args:
        G: (:obj:`networkx.Graph`):
            A networkx graph where the nodes represent people and the
            edges represent relationships between people

    Returns:
        :obj:`BinaryQuadraticModel`: A binary-valued binary quadratic model
    """
    # Build the BQM

    # Add linear and quadratic biases to the BQM

    return bqm


# TODO: Add the hybrid sampler and return the sampleset
def run_on_hybrid(bqm):
    """ Submits the BQM to the BQM hybrid sampler and returns the sampleset

    :param bqm: BQM for the problem
    :return: Sampleset from the hybrid sampler

    Args:
        bqm: (:obj:`BinaryQuadraticModel`):
            The BQM for the friends and enemies problem

    Returns:
        :obj:`SampleSet`: The sampleset from the hybrid sampler
    """

    # Define the sampler and submit the BQM

    return

def visualize(G, bqm, sampleset, problem_filename, solution_filename):
    """ Creates and saves plots that show the problem and solution returned in the lowest
    energy sample in the sampleset. It also prints the solution in a bipartite layout
    with the filename bipartite_solution_filename.

    Args:
        G: (:obj:`networkx.Graph`):
            The Networkx graph of the friends and enemies problem

        BQM: (:obj:`BinaryQuadraticModel`):
            The BQM for the friends and enemies problem

        sampleset: (:obj:`SampleSet`):
            The sampleset from the QPU sampler

        problem_filename: (:obj:`Str`):
            The filename for the graph of the problem

        solution_filename: (:obj:`Str`):
            The filename for the graph of the solution
    """
    # Get the best solution to display
    sample = sampleset.first.sample

    # Assign colors to the edges based on friend or enemy
    edgecolors = ['g' if bqm.get_quadratic(a, b) < 0 else 'r' if bqm.get_quadratic(a, b) > 0 else 'b' for a, b in
                  G.edges()]

    # Assign colors to nodes based on set membership
    blue = '#2a7de1'
    yellow = '#fcba03'
    
    for i in G.nodes():
        if i not in sample:
            sample[i] = 0
            
    nodecolors = [blue if sample[i] == 0 else yellow for i in G.nodes()]

    # Get a subset of the original graph (just the nodes assigned to group 1)
    set0 = [node for node in sample if sample[node] == 0]
    set1 = G.nodes - set0

    # Visualize the problem and results
    plt.figure(0)

    # Save original problem graph
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos=pos, edge_color=edgecolors, with_labels=True, node_color='k', font_color='w')
    plt.savefig(problem_filename, bbox_inches='tight')

    # Save the solution graph
    nx.draw_networkx_nodes(G, pos=pos, node_color=nodecolors)
    plt.savefig(solution_filename, bbox_inches='tight')

    # Save the solution as a bipartite graph
    plt.figure(1)

    pos_1 = nx.circular_layout(G.subgraph(set0), center=(-3, -0.5))
    pos_2 = nx.circular_layout(G.subgraph(set1), center=(3, 1))
    pos = {**pos_1, **pos_2}

    nx.draw_networkx_nodes(G, pos_1, nodelist=set0, node_color=blue)
    nx.draw_networkx_nodes(G, pos_2, nodelist=set1, node_color=yellow)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color=edgecolors)
    nx.draw_networkx_labels(G, pos)

    plt.savefig("partitioned_{}".format(solution_filename), bbox_inches='tight')

def process_sampleset(G, sampleset):
    """ Prints a summary of hostile and friendly edges in each set and between sets.

    Args:
        G: (:obj:`networkx.Graph`):
            The Networkx graph of the friends and enemies problem

        sampleset: (:obj:`SampleSet`):
            The sampleset from the QPU sampler
    """
    # Get the best solution to display
    sample = sampleset.first.sample

    # Get a subset of the original graph (just the nodes assigned to group 1)
    set1_nodes = [node for node in sample if sample[node] == 1]
    subgraph1 = G.subgraph(set1_nodes)
    set0_nodes = list(set(G.nodes()) - set(set1_nodes))
    subgraph0 = G.subgraph(set0_nodes)

    # Get friendly and hostile relationships in set 0
    set0_friendly = 0
    set0_hostile = 0
    for i, j in subgraph0.edges:
        if i != j and bqm.get_quadratic(i, j) < 0:
            set0_friendly += 1
        elif i != j and bqm.get_quadratic(i, j) > 0:
            set0_hostile += 1

    # Get friendly and hostile relationships in set 1
    set1_friendly = 0
    set1_hostile = 0
    for i, j in subgraph1.edges:
        if i != j and bqm.get_quadratic(i, j) < 0:
            set1_friendly += 1
        elif i != j and bqm.get_quadratic(i, j) > 0:
            set1_hostile += 1

    # Get friendly and hostile relationships between the sets
    cut_edges = G.edges - subgraph0.edges - subgraph1.edges
    cut_friendly = 0
    cut_hostile = 0
    for i, j in cut_edges:
        if i != j and bqm.get_quadratic(i, j) < 0:
            cut_friendly += 1
        elif i != j and bqm.get_quadratic(i, j) > 0:
            cut_hostile += 1

    # Print the results
    print('-' * 60)
    print('{:>15s}{:>15s}{:^15s}'.format('Set', 'Friendly', 'Hostile'))
    print('-' * 60)

    print('{:>15s}{:>15s}{:^15s}'.format('0', str(set0_friendly), str(set0_hostile)))
    print('{:>15s}{:>15s}{:^15s}'.format('1', str(set1_friendly), str(set1_hostile)))
    print('{:>15s}{:>15s}{:^15s}'.format('0 -> 1', str(cut_friendly), str(cut_hostile)))

## ------- Main program -------
if __name__ == "__main__":
    # Generate a random graph (with a 75% probability of edge creation)
    G = get_graph()

    # Solve this problem on the BQM hybrid solver
    bqm = get_bqm(G)
    sampleset = run_on_hybrid(bqm)

    if sampleset.variables != []:
        # Visualize results
        visualize(G, Q, sampleset, "qpu_problem_graph.png", "qpu_solution_graph.png")

        # Process results
        process_sampleset(G, sampleset)

    else:
        print("\nNo samples returned.\n")



