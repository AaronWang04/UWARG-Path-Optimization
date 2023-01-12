'''
TODO:
    Test
    Figure out input and output with data telemetry
    Make program work with n-point polygon, if needed, conops confusing aff :(
'''

# Libs
import utm # pip install utm
import shapely.geometry # pip install shapely
import matplotlib.pyplot as plt #pip install matplotlib

from math import sqrt, pow

# random nodes from test data
ALPHA = utm.from_latlon(48.5166707,-71.6375025) 
VICTOR = utm.from_latlon(48.510353,-71.6228085)
NOVEMBER = utm.from_latlon(48.5090567,-71.6461702)
OSCAR = utm.from_latlon(48.5107057,-71.6516848)
BRAVO = utm.from_latlon(48.5060947,-71.6317518)
QUEBEC =  utm.from_latlon(48.5262308,-71.6345802)
ZULU = utm.from_latlon(48.4932846,-71.6664874)

# A sample bounded area
bound = [ALPHA,VICTOR,NOVEMBER,OSCAR]

def restriction(start, end, bound):
    '''
    :type start, end: tuples(x,y) coordintes in UTM
    '''

    # Represents the bounded area
    bounded = polygon(bound)

    boundedScaled = bounded.buffer(15,join_style=2)

    scaledPoints = list(boundedScaled.exterior.coords)

    graph = [start,end]

    for x in scaledPoints:
        graph.append(x)

    dist = {}
    prev = {}
    queue = []

    for x in graph:
        dist[x] = float('inf')
        prev[x] = 0
        queue.append(x)

    dist[start] = 0

    while queue:
        unvisited = []
        tempNode = min(queue)
        
        for node in graph:
            if (node == tempNode): continue
            if (intersect(tempNode, node, bounded) == False):
                unvisited.append(node)

        queue.remove(tempNode)
        for node in unvisited:
            tempDist = dist[tempNode] + distance(tempNode,node)
            if(tempDist < dist[node]):
                dist[node] = tempDist
                prev[node] = tempNode
    
    finalList = [end]
    tempCurrent = end

    while (tempCurrent != start):
        finalList.insert(0,prev[tempCurrent])
        tempCurrent = prev[tempCurrent]
    return finalList


def intersect(start, end, boundedArea):
    ''' 
    Returns true if a line segment with endpoint start,end intersects a bounded region
    
    Parameters:
    start,end : tuple of (x,y) values
    boundedArea
    '''
    
    line = shapely.geometry.LineString([ (start[0],start[1]),(end[0],end[1]) ])

    return line.intersects(boundedArea)

def distance(Point1,Point2):
    '''
    returns a float of distance between two points
    Point1, Point2 : tuples with (x,y) values
    '''
    return sqrt( pow(Point1[0]-Point2[0],2) + pow(Point1[1]-Point2[1],2) )

def polygon(lst):
    '''
    returns a shapely polygon given a list of coordinates
    
    Current assumptions:
    list of points must be ordered to generate convex shape
    the polygon is composed of 4 points

    '''
    return shapely.geometry.Polygon([
        [lst[0][0],lst[0][1]],
        [lst[1][0],lst[1][1]],
        [lst[2][0],lst[2][1]],
        [lst[3][0],lst[3][1]]
    ])

# Random code for testing
lst = restriction(BRAVO,QUEBEC,bound)

x,y = polygon(bound).exterior.xy
plt.plot(x,y)
for i in lst:
    plt.plot(i[0],i[1],'bo',linestyle="--")

plt.show()