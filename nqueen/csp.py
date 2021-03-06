'''
Created on Mar 6, 2019

@author: dr.aarij
'''
import copy
import variable
import notEqualConstraint
import bactrackingSearch
import consoleListener
import notAttackingConstraint
import simpleInference
import forwardCheckingInference
import time
import unaryNumericConstraint
import allDifferentConstraint
import arcConsistencyInference
import localSearch


class CSP(object):
    '''
    classdocs
    '''


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
                self._contraintsOfVariable[var] = []
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
    
    
    def getAllConstraintsOfVariable(self,var):
        constraintList = []
        if var not in self._contraintsOfVariable:
            return []
        for _,v in self._contraintsOfVariable.items():
            for variableConstraint in v:
                if var in variableConstraint.getScope():
                    if variableConstraint not in constraintList:
                        constraintList.append(variableConstraint)
        return constraintList
    
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
    
    def removeValueFromDomain(self,variable,value):
        values = []
        for val in self.getDomainValues(variable):
            if val != value:
                values.append(val)
        self._domainOfVariable[variable] = values
        
    def getListOfConstraints(self):
        return self._constraints
    
    def getListOfDomains(self):
        return self._domain
    
    def getNeighboursOfVariableExcept(self,var1,var2):
        neigh = []
        for con in self.getConstraints(var1):
            if var2 not in con.getScope():
                neigh.append(con)
        return neigh
        
        
def createMapColoringCSP():
    wa = variable.Variable("WA")
    sa = variable.Variable("SA")
    nt = variable.Variable("NT")
    q = variable.Variable("Q")
    nsw = variable.Variable("NSW")
    v = variable.Variable("V")
    t = variable.Variable("T")
    variables = [wa,sa,nt,q,nsw,v,t]
    domains = ["RED","GREEN","BLUE"]
        
    constraints = [notEqualConstraint.NotEqualConstraint(wa,sa),
                   notEqualConstraint.NotEqualConstraint(wa,nt),
                   notEqualConstraint.NotEqualConstraint(nt,sa),
                   notEqualConstraint.NotEqualConstraint(q,nt),
                   notEqualConstraint.NotEqualConstraint(sa,q),
                   notEqualConstraint.NotEqualConstraint(sa,nsw),
                   notEqualConstraint.NotEqualConstraint(q,nsw),
                   notEqualConstraint.NotEqualConstraint(sa,v),
                   notEqualConstraint.NotEqualConstraint(nsw,v)]
        
    return CSP(variables,domains,constraints)

def createSudokuCSP():
    variables = []
    domains = [1,2,3,4,5,6,7,8,9]
    constraints = []
    rowName ='ABCDEFGHI'
    colName ='123456789'
        
    V = [
        0, 0, 0, 2, 6, 0, 7, 0, 1,
        6, 8, 0, 0, 7, 0, 0, 9, 0,
        1, 9, 0, 0, 0, 4, 5, 0, 0,
        8, 2, 0, 1, 0, 0, 0, 4, 0,
        0, 0, 4, 6, 0, 2, 9, 0, 0,
        0, 5, 0, 0, 0, 3, 0, 2, 8,
        0, 0, 9, 3, 0, 0, 0, 7, 4,
        0, 4, 0, 0, 5, 0, 0, 3, 6,
        7, 0, 3, 0, 1, 8, 0, 0, 0
        ]
    unaryMap = {}
    for i in range(0,9):
        for j in range(0,9):
            varname = rowName[i]+colName[j]
            var1 = Variable(varname)
            variables.append(var1)
            if V[i * 9 + j] != 0:
                unaryMap[var1] = V[i * 9 + j]
                
    for i in range(0,9):
        rowVars = []
        colVars = []
        for j in range(0,9):
            rowVars.append(variables[i*9 + j])
            colVars.append(variables[i + j*9])
        constraints.append(AllDifferentConstraint(rowVars))
        constraints.append(AllDifferentConstraint(colVars))
            
    for i in range(0,9):
        rowRange = int(i/3) * 3
        colRange = (i*3)%9
        varbs = []
        for row in range(rowRange, rowRange+3):
            for col in range(colRange,colRange+3):
                varbs.append(variables[row*9 + col])
        constraints.append(AllDifferentConstraint(varbs))


    csp = CSP(variables,domains,constraints)
    
    for var,value in unaryMap.items():
        csp.addVariableDomain(var,[value])
    
    return csp

def createNQueenCSP(n = 4):
    variables = []
    domains = []
    constraints = []
    for i in range(n):
        variables.append(Variable("Q_%d"%(i+1)))
    for i in range(1,n+1):
        domains.append(i)
    for i in range(n-1):
        for j in range(i+1,n):
            constraints.append(notAttackingConstraint.NotAttackingConstraint(variables[i] , variables[j]))
    return CSP(variables,domains,constraints)
            

if __name__ == "__main__":
#     csp = createMapColoringCSP() 
    csp = createNQueenCSP(200)
#     csp = createSudokuCSP()
     
#     inPro = SimpleInference()
    inPro = forwardCheckingInference.ForwardCheckingInference()
#     inPro = ArcConsistencyInference()     
#     bts = BactrackingSearch(inPro,[ConsoleListener()],variableOrdering = True)
    bts = localSearch.LocalSearch(inPro,[ConsoleListener()],variableOrdering = True) 
     
     
    start = time.time()    
    result = bts.solve(csp)
    end = time.time()
    print(end - start)
    
        
    
        