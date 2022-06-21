import csv
edgeFile = 'edges.csv'

def dfs(start, end):
    # Begin your code (Part 2)
    """
    First , build "graph" with data in the csv file . While stack is not empty ,
    put nodes that are near to vertices and not visited on stack's top , 
    however , stack pops out the last node . Also in the while loop , record 
    parents of vertex for tracing . When the route encounters "end" , return 
    the path , distance and number of visited nodes.
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
    stack = [start]            
    parent = {}
    dist_dict = {}
    num_visited = 0
    
    while stack:
        node = stack.pop()
        visited.append(node)

        if node in graph:
            vertices = graph[node]
            for i in vertices:
                if i[0] not in visited:
                    parent[i[0]] = node
                    dist_dict[i[0]] = i[1] 
                    stack.append(i[0])
                if i[0] == end:
                    dist = 0
                    path = []
                    tgt = end
                    
                    while tgt != start :
                        dist += dist_dict[tgt]
                        path.append(parent[tgt])
                        tgt = parent[tgt]
                    
                    path.append(start)
                    num_visited = len(visited)
                    
                    return path,dist,num_visited
    
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(426882161, 1737223506)
    print(f'The number of path vertices: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited vertices: {num_visited}')
