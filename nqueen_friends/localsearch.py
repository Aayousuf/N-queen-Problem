'''
Created on Mar 6, 2019

@author: dr.aarij
'''
import searchStrategy
import assignment
import inferenceInfo
import notAttackingConstraint
import math
import random


class LocalSearch(searchStrategy.SearchStrategy):
    '''
    classdocs
    '''


    def __init__(self, inferenceProcdeure,listeners = [],variableOrdering=False,valueOrdering=False,maxSteps = 100000):
        '''
        Constructor
        '''
        searchStrategy.SearchStrategy.__init__(self, listeners)
        self._inferenceProcedure = inferenceProcdeure
        self._variableOrdering = variableOrdering
        self._valueOrdering = valueOrdering
        self._maxSteps = 10000000
        
    def intiliazeRandomly(self,csp):
        self._assignment = assignment.Assignment()
        domainLength = len(csp._domain)
        for va in csp.getVariables():
            self._assignment.addVariableToAssignment(va, csp._domain[random.randint(0,domainLength-1)])
                  
    def solve(self,csp):
        self.intiliazeRandomly(csp)
        
        for _ in range(0,self._maxSteps):
            self.fireListeners(csp, self._assignment)
            notAttackingConstraint.NotAttackingConstraint.att=self._assignment.assigndomain()  
            if self._assignment.isSolution(csp):
                return self._assignment
            cands = self.getConflictedVariable(csp)
            var = cands[random.randint(0,len(cands)-1)]
            val = self.getMinConflictValueFor(var,csp)
            #print(str(var)+"_"+str(val)+"__"+str(len(cands)),'jhb')
            
            self._assignment.addVariableToAssignment(var,val)
            
        return False
    
    def getConflictedVariable(self,csp):
        resultVariables = []
        for con in csp._constraints:
            
            if not self._assignment.isConsistent([con]):
                for var in con.getScope():
                    
                    if var not in resultVariables:
                        resultVariables.append(var)
        
        return resultVariables
    
    def getMinConflictValueFor(self,var,csp):
        
        constraints = csp.getConstraints(var)
        assignment = self._assignment.returnCopy()
        minConflict = 100000000000
        candidates = []
        
        for val in csp.getDomainValues(var):
            assignment.addVariableToAssignment(var,val)
            count = 0
            for con in constraints:
                if not assignment.isConsistent([con]):
                    count+=1
            if count <= minConflict:
                if count < minConflict:
                    candidates = []
                    minConflict = count
                candidates.append(val)
                
        return candidates[random.randint(0,len(candidates)-1)]
    
#     def getMinConflictValueFor(self,var,csp):
#         
#         constraints = csp.getAllConstraintsOfVariable(var)
#         assignment = self._assignment.returnCopy()
#         minConflict = 100000000000
#         candidates = []
#         
#         for val in csp.getDomainValues(var):
#             if val == self._assignment.getAssignmentOfVariable(var):
#                 continue
#             assignment.addVariableToAssignment(var,val)
#             count = 0
#             for con in constraints:
#                 if assignment.isConsistent([con]):
#                     count+=1
#             if count <= minConflict:
#                 if count < minConflict:
#                     candidates = []
#                     minConflict = count
#                 candidates.append(val)
#                 
#         return candidates[random.randint(0,len(candidates)-1)]
    
    def fireListeners(self,csp,assignment):
        for listener in self._listeners:
            listener.fireChange(csp,assignment)