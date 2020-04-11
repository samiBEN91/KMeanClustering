
import math #For pow and sqrt
import sys
from random import shuffle, uniform
from random import choice
from matplotlib import pyplot

def CutToTwoFeatures(items,indexA,indexB):
    n = len(items)
    X = [];
    for i in range(n):
        item = items[i]
        newItem = [item[indexA],item[indexB]]
        X.append(newItem)

    return X

def PlotClusters(clusters):
    n = len(clusters);
    #Cut down the items to two dimension and store to X
    X = [[] for i in range(n)];

    for i in range(n):
        cluster = clusters[i];
        for item in cluster:
            X[i].append(item);

    colors = ['r','b','g','c','m','y'];

    for x in X:
        #Choose color randomly from list, then remove it
        #(to avoid duplicates)
        c = choice(colors);
        colors.remove(c);

        Xa = [];
        Xb = [];

        for item in x:
            Xa.append(item[0]);
            Xb.append(item[1]);

        pyplot.plot(Xa,Xb,'o',color=c);

    pyplot.show();

###_Pre-Processing_###
def ReadData(fileName):
    #Read the file, splitting by lines
    f = open(fileName,'r')
    lines = f.read().splitlines();
    print("LineNumber=",len(lines))
    f.close()

    items = []

    for i in range(1,len(lines)):
        line = lines[i].split(',')
        itemFeatures = []

        for j in range(len(line)-1):
            v = float(line[j]) #Convert feature value to float
            itemFeatures.append(v) #Add feature value to dict
    
        items.append(itemFeatures)

    shuffle(items)
    #print (items)
    return items
   
###_Auxiliary Function_###
def FindColMinMax(items):
    n = len(items[0])
    minima = [sys.maxsize for i in range(n)]#liste comprehension
    maxima = [-sys.maxsize -1 for i in range(n)]
    
    for item in items:
        for f in range(len(item)):
            if(item[f] < minima[f]):
                minima[f] = item[f]
            
            if(item[f] > maxima[f]):
                maxima[f] = item[f]
    print("nombre de colonnes dans chaque item =",n)
    return minima,maxima

def EuclideanDistance(x,y):
    S = 0; #The sum of the squared differences of the elements
    for i in range(len(x)):
        S += math.pow(x[i]-y[i],2);

    return math.sqrt(S); #The square root of the sum


def InitializeMeans(items,k,cMin,cMax):
    #Initialize means to random numbers between
    #the min and max of each column/feature
    
    f = len(items[0]); #number of features
    means = [[0 for i in range(f)] for j in range(k)]
    
    for mean in means:
        for i in range(len(mean)):
            #Set value to a random float
            #(adding +-1 to avoid a wide placement of a mean)
            mean[i] = uniform(cMin[i]+1,cMax[i]-1)

    return means

def UpdateMean(n,mean,item):
    for i in range(len(mean)):
        m = mean[i]
        m = (m*(n-1)+item[i])/float(n)
        mean[i] = round(m,3)
    
    return mean

def FindClusters(means,items):
    clusters = [[] for i in range(len(means))]; #Init clusters
    
    for item in items:
        #Classify item into a cluster
        index = Classify(means,item);

        #Add item to cluster
        clusters[index].append(item);

    return clusters;


###_Core Functions_###
def Classify(means,item):
    #Classify item to the mean with minimum distance
    
    minimum = sys.maxsize;
    index = -1;

    for i in range(len(means)):
        #Find distance from item to mean
        dis = EuclideanDistance(item,means[i]);

        if(dis < minimum):
            minimum = dis;
            index = i;
    
    return index;


def CalculateMeans(k,items,maxIterations=100000):
    #Find the minima and maxima for columns
    cMin, cMax = FindColMinMax(items);
    
    #Initialize means at random points
    means = InitializeMeans(items,k,cMin,cMax);
    
    #Initialize clusters, the array to hold
    #the number of items in a class
    clusterSizes = [0 for i in range(len(means))];

    #An array to hold the cluster an item is in
    belongsTo = [0 for i in range(len(items))];

    #Calculate means
    for e in range(maxIterations):
        #If no change of cluster occurs, halt
        noChange = True;
        for i in range(len(items)):
            item = items[i];
            #Classify item into a cluster and update the
            #corresponding means.
        
            index = Classify(means,item);

            clusterSizes[index] += 1;
            means[index] = UpdateMean(clusterSizes[index],means[index],item);

            #Item changed cluster
            if(index != belongsTo[i]):
                noChange = False;

            belongsTo[i] = index;

        #Nothing changed, return
        if(noChange):
            break;

    return means;


def main():
	items = ReadData("data.txt")
	items = CutToTwoFeatures(items,2,3);
	mintmp, maxtmp=FindColMinMax(items)
	print ("mintmp =",mintmp)
	print ("maxtmp =",maxtmp)
	k = 3
	means = InitializeMeans(items,k,mintmp, maxtmp)
	#print ("means Initialized =",means)
	means1=CalculateMeans(k,items)
	print ("means Calculated =",means)
	clusters = FindClusters(means,items);
	print (clusters)

	PlotClusters(clusters);

if __name__ == "__main__":
    main()