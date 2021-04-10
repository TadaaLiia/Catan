from gamestate import Gamestate
from simulation import Simulation
import math


class GametreeNode:
    def __init__(self, gamestate, move=None):
        self.parent = None
        self.children = []
        self.gamestate = gamestate
        # value measures the total wins
        self.value = 0
        self.simulations = 0
        self.move = move

    def hasChild(self):
        return len(self.children) > 0

    def addChild(self, child):
        self.children.append(child)
        child.parent = self

    def hasParent(self):
        return not self.parent == None

    def update(self, v):
        self.v += v
        self.simulations += 1


class MCTSHandler():
    def __init__(self, node, EXPLORATION_PARAMETER=1):
        self.GametreeNode = node
        self.EXPLORATION_PARAMETER = EXPLORATION_PARAMETER

    def calcUCB1(self, node):
        if node.simulations > 0:
            return math.inf
        return Node.v / (1. * Node.NumGames) + (EXPLORATION_PARAMETER * math.sqrt(
            20 * math.log(Node.parent.NumGames) / (1. * Node.NumGames)))

    def selection(self, node=self.GametreeNode):
        while node.hasChild():
            node = max([self.calcUCB1(child) for child in node.children])
        return node

    def expansion(self, node):
        Simulation = simulation(node.gamestate)
        for move in Simulation.getListOfLegalMoves():
            node.addChild(GametreeNode(Simulation.getNextState(move), move))

    def simulation(self, node):
        Simulation = simulation(node.gamestate)
        # Result should be 1 or 0 depending on if the Game was won or not
        result = simulation.simulateRandomGame(node.gamestate)
        return result

    def backpropagation(self, node, result):
        while node.parent is not None:
            node.update(result)
            node = node.parent

    def getBestMove(self, node, SIMULATION_DEPTH):
        for i in range(20000):
            selectedNode = self.selection()
            self.expansion(selectedNode)
            result = self.simulation(selectedNode)
            self.backpropagation(selectedNode, result)
        return
