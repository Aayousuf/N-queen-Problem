# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 17:55:09 2019

@auumer.aasma yousuf: 
"""
import variable
import copy
import notAttackingConstraint
import simpleInference
import time
import backtrackingSearch
import localsearch
import consoleListener
import arcConsistencyInference
class CSP():
     
    def __init__(self, variables = [], domains = [], constraints = []):
        self._variables = variables
        self._domain = domains
        self._constraints = constraints
        
        self._domainOfVariable = {}
        self._contraintsOfVariable = {}
        self.setUpVariableDomains()
        self.setUpConstraints()
        
    def setUpVariableDomains(self):
        for var in self._variables:
            self.addVariableDomain(var, self._domain)
        
    def setUpConstraints(self):
        for constraint in self._constraints:
            self.addConstraint(constraint)
            
    def addVariableDomain(self,var,domain):
        self._domainOfVariable[var] = copy.deepcopy(domain)
        
    def addConstraint(self,constraint):
        for var in constraint.getScope():
            if var not in self._contraintsOfVariable:
                #print(var,'constraints variable',constraint.getScope())
                self._contraintsOfVariable[var] = []
                self._contraintsOfVariable[var].append(constraint)
            if constraint not in self._contraintsOfVariable[var]:
                 self._contraintsOfVariable[var].append(constraint) 
                 
    def addSingleConstraint(self,constraint):
        self._constraints.append(constraint)
        for var in constraint.getScope():
            if var not in self._contraintsOfVariable:
                self._contraintsOfVariable[var] = []
                self._contraintsOfVariable[var].append(constraint)
                
    
    def addVariable(self,variable):
        self._variables.append(variable)
        self.addVariableDomain(variable,self._domain)
        
    def getVariables(self):
        return self._variables
    
    def getDomainValues(self,var):
        return self._domainOfVariable[var]

    def getConstraints(self,var):
        if var not in self._contraintsOfVariable:
            return []
        return self._contraintsOfVariable[var]
    
    def getVariableDomains(self):
        return self._domainOfVariable
    
    def setVariableDomains(self,domainOfVariable):
        self._domainOfVariable = domainOfVariable
        
    def copy(self):
        variables = copy.deepcopy(self._variables)
        domains = copy.deepcopy(self._variables)
        constraints = copy.deepcopy(self._variables)
        csp = CSP(variables, domains, constraints)
        return csp
    
    def getNeighbour(self,variable,constraint):
        neigh = []
        for va in constraint.getScope():
            if va != variable and (va not in neigh):
                neigh.append(va)
                return neigh 
        return self._contraintsOfVariable
    def removeValueFromDomain(self,variable,value):
        values = []
        for val in self.getDomainValues(variable):
            if val != value:
                values.append(val)
                self._domainOfVariable[variable] = values
    def getneighbourexcept(self,var1,var2):
        neigh = []
        for con in self.getConstraints(var1):
            if var2 not in con.getScope():
                neigh.append(con)
        return neigh
    def setBoard(self,size):
        self.board=size
    def getBoard(self):
        return self.board
    
    @staticmethod                    
    def createnightCSP(nqueen,n):
        variables = []
        domains = []
        constraints = []
        
        
        if nqueen > n-1:
            print('max queen can only ',n-1)
            return False 
        for i in range(nqueen):
            variables.append("Q%d"%(i+1))
        
        for i in range(n):
            for j in range(n):
                domains.append([i,j])
                #print(i,j, end =" ")
            #print('')
        for i in range(nqueen-1):
            for j in range(i+1,nqueen):
                
                constraints.append(notAttackingConstraint.NotAttackingConstraint(variables[i] , variables[j]))
        
        
        return CSP(variables,domains,constraints)
        
            
                
if __name__ == '__main__':
 
    nqueen=8
    n=9
    csp=CSP().createnightCSP(nqueen,n)
    if csp:
        csp.setBoard(n)
        notAttackingConstraint.NotAttackingConstraint.n=n 
        inPro = simpleInference.SimpleInference()
        #inPro=forwardCheckingInference.ForwardCheckingInference()
        #inPro=arcConsistencyInference.ArcConsistencyInference()
        #bts = localsearch.LocalSearch([consoleListener.ConsoleListener()],variableOrdering = True) 
        
        bts = backtrackingSearch.BactrackingSearch(inPro,[consoleListener.ConsoleListener()],variableOrdering = True)
        start = time.time()
        result = bts.solve(csp)
        end = time.time()
        
        print("%.2f ‐ %.2f" % (start,end))
    else:
        print('again enter K-night')
