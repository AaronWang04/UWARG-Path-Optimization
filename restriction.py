# Libs
import utm  # pip install utm
import shapely.geometry  # pip install shapely
import matplotlib.pyplot as plt  # pip install matplotlib
from math import sqrt, pow

# A sample bounded area
def restriction(start, end, bound):
    '''
    :type start, end: tuples(x,y) coordintes in UTM
    '''
    # Represents the bounded area
    bounded = polygon(bound)

    boundedScaled = bounded.buffer(15, join_style=2)

    scaledPoints = list(boundedScaled.exterior.coords)

    graph = [start, end]

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
            tempDist = dist[tempNode] + distance(tempNode, node)
            if (tempDist < dist[node]):
                dist[node] = tempDist
                prev[node] = tempNode

    finalList = [end]
    tempCurrent = end

    while (tempCurrent != start):
        finalList.insert(0, prev[tempCurrent])
        tempCurrent = prev[tempCurrent]

    return finalList


def intersect(start, end, boundedArea):
    '''
    Returns true if a line segment with endpoint start,end intersects a bounded region

    Parameters:
    start,end : tuple of (x,y) values
    boundedArea
    '''

    line = shapely.geometry.LineString([(start[0], start[1]), (end[0], end[1])])

    return line.intersects(boundedArea)


def distance(Point1, Point2):
    '''
    returns a float of distance between two points
    Point1, Point2 : tuples with (x,y) values
    '''
    return sqrt(pow(Point1[0] - Point2[0], 2) + pow(Point1[1] - Point2[1], 2))


def polygon(lst):
    '''
    returns a shapely polygon given a list of coordinates

    Current assumptions:
    list of points must be ordered to generate convex shape
    the polygon is composed of 4 points
    '''

    polyReturned = [[lst[coord][0], lst[coord][1]] for coord in range(len(lst))]

    return shapely.geometry.Polygon(polyReturned)

# Random code for testing
# lst = restriction(BRAVO, QUEBEC, bound)

# x, y = polygon(bound).exterior.xy
# plt.plot(x, y)
# for i in lst:
#     plt.plot(i[0], i[1], 'bo', linestyle="--")

# for i in range(len(names)):
#     plt.annotate(names[i], (bound[i][0], bound[i][1]))

# plt.annotate("START", (BRAVO[0], BRAVO[1]))
# plt.annotate("END", (QUEBEC[0], QUEBEC[1]))

# plt.show()
# print (lst)