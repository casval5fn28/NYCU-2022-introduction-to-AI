import csv
edgeFile = 'edges.csv'

def bfs(start, end):
    # Begin your code (Part 1)
    
    """
    First , build "graph" with data in the csv file . While queue is not empty ,
    put nodes that are linked to vertices and not visited on queue's top . Also
    in the while loop , record parents of vertex for tracing . When the route 
    encounters "end" , return the path , distance and number of visited nodes.
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
    queue = [start]
    parent = {}
    dist_dict = {}
    num_visited = 0

    while queue :
        node = queue[0]
        queue.pop(0)
        
        if node in graph:
            vertice = graph[node]
            for i in vertice:
                if i[0] not in visited:
                    queue.append(i[0])
                    visited.append(i[0])
                    parent[i[0]] = node
                    dist_dict[i[0]] = i[1]
                    
                    if i[0] == end:
                        
                        dist = 0
                        path = []
                        tgt = end
                        
                        while tgt != start :
                            dist += dist_dict[tgt]
                            path.append(tgt)
                            tgt = parent[tgt]
                        
                        path.append(start)
                        num_visited = len(visited)
                        return path,dist,num_visited
    # End your code (Part 1)


if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
