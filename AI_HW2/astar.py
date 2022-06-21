import csv
from queue import PriorityQueue
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'

def astar(start, end):
    # Begin your code (Part 4)
    """
    First , build "graph" and "heuri " with data in 2 csv files ,then put 
    "start " into priority queue "pq" . While "pq" is not empty , put
    the node near the vertex into "pq" and record the distance between the 
    node mentioned before and "start" into "dist_dict" and replace the 
    value if receiving  smaller one . In addition , sum the distance and 
    the "heuri" to compare . When the route encounters "end" , return the 
    path , distance and number of visited nodes.

    """
    graph = {}
    heuri = {}
    
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
            
    with open(heuristicFile, newline='') as f2:
        rows = csv.DictReader(f2)
        for line in rows:
            heuri[int(line['node'])] = float(line[str(end)])
            
    visited = [start] 
    dist_dict = {start : 0}
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
                if i[0] not in visited or dist_dict[i[0]] > dist_dict[node[1]] + i[1]:
                    if i[0] == end:
                        dist = 0
                        path = []
                        tgt = end
                        parent[tgt] = node[1]

                        while tgt != start :
                            path.append(parent[tgt])
                            tgt = parent[tgt]
                        
                        dist = dist_dict[node[1]] + i[1]
                        path.append(start)
                        num_visited = len(visited)
                        
                        return path,dist,num_visited
                    
                    else:
                        visited.append(i[0])
                        dist_dict[i[0]] = dist_dict[node[1]] + i[1]
                        parent[i[0]] = node[1]
                        pq.put((heuri[i[0]] + dist_dict[node[1]]+i[1],i[0]))
                        
    # End your code (Part 4)

if __name__ == '__main__':
    path, dist, num_visited = astar(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
