# CommunityDetector
this is an algorithm for finding communities within a undirected graph,especially usefull for networking.
the algorithm works by deleting one edge at a time,based on the weight calculated(which if we consider the Cij the weight of the edge connecting the nodes i and j,
and Zi the degree of the node i) with the formula of :Cij=(number of 3 node cycles which Eij has participated in +1 )/min[Zi-1,Zj-1]
two version of the algorithm exist,one parallel,which uses multiprocessing,and one which only works with one core
the tests and results are in csv format,which are compatible with the gephi software
