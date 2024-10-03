# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        
        totalIterations = self.iterations

        states = self.mdp.getStates()
    
        for i in range(totalIterations):
            #create empty dictionary
            copyOfValues = util.Counter()
            for state in states:
                bestAction = self.getAction(state)
                if bestAction != None:
                    copyOfValues[state] = self.getQValue(state, bestAction)
            
            # update values
            self.values = copyOfValues
                            
  
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"

        qValue = 0

        transitions = self.mdp.getTransitionStatesAndProbs(state, action)

        for transition in transitions:
            nextState = transition[0]
            prob = transition[1]
            reward = self.mdp.getReward(state, action, nextState)
            prevValue = self.getValue(nextState)
            tempQ = prob*(reward + self.discount*prevValue)
            qValue+=tempQ
        
        return qValue


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        bestAction = None

        actionValue = float('-inf')
        possibleActions = self.mdp.getPossibleActions(state)

        for action in possibleActions:
            val = self.computeQValueFromValues(state, action)
            if val > actionValue:
                actionValue = val
                bestAction = action
            
        return bestAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class PrioritizedSweepingValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        predecessors = {}

        priorityQ = util.PriorityQueue()

        for state in self.mdp.getStates():
          if not self.mdp.isTerminal(state):
            for action in self.mdp.getPossibleActions(state):
              for transition in self.mdp.getTransitionStatesAndProbs(state, action):
                if transition[0] not in predecessors:
                  predecessors[transition[0]] = {state}
                else:
                  predecessors[transition[0]].add(state)
      
      
        for state in self.mdp.getStates():
          highestQ = float('-inf')
          if not self.mdp.isTerminal(state):
            for action in self.mdp.getPossibleActions(state):
               tempQ = self.getQValue(state, action)
               if tempQ > highestQ:
                  highestQ = tempQ
            currVal = self.values[state]
            diff = abs(currVal - highestQ)
            priorityQ.push(state, -diff)
        

        for i in range (self.iterations):
          if priorityQ.isEmpty():
            break

          currState = priorityQ.pop()
          
          highestQ = float('-inf')
          if not self.mdp.isTerminal(currState):
            for action in self.mdp.getPossibleActions(currState):
                tempQ = self.getQValue(currState, action)
                if tempQ > highestQ:
                  highestQ = tempQ
            self.values[currState] = highestQ
           
        
            for pre in predecessors[currState]:
              highestQ = float('-inf')
              if not self.mdp.isTerminal(pre):
                for action in self.mdp.getPossibleActions(pre):
                  tempQ = self.getQValue(pre, action)
                  if tempQ > highestQ:
                      highestQ = tempQ
                currVal = self.values[pre]
                diff = abs(currVal - highestQ)

                if diff > self.theta:
                  priorityQ.update(pre, -diff)

               

           



              

             
               

                      



