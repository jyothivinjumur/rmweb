__author__ = 'jyothi'

import sys

class cm:
    def __init__(self):
        self.lam_r=1.0 # this is the cost value for Lambda_r = $5 per document
        self.lam_p=5.0 # this is the cost value for Lambda_p = $10 per document
        self.costMatrix=[[0 for x in range(3)] for x in range(3)]

    def setCostMatrix(self,cm01,cm02,cm10,cm12,cm20,cm21):
        self.costMatrix[0][0] = 0   # this is the cost value for lamda(PP) user input
        self.costMatrix[0][1] = cm01  # this is the cost value for lamda(PL) user input
        self.costMatrix[0][2] = cm02  # this is the cost value for lamda(PW) user input
        self.costMatrix[1][0] = cm10 # this is the cost value for lamda(LP) user input
        self.costMatrix[1][1] = 0    # this is the cost value for lamda(LL) user input
        self.costMatrix[1][2] = cm12  # this is the cost value for lamda(LW) user input
        self.costMatrix[2][0] = cm20  # this is the cost value for lamda(WP) user input
        self.costMatrix[2][1] = cm21  # this is the cost value for lamda(WL) user input
        self.costMatrix[2][2] = 0 # this is the cost value for lamda(WW) user input

    def setLam_R(self,value):
        self.lam_r=value

    def setLam_P(self,value):
        self.lam_p=value

    def setCondition(self, has502enabled):
        if has502enabled=='true':
            self.costMatrix[0][1]=9.1
        else:
            self.costMatrix[0][1] = 303.03

    def setAlpha(self, alpha):
        if not float(alpha)==1.0:
            for i in range(0,3):
                for j in range(0,3):
                    self.costMatrix[i][j]= float(alpha) * self.costMatrix[i][j]

    def getCellValue(self,row,column):
        return self.costMatrix[row][column]

    def getCostMatrix(self):
        return self.costMatrix

    def getLam_r(self):
        return self.lam_r

    def getLam_p(self):
        return self.lam_p
