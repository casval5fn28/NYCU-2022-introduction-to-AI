from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1) 
        """
            First , define a "minimax" function . In this function , it returns the utility when the game ends 
        or defined depth is reached ,and  does maximization for "Pacman" and minimization for "ghosts" 
        depending on the number of agent . 
            In pacman maximization part , it finds the max value of the results done by minimax() 
        with agent(=1) , current depth , and child game state . Similiar in ghost minimization part , it 
        finds the min value with the same function and parameteres except for a changing "agent" , also
        increase depth when agent+1 = 0 .
            Then , perform maximum action for root(pacman) by traversing through pacman's legal move and using 
        minimax() during the process .
            
        """  
        def minimax(agent, depth, gameState):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            if agent == 0:
                return max(minimax(1, depth, gameState.getNextState(agent, act)) for act in gameState.getLegalActions(agent))
            else:
                next_agent = agent + 1
                if gameState.getNumAgents() == next_agent:
                    next_agent = 0
                if next_agent == 0:
                    depth += 1
                return min(minimax(next_agent, depth, gameState.getNextState(agent, act)) for act in gameState.getLegalActions(agent))

        mx = float("-inf")
        move = Directions.WEST
        for agent_st in gameState.getLegalActions(0):
            utility = minimax(1, 0, gameState.getNextState(0, agent_st))
            if utility > mx or mx == float("-inf"):
                mx = utility
                move = agent_st

        return move
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        """
            Similar to Minimax , but set two values , alpha(a) and beta(b) as the standard to determine 
        if we should do pruning or not .
            First , define a maximize and a minimize function that calculates value with max(min) 's best 
        opertion on path to root (alpha(a) and beta(b) ).
            Then , define a "alphabetaprune()" which returns the utility if the game ends or defined depth 
        is reached , and maximize(minimize) pacman(ghost) just like minimax .
            Finally , perform maximum action for root(pacman) by traversing through pacman's legal move and using 
        alphabetaprune() during the process. 
            
        """
        def maximize(agent, depth, game_state, a, b):
            v = float("-inf")
            for act in game_state.getLegalActions(agent):
                v = max(v, alphabetaprune(1, depth, game_state.getNextState(agent, act), a, b))
                if v > b:
                    return v
                a = max(a, v)
            return v

        def minimize(agent, depth, game_state, a, b):
            v = float("inf")
            next_agent = agent + 1 
            if game_state.getNumAgents() == next_agent:
                next_agent = 0
            if next_agent == 0:
                depth += 1

            for act in game_state.getLegalActions(agent):
                v = min(v, alphabetaprune(next_agent, depth, game_state.getNextState(agent, act), a, b))
                if v < a:
                    return v
                b = min(b, v)
            return v

        def alphabetaprune(agent, depth, game_state, a, b):
            if game_state.isWin() or game_state.isLose() or depth == self.depth:
                return self.evaluationFunction(game_state)

            if agent == 0:
                return maximize(agent, depth, game_state, a, b)
            else:
                return minimize(agent, depth, game_state, a, b)
        
        alpha = float("-inf")
        beta = float("inf")
        utility = float("-inf")
        move = Directions.WEST
        for agent_st in gameState.getLegalActions(0):
            ghost_val = alphabetaprune(1, 0, gameState.getNextState(0, agent_st), alpha, beta)
            if ghost_val > utility:
                utility = ghost_val
                move = agent_st
            if utility > beta:
                return utility
            alpha = max(alpha, utility)

        return move
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        """
            Also similar to Minimax , define a expectimax function that returns the utility if the game ends 
        or defined depth is reached , and does maximization for pacman when "agent" be 0, but chooses the 
        branch by max expected utility for ghosts(chance) when "agent" not be 0 .
            Finally , perform maximum action for root(pacman) by traversing through pacman's legal move and using 
        expectimax() during the process. 
            
        """
        def expectimax(agent, depth, gameState):
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState)
            if agent == 0:
                return max(expectimax(1, depth, gameState.getNextState(agent, act)) for act in gameState.getLegalActions(agent))
            else: 
                next_agent = agent + 1
                if gameState.getNumAgents() == next_agent:
                    next_agent = 0
                if next_agent == 0:
                    depth += 1
                return sum(expectimax(next_agent, depth, gameState.getNextState(agent, act)) for act in gameState.getLegalActions(agent)) / float(len(gameState.getLegalActions(agent)))

        mx = float("-inf")
        move = Directions.WEST
        for agent_st in gameState.getLegalActions(0):
            utility = expectimax(1, 0, gameState.getNextState(0, agent_st))
            if utility > mx or mx == float("-inf"):
                mx = utility
                move = agent_st

        return move
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    """
        First , calcultate the distance between pacman & ghosts  , and 
    get "g_dist" . In addition , check the proximity of ghosts ( within distance = 1) 
    around pacman , and get "g_proximity". 
        Second , calculate the distance to the closest food and get "min_fdst" 
    as the result.
        Finally , get the number of capsules available (cap_num) . The combination of 
    all former calculated results and score we get will be the result .
            
    """    
    pacman_pos = currentGameState.getPacmanPosition()
    g_dist = 1
    g_proximity = 0
    for ghost_state in currentGameState.getGhostPositions():
        dist = util.manhattanDistance(pacman_pos, ghost_state)
        g_dist += dist
        if dist <= 1:
            g_proximity += 1
     
    food = currentGameState.getFood()
    food_List = food.asList()
    #print("food list:" , food_List)
    min_fdist = -1
    for fd in food_List:
        dist = util.manhattanDistance(pacman_pos, fd)
        if min_fdist == -1 or min_fdist >= dist:
            min_fdist = dist

    cap = currentGameState.getCapsules()
    cap_num = len(cap)
    #print("g_dst: ",g_dist)
    #print("g_prox: ",g_proximity)
    #print("min_fdist: ",min_fdist)
    #print("cap_num: ",cap_num)
    #print("res:", currentGameState.getScore() - (1 / float(g_dist)) - g_proximity + (1 / float(min_fdist))  - cap_num)
    return currentGameState.getScore() - (1 / float(g_dist)) - g_proximity + (1 / float(min_fdist))  - cap_num
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
