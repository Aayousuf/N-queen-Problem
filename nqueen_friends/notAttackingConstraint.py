'''
Created on Mar 6, 2019

@author: dr.aarij
'''
import constraint

class NotAttackingConstraint(constraint.Constraint):
    '''
    classdocs
    '''
    n=0
    def __init__(self, var1, var2):
        '''
        Constructor
        '''
        self._scope = [var1,var2]
        self.li=[]
        
    def getScope(self):
        return self._scope
    
    def isConsistentWith(self,assignment):
        val1 = assignment.getAssignmentOfVariable(self._scope[0])
        val2 = assignment.getAssignmentOfVariable(self._scope[1])
        
        return val1 == None or val2 == None or self.checkAttack(val1,val2)
    
    def checkAttack(self,val1,val2):
        
        if val1 == val2:
            return False
       
        val1i,val1j=val1
        val2i,val2j=val2
        if val1i== val2i:
            return False
        if val1j == val2j:
            return False
        digonal=[]
        n=self.n
        while n>0:
            digonal.append([val1i+1,val1j+1])
            digonal.append([val1i+1,val1j-1])
            n=-1
        
        if val2 in digonal:
            return False            
        
        
        return True
    
