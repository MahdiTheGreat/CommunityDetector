import csv
import numpy as np
import math
import copy
import time
from multiprocessing import Process
import multiprocessing
from matplotlib import pyplot as plt


class node:

    def __init__(self, value):
        self.value = value
        self.seen=0

    def __eq__(self, obj):
        return isinstance(obj, node) and obj.value == self.value
            # and  obj.seen == self.seen

    def __ne__(self, obj):
        return not self == obj

    def getValue(self):
        return self.value

    def getSeen(self):
        return self.seen

    def incrementSeen(self):
        self.seen+=1


class edge:

    def __init__(self, i, j, w):

        if (i > j):
            self.j = i
            self.i = j
        else:
            self.i = i
            self.j = j
        self.weight = w
        self.cycleCount=-1

    def __eq__(self, obj):
        return isinstance(obj, edge) and obj.weight == self.weight and obj.i == self.i and obj.j == self.j

    def __ne__(self, obj):
        return not self == obj

    def getI(self):
        return self.i

    def getJ(self):
        return self.j

    def getWeight(self):
        return self.weight

    def setWeight(self,weight):
        self.weight=weight

    def setCycleCount(self,cycleCount):
        self.cycleCount=cycleCount

    def getCycleCount(self):
        return self.cycleCount



def hasher(row, col):

    if row>col :return 12*(col+row)*(col+row+1)+row
    else:return 12*(col+row)*(col+row+1)+col


def insertionSort(arg):
    tempSort = arg[1]
    arr=arg[0]


    for i in range(1, len(arr)):

        key = arr[i]
        j = i - 1
        while j >= 0 and key.getWeight() < arr[j].getWeight():
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1]=key

    tempSort.put(arr)


def bubbleSort(arg):
    tempSort = arg[1]
    arr=arg[0]

    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j].getWeight() >= arr[j + 1].getWeight():
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    tempSort.put(arr)

def partition(arg, l, h):
    i = (l - 1)
    x = arg[h]

    for j in range(l, h):
        if arg[j].getWeight() <= x.getWeight():

            i = i + 1
            arg[i], arg[j] = arg[j], arg[i]

    arg[i + 1], arg[h] = arg[h], arg[i + 1]
    return (i + 1)


def quickSort(arg):

    tempSort=arg[1]
    arr=arg[0]

    l=0
    h=len(arr)-1
    size = h - l + 1
    stack = [0] * (size)


    top = -1


    top = top + 1
    stack[top] = l
    top = top + 1
    stack[top] = h



    while top >= 0:


        h = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1


        p = partition(arr, l, h)
        if p - 1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1


        if p + 1 < h:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top]=h

    tempSort.put(arr)



def mergeSort(arg):
    tempSort = arg[1]
    arr = arg[0]



    current_size = 1


    while current_size < len(arr) - 1:

        left = 0

        while left < len(arr) - 1:

            mid = min((left + current_size - 1), (len(arr) - 1))


            right = ((2 * current_size + left - 1,len(arr) - 1)[2 * current_size+ left - 1 > len(arr) - 1])


            merge(arr, left, mid, right)
            left = left + current_size * 2


        current_size = 2 * current_size
    tempSort.put(arr)





def merge(arg, l, m, r):
    n1 = m - l + 1
    n2 = r - m
    right = [0] * n2
    left = [0] * n1

    for i in range(0, n2):
        right[i] = arg[m + i + 1]

    for i in range(0, n1):
        left[i] = arg[l + i]


    i=0
    j=0
    k=l
    while i < n1 and j < n2:
        if left[i].getWeight() > right[j].getWeight():
            arg[k] = right[j]
            j += 1
        else:
            arg[k] = left[i]
            i += 1
        k += 1

    while i < n1:
        arg[k] = left[i]
        i += 1
        k += 1

    while j < n2:
        arg[k] = right[j]
        j += 1
        k += 1




def cycleCounter(i, j):
    cycle = 0
    temp = valueMaker(graph[i])
    for k in range(0, len(temp)):
        if j in graph[temp[k].getValue()]: cycle += 1

    return cycle


def calEdges():
    edges=valueMaker(edgesMap)
    for i in range(0, len(edges)):
        index = [edges[i].getI(),edges[i].getJ()]
        cycleCount=cycleCounter(index[0], index[1])
        edges[i].setCycleCount(cycleCount)
        if not min(len(graph[index[0]]) - 1, len(graph[index[1]]) - 1)<=0 and not edges[i].getWeight()==math.inf:
         edges[i].setWeight( (edges[i].getCycleCount() + 1) / min(len(graph[index[0]]) - 1, len(graph[index[1]]) - 1))
        else:
            edges[i].setWeight(math.inf)
            #print("[" + str(edges[i].getI()) + " " + str([edges[i].getJ()]) + "]")


def recalEdge(Edge):

    global disjointed
    tempGraphArray = valueMaker(graph[Edge.getI()])
    for i in range(0, len(tempGraphArray)):
        k = tempGraphArray[i].getValue()
        tempEdge = edgesMap[hasher(Edge.getI(), k)]
        if not min(len(graph[Edge.getI()]) - 1, len(graph[k]) - 1) <=0 and not tempEdge.getWeight()==math.inf:
         if Edge.getJ() in graph[k]:
             tempEdge.setWeight( (tempEdge.getCycleCount() - 1) / min(len(graph[Edge.getI()]) - 1, len(graph[k]) - 1))
             tempEdge.setCycleCount(tempEdge.getCycleCount()-1)
         else:
             tempEdge.setWeight( tempEdge.getCycleCount() / min(len(graph[Edge.getI()]) - 1, len(graph[k]) - 1))
        else:
            tempEdge.setWeight(math.inf)
            #print("[" + str(tempEdge.getI()) + " " + str(tempEdge.getJ()) + "]")

    tempGraphArray = valueMaker(graph[Edge.getJ()])
    for i in range(0, len(tempGraphArray)):
        k = tempGraphArray[i].getValue()
        tempEdge = edgesMap[hasher(Edge.getJ(), k)]
        if not min(len(graph[Edge.getJ()]) - 1, len(graph[k]) - 1)<=0 and not tempEdge.getWeight()==math.inf:
         if Edge.getI() in graph[k]:
             tempEdge.setWeight( (tempEdge.getCycleCount() - 1) / min(len(graph[Edge.getJ()]) - 1, len(graph[k]) - 1))
             tempEdge.setCycleCount(tempEdge.getCycleCount()-1)
         else:
             tempEdge.setWeight( tempEdge.getCycleCount() / min(len(graph[Edge.getJ()]) - 1, len(graph[k]) - 1))
        else:
            tempEdge.setWeight(math.inf)
            #print("[" + str(tempEdge.getI()) + " " + str(tempEdge.getJ()) + "]")




def bfs(index):
    global a
    Node=nodesMap[index]
    passed = [False] * len(nodesMap)
    stack = []
    stack.append(Node)
    passed[Node.getValue()] = True
    Node.incrementSeen()
    #print("node is")
    #print(Node.getValue())
    while stack:

        tempNode = stack.pop(0)
        tempGraph = valueMaker(graph[tempNode.getValue()])
        for i in range(0, len(tempGraph)):
            if passed[tempGraph[i].getValue()] == False:
                stack.append(tempGraph[i])
                passed[tempGraph[i].getValue()] = True
                tempGraph[i].incrementSeen()
                #print("node is")
                #print(tempGraph[i].getValue())

    check = 0
    for i in range(0, len(passed)):
        if passed[i]:
            check += 1
        else:
            #print("index is"+str(i))
            a.append(nodesMap[i])


    return check



def deleteEdge(i,j):
    tempEdge=copy.deepcopy(edgesMap[hasher(i,j)])
    edgesMap.pop(hasher(tempEdge.getI(), tempEdge.getJ()))
    tempGraph = graph[tempEdge.getI()]
    tempGraph.pop(tempEdge.getJ())
    tempGraph = graph[tempEdge.getJ()]
    tempGraph.pop(tempEdge.getI())
    recalEdge(tempEdge)

def valueMaker(arr):
    arr=list(dict.items(arr))
    temp = []
    for i in range(0, len(arr)):
        temp.append(arr[i][1])
    return temp


def sortMerge(arg):

    left = arg[0]
    right=arg[1]
    tempMerge = arg[2]



    if not len(left) or not len(right):
        return left or right

    result = []
    i, j = 0, 0
    while (len(result) < len(left) + len(right)):
        if left[i].getWeight() < right[j].getWeight():
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
        if i == len(left) or j == len(right):
            result.extend(left[i:] or right[j:])
            break

    tempMerge.put(result)



def workers(target, args, step, length, mode):
    begining = 0
    processes = []
    arr = args[0]
    tempArg=[]


    for i in range(0, length):
        if mode=="sort":
            tempArg=(arr[begining: ((begining + step) if i < (length-1) else len(arr))], args[1])
        elif mode=="merge":
            tempArg=(arr[begining], arr[begining + step] , args[1])
            begining+=step
        elif mode=="cal":tempArg=""
        tempProcess = Process(target=target, args=(tempArg,))
        processes.append(tempProcess)
        tempProcess.start()
        begining += step

    for i in range(0, length):
        processes[i].join()


def queueTolist(queue):
    temp=[]
    while not queue.empty():
        temp.append(queue.get())

    return temp

if __name__ == '__main__':



 disjointed = False
 graph = []
 edgesMap = dict()
 nodesMap = dict()
 fileName="RUN Bubble communityTest.tsv"
 mode=fileName.split(" ")
 mode=mode[1]
 csvAndCallTime = []
 a=[]
 sortMode={"Insertion":insertionSort,"Quick":quickSort,
           "Merge":mergeSort,"Bubble":bubbleSort}
 cores=multiprocessing.cpu_count()
 #cores = 4


 start_time = time.time()

 tsv_file = open(fileName)
 read_tsv = csv.reader(tsv_file, delimiter="\t")
 x = list(read_tsv)
 result = np.array(x).astype("int")
 offSet = copy.deepcopy(result[0][0])
 max=-1
 for i in range(0, len(result)):
     for j in range(0, len(result[0])):
         result[i][j] -= offSet
         if result[i][j]>max:
             max=copy.deepcopy( result[i][j])



 for i in range(0, len(result)):
     tempNode = node(result[i][0])
     if not (tempNode.getValue() in nodesMap):
         nodesMap[tempNode.getValue()] = tempNode


     tempNode = node(result[i][1])
     if not (tempNode.getValue() in nodesMap):
         nodesMap[tempNode.getValue()] = tempNode



 for i in range(0, len(nodesMap)):
     graph.append(dict())

 for i in range(0, len(result)):

     tempNode = nodesMap[result[i][1]]
     if not (tempNode.getValue() in graph[result[i][0]]):
         graph[result[i][0]][tempNode.getValue()] = tempNode

     tempNode = nodesMap[result[i][0]]
     if not (tempNode.getValue() in graph[result[i][1]]):
         graph[result[i][1]][tempNode.getValue()] = tempNode

     hash=hasher(result[i][1], result[i][0])

     if not (hash in edgesMap):
         tempEdge = edge(result[i][1], result[i][0], -1)
         edgesMap[hash] = tempEdge

 csvAndCallTime.append(time.time() - start_time)

 start_time = time.time()

 calEdges()

 csvAndCallTime.append(time.time() - start_time)

 print("the nodes number before")
 print(len(nodesMap))
 print("the graph number before")
 print(len(graph))
 print("the edges number before")
 print(len(edgesMap))



 loop = 0
 passed=-1
 minEdge=edge(-1,-1,-1)
 WhileTimey = np.array([])
 sortFunc = sortMode[mode]


 while not disjointed:

     start_time = time.time()
     edges=copy.deepcopy(valueMaker(edgesMap))
     step = math.floor(len(edgesMap) / cores)


     if step > 1:
        tempMerge = multiprocessing.Manager().Queue(-1)
        tempSort = multiprocessing.Manager().Queue(-1)
        oddTempEdge=[]

        workers(sortFunc,(edges,tempSort), step, cores,"sort")
        tempSortList = queueTolist(tempSort)

        if len(tempSortList)%2==1:
            oddTempEdge.append(tempSortList[len(tempSortList)-1])
            tempMergeList=tempSortList[0:len(tempSortList)-1]


        workers(sortMerge,(tempSortList,tempMerge),1,math.floor(cores / 2),"merge")
        tempMergeList = queueTolist(tempMerge)


        while len(tempMergeList)>1:

            tempMerge=multiprocessing.Manager().Queue(-1)
            workers(sortMerge, (tempMergeList, tempMerge), 1,math.floor(len(tempMergeList)/2), "merge")
            tempMergeList = queueTolist(tempMerge)

        edges = copy.deepcopy(tempMergeList)

        tempSort=multiprocessing.Manager().Queue(-1)

        if  len(oddTempEdge)==1:

            sortMerge((edges[0],oddTempEdge[0],tempSort))
            edges=queueTolist(tempSort)

     else:
         tempSort=multiprocessing.Manager().Queue(-1)
         sortFunc((edges,tempSort))
         edges=queueTolist(tempSort)


     WhileTimey=np.append(WhileTimey,[time.time() - start_time])

     minEdge=edges[0][0]
     i=minEdge.getI()

     print("min is")
     print(str(minEdge.getI())+" "+str(minEdge.getJ()))
     print(minEdge.getWeight())
     deleteEdge(minEdge.getI(),minEdge.getJ())
     passed=bfs(i)
     disjointed = not (passed==len(nodesMap))
     loop+=1
     print(loop)


 print(passed)
 graphCsv = []
 WhileTimex = x = np.arange(0, loop)
 print("the nodes number")
 print(len(nodesMap))
 print("the graph number")
 print(len(graph))
 print("the edges number")
 print(len(edgesMap))
 print("the a number")
 print(len(a))
 print("passed is")
 print(passed)
 print("csv time:"+str(csvAndCallTime[0]))
 print("cal time:" + str(csvAndCallTime[1]))
 plt.plot(WhileTimex, WhileTimey)

 for i in range(0, len(a)):
     value=a[i].getValue()
     tempArr = valueMaker(graph[value])
     tempArr2=[value+offSet]

     if not len(tempArr)==0:
      for j in range(0, len(tempArr)):
          tempArr2.append(tempArr[j].getValue()+offSet)
     graphCsv.append(tempArr2)




 with open("new_file.csv", "w+", newline='') as my_csv:
     csvWriter = csv.writer(my_csv, delimiter=',')
     csvWriter.writerows(graphCsv)

 plt.show()
 print("done")





