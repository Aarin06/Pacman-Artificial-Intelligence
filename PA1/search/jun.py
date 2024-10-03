# NOTE: Uses the Union Find Algorithm (ie. Kruskal's) to find MST
    
    # Gets the starting (root) food for path to f2 [find]
    def getRoot(paths, f2):
        if (paths[f2] == f2):
            return f2
        return getRoot(paths, paths[f2])
    
    # Combines the root paths into a single path [union]
    def unionPath(paths, ranks, f1, f2):
        root1 = getRoot(paths, f1)
        root2 = getRoot(paths, f2)
        
        # Update the paths and ranks
        if (ranks[root1] < ranks[root2]):
            paths[root1] = root2
        elif (ranks[root1] > ranks[root2]):
            paths[root2] = root1
        else:
            paths[root2] = root1
            ranks[root1] += 1
    
    # Get list of food and walls
    unvisited = foodGrid.asList()
    
    # If all food is found
    if (not unvisited):
        return 0

    # Costruct a graph for MST search
    graph = []
    for pos1 in range(len(unvisited)):
        for pos2 in range(1, len(unvisited)):
            food1 = unvisited[pos1]
            food2 = unvisited[pos2]
            graph.append([food1, food2, util.manhattanDistance(food1, food2)])
    graph = sorted(graph, key=lambda x: x[2])
    
    # Initate MST variables
    mst = 0 # the resulting MST distance
    cur = 0 # current unvisited food
    rem = 0 # remaining food
    paths = {}
    ranks = {}
    for food in unvisited:
        paths[food] = food
        ranks[food] = 0
    
    # Begin MST search
    while rem < len(unvisited) - 1:
        food1, food2, dist = graph[cur]
        cur += 1
        
        # Get the parent of two foods
        root1 = getRoot(paths, food1)
        root2 = getRoot(paths, food2)
        
        # If the foods do not originate from the same food path
        if (root1 != root2):
            rem += 1
            mst += dist
            unionPath(paths, ranks, root1, root2)
    
    # Get the closest food to current position
    res = min([util.manhattanDistance(position, food) for food in unvisited])
    
    # Return heuristic based on closest food and MST unvisited foods
    return res + mst 