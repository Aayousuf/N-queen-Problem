'''
Created on Mar 6, 2019

@author: dr.aarij
'''
from searchStrategy import SearchStrategy
from assignment import Assignment
from inferenceInfo import InferenceInfo
import math
import notAttackingConstraint
class BactrackingSearch(SearchStrategy):
    '''
    classdocs
    '''


    def __init__(self, inferenceProcdeure,listeners = [],variableOrdering=False,valueOrdering=False):
        '''
        Constructor
        '''
        SearchStrategy.__init__(self, listeners)
        self._inferenceProcedure = inferenceProcdeure
        self._variableOrdering = variableOrdering
        self._valueOrdering = valueOrdering
        self.consistentlist=[]
    
    def solve(self,csp):
        return self.recursiveBacktrackingSearch(csp, Assignment())
    
    def recursiveBacktrackingSearch(self,csp,assignment):
        if assignment.isComplete(csp.getVariables()):
            self.boardprint(assignment,csp)
            return assignment
        var = self.selectUnAssignedVariable(csp, assignment)
        for value in self.orderDomainValues(csp, var):
            assignment.addVariableToAssignment(var,value)
            self.fireListeners(csp,assignment)
            if self.consistentlist is None:
                self.consistentlist.append(value)
            if assignment.isConsistent(csp.getConstraints(var)):
                if value in self.consistentlist:
                    continue
                self.consistentlist.append(value)
                notAttackingConstraint.NotAttackingConstraint.att = self.consistentlist   
                inference = InferenceInfo(csp,var,value,self._inferenceProcedure)
                inference.doInference(csp, var, value)
                if not inference.isFailure(csp, var, value):
                    inference.setInferencesToAssignments(assignment,csp)
                    result = self.recursiveBacktrackingSearch(csp,assignment)
                    if result is not None:
                        return result
                    inference.restoreDomains(csp)
                  
            assignment.removeVariableFromAssignment(var)
        self.consistentlist.pop()
        
        return None
    
    def selectUnAssignedVariable(self,csp,assignment):
        
        if not self._variableOrdering:
            for var in csp.getVariables():
                if not assignment.hasAssignmentFor(var):
                    return var
        else:
            minimum = math.inf
            resVar = None
            for var in csp.getVariables():
                if not assignment.hasAssignmentFor(var):
                    if len(csp.getDomainValues(var)) < minimum:
                        minimum = len(csp.getDomainValues(var))
                        resVar = var
            return resVar
    
    def orderDomainValues(self,csp,var):
        return csp.getDomainValues(var)
    
    def fireListeners(self,csp,assignment):
        for listener in self._listeners:
            listener.fireChange(csp,assignment)
    def boardprint(self,assign, csp):
        print('The board is:')
        empty=True
        values=assign.getassingvalue()
        for i in range(csp.getBoard( )):
            for j in range(csp.getBoard( )):
               empty=True 
               for value in values:
                  if values[value][0]== i and values[value][1]==j:
                      empty=False
                      print(value, end =" ")
               if empty :       
                   print('A' ,end =" ")
            print(' ')