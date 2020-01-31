'''
Created on Mar 12, 2019

@author: Dr.aarij
'''
import assignment

class ArcConsistencyInference(object):
    '''
    classdocs
    '''


    def __init__(self):pass
    
    
    #def doInference(self,csp,variable,value):
    def doInference(self,inferenceInfo,csp,variable,value):    
        
        self.assignment = assignment.Assignment()
        self.assignment.addVariableToAssignment(variable, value)
        self.var = variable
        self.val= value
        queue = csp.getConstraints(variable)
        #print('queue',queue)
        pairs = []
        
        for con in queue:
            #con in working
            if len(con.getScope()) == 2:
                obj = [con.getScope()[1],con.getScope()[0],con]
                #print(con.getScope()[1],con.getScope()[0],con)
                pairs.append(obj)
        
        while len(pairs) > 0:
            
            constraint = pairs[0][2]
            #p
            if self.revise(csp, pairs[0][0], pairs[0][1], constraint):
                
                if len(csp.getDomainValues(pairs[0][0])) == 0:
                    return None
                #print('getneighbour',csp.getNeighboursOfVariableExcept(pairs[0][0],pairs[0][1]))                    
                for con in csp.getneighbourexcept(pairs[0][0],pairs[0][1]):
                    
                    if con.getScope()[0] == variable or con.getScope()[1] == variable:
                        continue
                    if con.getScope()[0] == pairs[0][0]:
                        pairs.append([con.getScope()[1],con.getScope()[0],con])
                    else:
                        pairs.append([con.getScope()[0],con.getScope()[1],con])
            del pairs[0]
        return []
    
    def revise(self,csp,var1,var2,constraint):
        revised = False
        dv2Values = [] 
        assig = assignment.Assignment()
        assig.addVariableToAssignment(self.var, self.val)
        if assig.hasAssignmentFor(var2):
            dv2Values.append(self.assignment.getAssignmentOfVariable(var2))
        else:
            dv2Values = csp.getDomainValues(var2)

        for dv1 in csp.getDomainValues(var1):            
            for dv2 in dv2Values:
                if not assig.hasAssignmentFor(var1):               
                    assig.addVariableToAssignment(var1, dv1)
                assig.addVariableToAssignment(var1, dv1)
                if not assig.isConsistent([constraint]):
                    csp.removeValueFromDomain(var1,dv1)
                    revised = True                
        return revised
                