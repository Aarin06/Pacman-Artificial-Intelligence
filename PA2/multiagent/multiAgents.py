# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        # print("*********************************")
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        "*** YOUR CODE HERE ***"
        
        foodW=10
        ghostW=1/2
        
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        
        # List of new position given that you move in the direction ACTION
        newPos = successorGameState.getPacmanPosition()
        # list of remaining food pellets
        newFood = currentGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        ghostDist = float('inf')
        for ghost in newGhostStates:
            dist = manhattanDistance(ghost.getPosition(), newPos)
            if dist < ghostDist:
                ghostDist = dist
                
        foodDist = float('inf')
        for food in newFood:
          dist = manhattanDistance(food, newPos)
          if dist < foodDist:
              foodDist = dist
      
        if foodDist == 0:
            foodDist = 10
        else:
            foodDist = 1/foodDist
      
        # print ("Food dist",foodDist)
        # print("Ghost dist",ghostDist)
        # print("score",successorGameState.getScore())
        # print(action)
        return foodW*foodDist+ghostW*ghostDist+successorGameState.getScore()
 
def scoreEvaluationFunction(currentGameState: GameState):
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
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        maxDepth = self.depth
        def minimax(evalF, gameState, depth, agentIndex):
      
          if depth == 0 or gameState.isWin() or gameState.isLose():
            return evalF(gameState)
        
          if agentIndex == 0:
            bestValue = float("-inf")
            bestAction = None
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                value = minimax(evalF, successor, depth, 1)
                if value > bestValue:
                    bestValue = value
                    bestAction = action
            if depth == maxDepth:
                return bestAction
            else:
                return bestValue
          else:
            bestValue = float("inf")
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == gameState.getNumAgents() - 1:
                    value = minimax(evalF, successor, depth - 1, 0)
                else:
                    value = minimax(evalF, successor, depth, agentIndex + 1)
                bestValue = min(bestValue, value)
            return bestValue
        
        move = minimax(self.evaluationFunction, gameState, maxDepth, 0)

        return move



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def alphaBeta(evalF, gameState, depth, agentIndex, alpha, beta):
          # print("agent",agentIndex)
          # print("previous",prev)
          if depth == 0 or gameState.isWin() or gameState.isLose():
            # print("terminal", evalF(gameState))
            return evalF(gameState)
          
          if agentIndex == 0:
            bestValue = float("-inf")
            bestAction = None
            value = None
            for action in gameState.getLegalActions(agentIndex):
                # print(beta,">=",alpha)
                if beta >= alpha:  
                  successor = gameState.generateSuccessor(agentIndex, action)
                  value = alphaBeta(evalF, successor, depth, 1, alpha, beta)
                  if value > bestValue:
                    bestValue = value
                    bestAction = action
                  alpha = max(bestValue, alpha)
            if depth == maxDepth:
                return bestAction
            else:
                # print("bestValue",bestValue)
                return bestValue
          else:
            bestValue = float("inf")
            value = None
            for action in gameState.getLegalActions(agentIndex):
                # print(alpha,"<=",beta)
                if alpha <= beta:
                  successor = gameState.generateSuccessor(agentIndex, action)
                  if agentIndex == gameState.getNumAgents() - 1:
                      value = alphaBeta(evalF, successor, depth - 1, 0, alpha, beta)
                  else:
                      value = alphaBeta(evalF, successor, depth, agentIndex + 1, alpha, beta)
                  bestValue = min(bestValue, value)
                  beta = min(beta, bestValue)

            return bestValue

        maxDepth = self.depth
        move = alphaBeta(self.evaluationFunction, gameState, maxDepth, 0, float("-inf"), float("inf"))

        return move

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        maxDepth = self.depth

        def expectimax(evalF, gameState, depth, agentIndex):
          # print("agent",agentIndex)
          # print("previous",prev)
          if depth == 0 or gameState.isWin() or gameState.isLose():
            return evalF(gameState)
        
          if agentIndex == 0:
            bestValue = float("-inf")
            bestAction = None
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                value = expectimax(evalF, successor, depth, 1)
                if value > bestValue:
                    bestValue = value
                    bestAction = action
            if depth == maxDepth:
                return bestAction
            else:
                return bestValue
            9.5 
            9.75
            
          else:
            bestValue = 0
            p = 1/len(gameState.getLegalActions(agentIndex))
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == gameState.getNumAgents() - 1:
                    value = expectimax(evalF, successor, depth - 1, 0)
                else:
                    value = expectimax(evalF, successor, depth, agentIndex + 1)
                bestValue += p*value

            return bestValue

        move = expectimax(self.evaluationFunction, gameState, maxDepth, 0)
        return move

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    foodW = 60
    ghostW = -15
    pelletW = -25
    scaredW = 10
    
    
  
    # List of new position given that you move in the direction ACTION
    pos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood().asList()
    powerPellets = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    ghostDist = [manhattanDistance(pos, ghost.getPosition()) for ghost in ghostStates]
    powerPelletDist = [manhattanDistance(pos, pellet) for pellet in powerPellets]
    foodDist = [manhattanDistance(pos, food) for food in  newFood]
    scaredTimes = [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]

    ghostFinal = 0
    for scared,ghost in zip(scaredTimes, ghostDist):
      if scared > 0:
          ghostFinal += scaredW*(ghost+1)
      else:
          ghostFinal += ghostW*(ghost+1)
    
    foodFinal = foodW/min(foodDist, default=1)
    pelletFinal = foodW/min(powerPelletDist, default=1)
         

    return foodFinal+ghostFinal+pelletFinal+currentGameState.getScore()-len(newFood)*100


# Abbreviation
better = betterEvaluationFunction
