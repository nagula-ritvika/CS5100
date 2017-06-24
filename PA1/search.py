# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()

    visited_states = set()
    fringe = util.Stack()
    actions = []
    fringe.push((start_state,actions))
    while(not fringe.isEmpty()):
        node,actions = fringe.pop()
        # print "popped ",node,"  Actions = ",actions
        visited_states.add(node)
        # print visited_states
        if problem.isGoalState(node):
            return actions
        s_list = problem.getSuccessors(node)
        # print s_list
        for s in s_list:
            # print s
            n,a,c = s
            if n not in visited_states:
                # print "pushing ",n
                actions_new = actions+[a]
                fringe.push((n, actions_new))
        # print "final actions=",n,actions
        # print fringe

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    visited_states = set()
    fringe = util.Queue()
    actions = []
    fringe.push((start_state, actions))
    while(not fringe.isEmpty()):
        node, actions = fringe.pop()
        visited_states.add(node)
        if problem.isGoalState(node):
            return actions
        s_list = problem.getSuccessors(node)
        for s in s_list:
            n, a, c = s
            if n not in visited_states:
                actions_new = actions + [a]
                fringe.push((n, actions_new))
                visited_states.add(n)

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    visited_states = set()
    fringe = util.PriorityQueue()
    actions = []
    fringe.push((start_state, actions,0),0)
    while not fringe.isEmpty():
        node, actions, priority = fringe.pop()
        # print "popping",node,"with p = ",priority
        # print visited_states
        if node not in visited_states:
            visited_states.add(node)
            if problem.isGoalState(node):
                return actions
            s_list = problem.getSuccessors(node)
            for s in s_list:
                n, a, c = s
                if n not in visited_states:
                    actions_new = actions + [a]
                    c_new = priority + c
                    fringe.push((n, actions_new, c_new),c_new)


    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    visited_states = set()
    fringe = util.PriorityQueue()
    actions = []
    fringe.push((start_state, actions, 0), 0)
    while (not fringe.isEmpty()):
        node, actions, priority = fringe.pop()
        # print "popping",node,"with p = ",priority
        # print visited_states
        if node not in visited_states:
            visited_states.add(node)
            if problem.isGoalState(node):
                return actions
            heuristic_parent = heuristic(node,problem)
            s_list = problem.getSuccessors(node)
            for s in s_list:
                n, a, f = s
                heuristic_n = heuristic(n,problem)
                # since we are storing the f(n) with each and
                # when we extract the cost we should subtract that of the parent node
                # from the cost
                f_new = priority + heuristic_n + f - heuristic_parent
                if n not in visited_states:
                    actions_new = actions + [a]
                    fringe.push((n, actions_new, f_new), f_new)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
