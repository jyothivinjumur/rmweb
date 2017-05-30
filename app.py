# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for
from ModuleP1 import phase1
from ModuleP2 import phase2
from ModuleP3 import phase3
import sys
from CostMatrix import cm
import logging

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('form_submit.html')

def p1caller(costs,alpha):
    try:
        
        costMatrix=cm()
        cmv=costs.split(',')
        costMatrix.setCostMatrix(float(cmv[0]),float(cmv[1]),float(cmv[2]),float(cmv[3]),float(cmv[4]),float(cmv[5]))
        costMatrix.setAlpha(float(alpha.strip()))
        cmvalue=costMatrix.getCostMatrix()
        p1=phase1()
        twd='/app/data'
        p1.classifyDocuments(twd,twd+'/GPOL-ds-op-label.tuple.dictionary.20000.p',twd+'/ECAT-ds-op-label.tuple.dictionary.20000.p',20000,cmvalue,reclassify=False)
    except:
        raise

def p2caller(costs,alpha):
    try:
        costMatrix=cm()
        cmv=costs.split(',')
        costMatrix.setCostMatrix(float(cmv[0]),float(cmv[1]),float(cmv[2]),float(cmv[3]),float(cmv[4]),float(cmv[5]))
        costMatrix.setAlpha(float(alpha.strip()))
        cmvalue=costMatrix.getCostMatrix()
        lamR=costMatrix.getLam_r()
        p2=phase2()
        twd='/app/data'
        p2.computeExpectation(twd,20000,cmvalue,lamR,twd+'/GPOL-ds-op-label.tuple.dictionary.20000.p',twd+'/ECAT-ds-op-label.tuple.dictionary.20000.p')
        Tau_rValue=p2.runphase2(twd+'/GPOL-ds-op-label.tuple.dictionary.20000.p',twd+'/ECAT-ds-op-label.tuple.dictionary.20000.p',twd+'/rcv1_GPOL.txt',twd,20000,0)
        return Tau_rValue
    except:
        raise

def p3caller(costs,alpha):
    try:
        costMatrix=cm()
        cmv=costs.split(',')
        costMatrix.setCostMatrix(float(cmv[0]),float(cmv[1]),float(cmv[2]),float(cmv[3]),float(cmv[4]),float(cmv[5]))
        costMatrix.setAlpha(float(alpha.strip()))
        cmvalue=costMatrix.getCostMatrix()
        lamP=costMatrix.getLam_p()
        twd='/app/data'
        p3=phase3()
        p3.computeExpectation(twd,20000,cmvalue,lamP,twd+'/ECAT-ds-op-label.tuple.dictionary.20000.p')
        Tau_pValue=p3.runphase3(twd+'/ECAT-ds-op-label.tuple.dictionary.20000.p',twd+'/rcv1_ECAT.txt',twd,20000,0)
        return Tau_pValue
    except:
        raise

@app.route('/hybridmodel/', methods=['POST'])
def hybridmodel():
    costs=request.form['yourname']
    alpha=request.form['youremail']
    p1caller(costs,alpha)
    Tau_r=p2caller(costs,alpha)
    Tau_p=p3caller(costs,alpha)
    msg="NONE"
    if Tau_r>0 and Tau_r<20000:
        msg="Review Something"
    elif Tau_r==0:
        msg="Review Nothing"
    else:
        msg="Review Everything"
    return render_template('form_action.html', name=Tau_r, Tau_p=Tau_p, message=msg)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
