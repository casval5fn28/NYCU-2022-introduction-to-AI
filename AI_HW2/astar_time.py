import csv
from queue import PriorityQueue
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'

def astar_time(start, end):
    
    # Begin your code (Part 6)
    """
    Basically the same thing like "astar.py" , but I used the biggest 
    speed limit to divide "heuri" . In addition , I divide each distance
    by speed limit to get the time , not distance .
    """
    
    max_lmt = 0
    graph = {}
    heuri = {}
    with open(edgeFile, newline='') as file:
        rows = csv.DictReader(file)
        for line in rows:
            tmp = []
            if int(line['start']) in graph:
                tmp.extend(graph[int(line['start'])])
                tmp.append((int(line['end']),float(line['distance']),float(line['speed limit'])))
                max_lmt = max(max_lmt, float(line['speed limit']))
                graph[int(line['start'])]=tmp
            else:
                tmp.append((int(line['end']),float(line['distance']),float(line['speed limit'])))
                max_lmt = max(max_lmt, float(line['speed limit']))
                graph[int(line['start'])] = tmp
            
    with open(heuristicFile, newline='') as f2:
        rows = csv.DictReader(f2)
        for line in rows:
            heuri[int(line['node'])] = float(line[str(end)])  
            
    visited = [start]         
    sec_dict = {start : 0}
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
                if i[0] not in visited or sec_dict[i[0]] > sec_dict[node[1]] + i[1]/i[2]:
                    if i[0] == end:
                        sec = 0
                        path = []
                        tgt = end
                        parent[tgt] = node[1]
                        
                        while tgt != start :
                            path.append(parent[tgt])
                            tgt = parent[tgt]
                            
                        sec = sec_dict[node[1]] + i[1]/i[2]
                        path.append(start)
                        num_visited = len(visited)
                        
                        return path,sec,num_visited
                    else:
                        visited.append(i[0])
                        sec_dict[i[0]] = sec_dict[node[1]] + i[1]/i[2]
                        parent[i[0]] = node[1]
                        pq.put((heuri[i[0]]/max_lmt + sec_dict[node[1]] + i[1]/i[2] , i[0]))

    # End your code (Part 6)


if __name__ == '__main__':
    path, time, num_visited = astar_time(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
