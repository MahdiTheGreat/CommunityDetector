# CommunityDetector
This is an algorithm for finding communities within an undirected graph, especially useful for networking.

A community in a graph is called a subgraph if the number of edges between the internal vertices of the subgraph is more than the edges that go out of that subgraph (to other vertices in the graph). For example, the figure below shows the communities in a graph:

![image](https://github.com/MahdiTheGreat/CommunityDetector/assets/47212121/0bafd8d4-1150-4b83-9545-b8c174e8f63d)

The algorithm works by deleting one edge at a time, based on the weight calculated(which if we consider the Cij the weight of the edge connecting the nodes i and j, and Zi the degree of the node i) with the below formula:

![image](https://github.com/MahdiTheGreat/CommunityDetector/assets/47212121/5c4aaf0e-ab75-46ec-9bb5-6d86bac1228c)

which is based on how much they were present in the three-node rounds and whether they are between two communities (which we check by calculating the min of the two degrees of the edge nodes in the weight calculation). The logic of this algorithm is based on the fact that in communities, nodes have many relationships with each other, and each node is connected with a relatively significant number of nodes in that community, and therefore there are many cycles between existing nodes in the community. As we know, each cycle must at least be between three nodes, and in fact, we want to find the communities in which the maximum number of overlaps from three-node rounds exist.

Python dictionary is used to store the edges, which is like a hashmap and the access time to each of the elements is O(1) which is very suitable for us, considering that each of the edges has its own ID, which is the nodes that this edge is located between, and we can also use this fact to calculate the number of three-node cycles that an edge participates in, by seeing if there are nodes between the nodes related to the edge (stored in the edge class), which are connected to both, and we have the number We get these nodes, and we also store these numbers in the edge class to adjust the weights of the edges.

For the implementation of edges, a class has been used, which contains its weight and the number of cycles that it's participating in. To store the graph, we used a 2-dimensional matrix, each row of which is a dictionary, which, for example, row i, stores the nodes with which node i is connected. Again, because each One of the nodes has its own ID, we can easily use a dictionary, and the reason that the first layer of the matrix (the matrix that stores the rows) is also not a dictionary, is that none of the rows will ever be deleted and their place is specific, while the nodes in each row, depending on whether the related edge is present or not, may be deleted, and for this reason, the order may be messed up. Note that if two nodes are connected, then each of the nodes is in the other nodes row and basically an edge is represented in two places and the reason for this is that our graph is undirected.

To implement the nodes, we also use a class, which includes information such as the degree of the node. Also an array is used as a stack in the bfs or breath first search function to check whether the graph is connected or not, and the quicksort function is implemented in an iterative way, to prevent stack overflow as there is a limit for the number of recursions in Python. Finally, queue is also used for multi-core programming, due to the fact that this structure manages shared variables. 

The steps of the algorithm are as follows:
1. Weight calculation for all edges
2. Ascending sorting of edges based on the calculated weight.
3. Remove the edge with the smallest weight from the graph.
4. If the graph is divided into two parts, then the algorithm ends.
5. Calculation of the weight for the edges whose score changes after removing the edge in the third step. (Obviously, the weights of some edges in the graph change in each loop of running the algorithm, the edges that were connected to the nodes of the deleted edge and the weight of the remaining edges of the graph remain constant and do not need to be recalculated.) We can reduce the number of recalculations by considering the edges that are connected to two deleted edge nodes, and whether the deleted edge had formed a cycle with these edges and if so, reduce the number of cycles of these edges by one and not calculate the number of their cycles again. 
7. return to the first step.

The input of the program is a file in CSV format where each node is represented by a natural number and each line represents an edge of the input graph. The whole file must be read at once and loaded into the RAM memory. 

The following algorithms are implemented for sorting:
. Insertion sort
. Bubble sort
. Merge Sort
. Quick Sort

We can also use the min function,which improves the complexity.
At the time of execution of the program, the desired file containing graph information and the name of the selected algorithm for creating a map should be input. for example:

1. RUN Bubble test1.csv
2. RUN Quick test2.csv
3. RUN Merge test1.csv
4. RUN Insertion test2.csv

The output of each execution of the program contains the following items:

1. The time spent to read the graph information from the CSV file and store it in the Adjacency list of the graph.
2. The time spent for the initial calculation of the weights.
3. The graph of the time spent in the sorting step from the beginning to the end of the algorithm.
4. A CSV file whose lines contain the number of each vertex along with its community (A or B)

Two versions of the algorithm exist, one parallel, which uses multiprocessing(CommunityDetectorPar.py), and one which only works with one core.
The tests and results are in csv format, which is compatible with the Gephi software.
Keep in mind that the algorithm stops when the graph becomes disconnected, and in order to continue the algorithm, we have to run the algorithm recursively on the disconnected parts 
or communities.

# Testing
Due to the large size of the test files, as well as the fact that Python's speed is low, small test files have been used, which include communitytest files, in which communities can be seen by eye, and after Do the test
You can see that in the resulting graph, the communities are separated. For example:

![image](https://github.com/MahdiTheGreat/CommunityDetector/assets/47212121/75a6d110-0eca-436f-ab80-48cddc16c619)

And now after running the algorithm:

![image](https://github.com/MahdiTheGreat/CommunityDetector/assets/47212121/8cf0ae35-2c11-4f4d-a73d-37ead9c2bff9)

The example above is related to the "communitytest bubblesort run" file.



