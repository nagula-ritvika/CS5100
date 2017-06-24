# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        # print "Score chosen =",bestScore,"action =",legalMoves[chosenIndex]
        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
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

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # print [g[i] for i in newGhostStates]

        # if successorGameState.isWin() or currentGameState.isWin():
        #     return float('inf')
        # if successorGameState.isLose() or currentGameState.isLose():
        #     return float('-inf')


        # if the current position is same as the position we get on taking this action then this is the worst action.
        if newPos == currentGameState.getPacmanPosition():
            return float('-inf')

        foodDist = [manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()]

        ghostDist = []
        for ghost in newGhostStates:
            ghostDist.append(util.manhattanDistance(newPos,ghost.getPosition()))

        for dist in ghostDist:
            # if the ghost is too close then this is worst action to take
            if dist <= 3:
                return float('-inf')

        # if there is no food left --> this is the best action to take.
        if len(foodDist) == 0:
            return float('inf')

        # more food is left, then the score will be less
        # more the sum of distances to each food dot, lesser the score
        # the number of food left is more important than the distances to the food.
        score = scoreEvaluationFunction(successorGameState)
        return score + (10000/sum(foodDist)) + (20000/len(foodDist))


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
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
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
        """
        "*** YOUR CODE HERE ***"
        def min_minimax(state,cur_depth,total_ghosts,cur_ghost):
            # print "depth=", cur_depth, "min called"
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            moves = state.getLegalActions(cur_ghost)
            score = float('inf')
            if cur_ghost == total_ghosts:

                for m in moves:
                    next_state = state.generateSuccessor(cur_ghost,m)
                    score = min(score,max_minimax(next_state,cur_depth,total_ghosts))
            else:
                for m in moves:
                    next_state = state.generateSuccessor(cur_ghost,m)
                    score = min(score, min_minimax(next_state, cur_depth, total_ghosts, cur_ghost+1))

            # print "Score from min = ",score
            return score

        def max_minimax(state,cur_depth,total_ghosts):
            new_depth = cur_depth + 1
            # print "depth=",new_depth,"max called"

            if state.isWin() or state.isLose() or new_depth == self.depth:
                return self.evaluationFunction(state)
            moves = state.getLegalActions(0)
            score = float('-inf')
            for m in moves:
                next_state = state.generateSuccessor(0,m)
                score = max(score,min_minimax(next_state,new_depth,total_ghosts,1))
            # print "Score from max = ", score
            return score

        total_ghosts = gameState.getNumAgents() - 1
        moves = gameState.getLegalActions(0)
        best_move = None
        score = float('-inf')

        for m in moves:
            cur_depth = 0
            next_state = gameState.generateSuccessor(0,m)
            old_score = score
            score = max(score,min_minimax(next_state,cur_depth,total_ghosts,1))
            if score > old_score:
                best_move = m

        return best_move
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def min_alphabeta(state,cur_depth, total_ghosts, cur_ghost, alpha, beta):

            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            # print "depth = ", cur_depth,"min called"
            moves = state.getLegalActions(cur_ghost)
            score = float('inf')
            if cur_ghost == total_ghosts:

                for m in moves:
                    # print "     ", m
                    if alpha > beta:
                        # print "score from min", score
                        return score

                    next_state = state.generateSuccessor(cur_ghost,m)
                    # print "     old score",p_score
                    score = min(score, max_alphabeta(next_state,cur_depth,total_ghosts, alpha, beta))
                    # print "     new_score",score
                    # print "explored ", str(next_state)
                    # if score <= alpha:
                    #     # print "score from min", score
                    #     print "got score less than alpha"
                    #
                    #     return score
                    beta = min(beta,score)
            else:
                for m in moves:
                    # print "     ",m
                    if alpha > beta:
                        # print "score from min", score

                        return score
                    next_state = state.generateSuccessor(cur_ghost,m)
                    score = min(score,min_alphabeta(next_state,cur_depth,total_ghosts,cur_ghost+1,alpha,beta))
                    # print "explored ", str(next_state)
                    # if score <= alpha:
                    #     # print "score from min", score
                    #     print "got score less than alpha"
                    #     return score
                    beta = min(beta, score)
            # print "score from min", score
            return score

        def max_alphabeta(state, cur_depth, total_ghosts, alpha, beta):
            new_depth = cur_depth + 1
            # print "depth=",new_depth,"max called"

            if  state.isWin() or state.isLose() or new_depth == self.depth:
                # print "     win=",state.isWin()
                return self.evaluationFunction(state)
            moves = state.getLegalActions(0)
            score = float('-inf')
            for m in moves:
                if alpha > beta:
                    # print "score from max", score

                    return score
                next_state = state.generateSuccessor(0, m)
                score = max(score, min_alphabeta(next_state, new_depth, total_ghosts, 1, alpha, beta))
                # print "explored ", str(next_state)
                # if score >= beta:
                #     # print "Score from max = ", score
                #     return score
                alpha = max(alpha,score)
            # print "Score from max = ", score

            return score
        total_ghosts = gameState.getNumAgents() - 1
        moves = gameState.getLegalActions(0)
        best_move = None
        score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for m in moves:
            cur_depth = 0
            next_state = gameState.generateSuccessor(0, m)
            old_score = score
            score = max(score, min_alphabeta(next_state, cur_depth, total_ghosts, 1,alpha,beta))
            # print "explored ",str(next_state)
            if score > old_score:
                best_move = m
            # if score >= beta:
            #     return best_move
            alpha = max(alpha,score)

        return best_move
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        def min_expectimax(state, cur_depth, total_ghosts, cur_ghost):
            # print "depth=", cur_depth, "min called"
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            moves = state.getLegalActions(cur_ghost)
            total_actions = len(moves)
            score = float(0)
            if cur_ghost == total_ghosts:

                for m in moves:
                    next_state = state.generateSuccessor(cur_ghost, m)
                    score += max_expectimax(next_state, cur_depth, total_ghosts)
            else:
                for m in moves:
                    next_state = state.generateSuccessor(cur_ghost, m)
                    score += min_expectimax(next_state, cur_depth, total_ghosts, cur_ghost + 1)

            # print "Score from min = ",score
            return float(score/total_actions)

        def max_expectimax(state, cur_depth, total_ghosts):
            new_depth = cur_depth + 1
            # print "depth=",new_depth,"max called"

            if state.isWin() or state.isLose() or new_depth == self.depth:
                return self.evaluationFunction(state)
            moves = state.getLegalActions(0)
            score = float('-inf')
            for m in moves:
                next_state = state.generateSuccessor(0, m)
                score = max(score, min_expectimax(next_state, new_depth, total_ghosts, 1))
            # print "Score from max = ", score
            return score

        total_ghosts = gameState.getNumAgents() - 1
        moves = gameState.getLegalActions(0)
        best_move = None
        score = float('-inf')

        for m in moves:
            cur_depth = 0
            next_state = gameState.generateSuccessor(0, m)
            old_score = score
            score = max(score, min_expectimax(next_state, cur_depth, total_ghosts, 1))
            if score > old_score:
                best_move = m

        return best_move

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>

      1. Distance to closest food: If distance is more, then pacman has less chance of winning. Therefore,
      the score should be inversely proportional to this value.
      2. Distance to Closest Active Ghost: the less the distance, lesser the chance of winning.
    """
    "*** YOUR CODE HERE ***"

    def distClosestFood(foodList, pacPos):
        dist = []
        for food in foodList:
            dist.append(util.manhattanDistance(food,pacPos))
        # print min(dist)
        # if min(dist) == 0:
        #     return 0.1
        return min(dist)

    def distClosestActiveGhost(ghost_states,pacPos):
        dist = []
        for ghost in ghost_states:
            if not ghost.scaredTimer:
                dist.append(util.manhattanDistance(ghost.getPosition(),pacPos))
        if len(dist) == 0:
            return 1
        return min(dist)


    cur_score = currentGameState.getScore()
    cur_pacPos = currentGameState.getPacmanPosition()
    cur_Food = currentGameState.getFood()
    foodList = cur_Food.asList()
    cur_GhostStates = currentGameState.getGhostStates()
    # print cur_Food
    if currentGameState.isWin():
        return float('inf')
    if currentGameState.isLose():
        return float('-inf')

    foodLeft = len(foodList)
    c = cur_score + 1.0/distClosestFood(foodList,cur_pacPos) \
         + 2.0/distClosestActiveGhost(cur_GhostStates,cur_pacPos)\
        # -5*foodLeft

    # print c
    return c



    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

