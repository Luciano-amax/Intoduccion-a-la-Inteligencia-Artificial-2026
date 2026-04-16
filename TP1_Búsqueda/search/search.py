# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

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




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    start_state = problem.getStartState() # Estado inicial
    if problem.isGoalState(start_state):
        return [] # Si el estado inicial es el objetivo devuelvo lista vacia

    frontier = util.Stack() # Pila
    frontier.push((start_state, [])) # Guardo tuplas (estado,camino)
    visited = {start_state} # Para no repetir estados (es un conjunto)

    while not frontier.isEmpty(): # Mientras haya nodo que visitar
        state, path = frontier.pop() # Sacamos el ultimo agregado

        if problem.isGoalState(state): # Si resolvi, devuelvo camino
            return path
        
        """
        successor = nuevo estado
        action = como llegue hasta ese punto
        _ = costo  
        """
        for successor, action, _ in problem.getSuccessors(state):
            if successor not in visited: # Evito meter estados ya visitados
                visited.add(successor) # Marcamos como visitado
                frontier.push((successor, path + [action])) # Lo agregamos a la pila y guardo camino actualizado

    return [] # No se encontro el objetivo

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    start_state = problem.getStartState()  # Estado inicial
    if problem.isGoalState(start_state):
        return [] # Si el estado inicial es el objetivo devuelvo lista vacia

    frontier = util.Queue() # Cola
    frontier.push((start_state, [])) # Guardamos estado inical a la cola
    visited = {start_state} # Conjunto de visitados, marcamos incial como visitado para no repetir

    while not frontier.isEmpty(): # Mientras haya nodo por explorar
        state, path = frontier.pop() # Sacamos el primer elemento de la cola

        if problem.isGoalState(state): # Chequeo si el estado es el objetivo
            return path # Devolvemos el camino encontrado

        """
        successor = nuevo estado
        action = como llegue hasta ese punto
        _ = costo  
        """
        for successor, action, _ in problem.getSuccessors(state):
            if successor in visited: 
                continue # Si ya visitamos, lo ignoramos (salteamos de iteracion)
            visited.add(successor) # Marcamos al sucesor como visitado
            frontier.push((successor, path + [action])) # Lo agregamos a la cola y guardo camino actualizado

    return [] # Si no encontramos nada, devolvemos lista vacia

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    frontier = util.PriorityQueue() # Cola de prioridad
    start_state = problem.getStartState() # Estado inicial
    frontier.push((start_state, [], 0), 0) # Metemos estado incial en la cola de prioridad
    # (estado incial, camino vacio, costo acumulado)

    best_costs = {start_state: 0}
    expanded_costs = {}

    while not frontier.isEmpty():
        state, path, cost = frontier.pop()

        if cost > best_costs.get(state, float('inf')):
            continue

        if problem.isGoalState(state): # Chequeo si el estado es el objetivo
            return path # Devolvemos el camino encontrado

        if state in expanded_costs and expanded_costs[state] <= cost:
            continue
        expanded_costs[state] = cost

        '''
        successor = siguiente estado
        action = movimiento hecho
        step_cost = costo de ese paso
        '''
        for successor, action, step_cost in problem.getSuccessors(state):
            new_cost = cost + step_cost
            '''
            cost -> g(n) donde n = actual
            new_cost -> g(n) donde n = sucesor
            ''' 
            if new_cost < best_costs.get(successor, float('inf')):
                best_costs[successor] = new_cost
                frontier.push((successor, path + [action], new_cost), new_cost)

    return []

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = util.PriorityQueue()
    start_state = problem.getStartState()
    frontier.push((start_state, [], 0), heuristic(start_state, problem))
    # Seria como push (item, prioridad) donde item = estado, path, costo

    best_costs = {start_state: 0}
    expanded_costs = {}  

    while not frontier.isEmpty(): # Mientras haya nodo sigo buscando
        state, path, cost = frontier.pop() # Saco nodo para procesar

        if cost > best_costs.get(state, float('inf')): 
            continue
            '''
            costo actual > mejor  costo conocido
            '''
        if problem.isGoalState(state):
            return path

        if state in expanded_costs and expanded_costs[state] <= cost:
            continue
        expanded_costs[state] = cost

        for successor, action, step_cost in problem.getSuccessors(state):
            new_cost = cost + step_cost
            if new_cost < best_costs.get(successor, float('inf')):
                best_costs[successor] = new_cost
                priority = new_cost + heuristic(successor, problem) # f(n) = g(n) + h(n)
                frontier.push((successor, path + [action], new_cost), priority)

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
