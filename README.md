# Set Partitioning - Friends and Enemies Problem

In module 1b we looked at how to construct QUBOs that model friendly and
hostile relationships. We also saw that we can sum up the relationships 
in a social network to model the network. When we solve this problem on
a D-Wave solver, the solution partitions the graph into two sets such that the 
number of hostile relationships within a set is minimized. 

In this exercise you will construct a QUBO or BQM for arbitrarily sized social networks
and solve these networks on both a QPU and BQM hybrid solver. You will also 
explore the limit of the QPU solver to see why the hybrid solvers are useful.

When you run the program it will generate three graphs. One will show the problem and
two will display the solution. For example, if you construct a QUBO or BQM properly
for a 10 node graph, you may see something like this

![graphs](readme_images/graphs.png "graphs")

where 
* red edges = hostile relationships
* green edges = friendly relationships
* black nodes = nodes in the problem 
* yellow nodes = nodes in one group (in the solution)
* blue nodes = nodes in the second group (in the solution)

As a reminder the QUBOs for each relationship are as follows.

Friendly relationship

![friendly](readme_images/friendly.png "friendly")

Hostile relationship

![hostile](readme_images/hostile.png "hostile")       

##Instructions:
There are two parts to this assignment.

###Exercise 1:  
In this exercise you will build a QUBO for the friends and enemies problem on a random
graph. The QUBO will be submitted to the QPU. Feel free to experiment
 with the size of the graph and remember to make your code scalable so you don't have to
 rewrite the QUBO for every new graph. It's worth noting that the EmbeddingComposite can
 take a few minutes to find an embedding for really big graphs.
  
 Open up the `friends_enemies_qpu.py` file. You will need to
 
1. Add your API token
2. Construct the QUBO for the friends and enemies problem 
3. Run the problem on the QPU

Hint:  
* Use random.choice() to randomly assign a friendly or hostile relationship to an edge
    
###Exercise 2:  
In this exercise you will build a BQM for the friends and enemies problem on a random graph.
This time you will submit the problem to the BQM hybrid solver. Although the work you did
in exercise 1 will come in handy, pay close attention to the differences between a dictionary
and the type of BQM you're asked to create. 

Open up the `friends_enemies_hybrid.py` file. You will need to

1. Create a graph that's too large to run on the QPU
2. Construct a BQM for the friends and enemies problem
3. Run the problem on the hybrid sampler

Hints:  
* Use random.choice() to randomly assign a friendly or hostile relationship to an edge
* Check the dimod documentation to learn how and when to use AdjVectorBQM

####Resources
1. Ocean documentation: https://docs.ocean.dwavesys.com/en/latest/index.html
2. BQM documentation: https://docs.ocean.dwavesys.com/en/latest/docs_dimod/reference/bqm.html#usage
3. Random python module: https://docs.python.org/3/library/random.html
4. How to use the timeout parameter with the embedding tools: 
https://support.dwavesys.com/hc/en-us/community/posts/360052799433/comments/1500000168162
5. Maximum cut code example: https://github.com/dwave-examples/maximum-cut