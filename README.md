# CommunityDetector
this is an algorithm for finding communities within a undirected graph,especially usefull for networking.
A community in a graph is called a subgraph if the number of edges between the internal vertices of the subgraph is more than the edges that go out of that subgraph (to other vertices in the graph). For example, the figure below shows the communities in a graph.

![image](https://github.com/MahdiTheGreat/CommunityDetector/assets/47212121/0bafd8d4-1150-4b83-9545-b8c174e8f63d)

the algorithm works by deleting one edge at a time, based on the weight calculated(which if we consider the Cij the weight of the edge connecting the nodes i and j, and Zi the degree of the node i) with the below formula:

![image](https://github.com/MahdiTheGreat/CommunityDetector/assets/47212121/5c4aaf0e-ab75-46ec-9bb5-6d86bac1228c)

The steps of the algorithm are as follows:
1. weight calculation for all edges
2. Ascending sorting of edges based on the calculated weight.
3. Remove the edge with the smallest weight from the graph.
4. If the graph is divided into two parts, then the algorithm ends.
5. Calculation of the weight for the edges whose score changes after removing the edge in the third step. (Obviously, the weights of some edges in the graph change in each period of running the algorithm, and the weight of the remaining edges of the graph remains constant and does not need to be recalculated.)
6. return to the first step.

The input of the program is a file in CSV format where each vertex is represented by a natural number and each line represents an edge of the input graph. The whole file must be read at once and loaded into the RAM memory. Also, to store the graph in memory, the linked list data stucture is used. 
The following algorithms are implemented for sorting:
. Insertion sort
. Bubble sort
. Merge Sort
. Quick Sort

At the time of execution of the program, the desired file containing graph information and the name of the selected algorithm for creating a map should be inputed. for example:

1. RUN Bubble test1.csv
2. RUN Quick test2.csv
3. RUN Merge test1.csv
4. RUN Insertion test2.csv

The output of each execution of the program contains the following items:

1. The time spent to read the graph information from the CSV file and store it in the Adjacency list.
2. The time spent for the initial calculation of the weights.
3. The graph of the time spent in the sorting step from the beginning to the end of the algorithm.
4. A CSV file whose lines contain the number of each vertex along with its community (A or B)

two version of the algorithm exist,one parallel,which uses multiprocessing,and one which only works with one core.
the tests and results are in csv format,which are compatible with the gephi software.
keep in mind that the algorithm stops when the graph becomes disconnected,and in order to continue the algorithm,we have to run the algorithm recursivly on the disconnectd parts.

the algorithm uses a sort algorithm(bubble,merge,quick and insertion) and findest the edge with the minumum weight.(we can also use the min function,which improves the complexity).
