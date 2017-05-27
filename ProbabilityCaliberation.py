__author__ = 'jyothi'


import math
import cPickle
import sys

class Probabilities:
    def __init__(self):
        self.platt_params={}
        self.platt_params['GCAT']=(-3.4691414065263144,-0.13719639846313605)
        self.platt_params['CCAT']=(-3.0399279961917069,-0.13586854190852918)
        self.platt_params['MCAT']=(-3.4346707380440957,0.0056597239972020772)
        self.platt_params['GPOL']=(-3.3043099615863412,-0.023626049322927944)
        self.platt_params['GDIP']=(-3.7001228975833436,-0.06519881163203084)
        self.platt_params['ECAT']=(-3.0729808755097685,-0.16442790802646404)


    def getCaliberatedProbabilities(self,workDir,testSetSize,category,tDfilepath,tLfilepath):
        tInsDPL={}
        testInsScores={}
        testInsLabs={}
        testInsProbabilities={}
        paramFields=self.platt_params[category]#.replace('(','').replace(')','').split(',')
        paramA=float(paramFields[0])
        paramB=float(paramFields[1])
        f = open(tDfilepath, 'r')
        print paramFields
        lines=f.readlines()
        f.close()
        counter=1
        for l in lines:
            testInsScores[counter]=float(l.strip('\n'))
            counter=counter+1

        fl = open(tLfilepath, 'r')
        labs=fl.readlines()
        fl.close()

        c=1
        for l in labs:
            testInsLabs[c]=int(l.strip('\n'))
            c=c+1

        for k,v in testInsScores.iteritems():
            plattProbability=(float(1.0)/float(1.0 + math.exp((v*paramA)+paramB)))
            testInsProbabilities[k]=plattProbability
        for k,v in testInsProbabilities.iteritems():
            dplTuple=(float(v),float(testInsScores[k]),int(testInsLabs[k]))
            tInsDPL[k]=dplTuple

        if testSetSize==23149:
            cPickle.dump(tInsDPL,open(workDir+"/pickleFiles/ds-op-label.tuple.dictionary."+str(testSetSize)+".p", "wb"))
        else:
            cPickle.dump(tInsDPL,open(workDir+"/pickleFiles/ds-op-label.tuple.dictionary."+str(testSetSize)+".p", "wb"))

def main(argv):
    try:
        caliberatedProbabilities=Probabilities()
        # argv[0] = Path of Working Directory
        # argv[1] = Platt PARAMETERS
        # argv[2] = Prediction file path ; $wd/predictions/test/prediction.tCount.$testsetSize.dat
        # argv[3]= Truth Labels file path;  $wd/testinsf.$testsetSize.count.lables.dat
        # argv[4] = No. of files in test-set
        # argv[5] = boolean value ; CV true or false
        tup=caliberatedProbabilities.getCaliberatedProbabilities(argv[0],argv[4],argv[1],argv[2],argv[3])
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])