import csv
from queue import PriorityQueue
edgeFile = 'edges.csv'

def ucs(start, end):
    # Begin your code (Part 3)
    """
    First , build "graph" with data in the csv file ,then put "start " into 
    priority queue "pq". While "pq" is not empty , put the node near the 
    vertex into "pq" and record distance between the node mentioned before 
    and "start" into "dist_dict" and replace the value if receiving  smaller one.
    When the route encounters "end" , return the path , distance and number 
    of visited nodes.
    """
    graph = {}
    with open(edgeFile, newline='') as f:
        rows = csv.DictReader(f)
        for line in rows:
            tmp = []
            if int(line['start']) in graph:
                tmp.extend(graph[int(line['start'])])
                tmp.append((int(line['end']),float(line['distance'])))
                graph[int(line['start'])] = tmp
            else:
                tmp.append((int(line['end']),float(line['distance'])))
                graph[int(line['start'])] = tmp
                
    
    visited = [start]
    dis_dict = {start : 0}
    parent = {}
    pq = PriorityQueue()
    pq.put((0,start))
    num_visited = 0
    
    while not pq.empty():
        tmp = []
        node = pq.get()

        if node[1] in graph:
            tmp.extend(graph[node[1]])
            for i in tmp:
                if i[0] not in visited or dis_dict[i[0]] > node[0] + i[1]:
                    if i[0] == end:
                        dist = 0
                        path = []
                        tgt = end
                        parent[tgt] = node[1]

                        while tgt != start :
                            path.append(parent[tgt])
                            tgt = parent[tgt]
                        
                        dist = node[0] + i[1]
                        path.append(start)
                        num_visited = len(visited)
                        
                        return path,dist,num_visited
                    
                    else:
                        visited.append(i[0])
                        dis_dict[i[0]] = node[0] + i[1]
                        parent[i[0]] = node[1]
                        pq.put((node[0]+i[1],i[0]))
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(426882161, 1737223506)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
