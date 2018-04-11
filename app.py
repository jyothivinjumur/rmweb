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
from logging.handlers import RotatingFileHandler


# Initialize the Flask application
app = Flask(__name__)

# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('form_submit.html')

def p1caller(pl,pw,lp,lw,wp,wl,alpha):
    try:
        costMatrix=cm()
        costMatrix.setCostMatrix(float(pl),float(pw),float(lp),float(lw),float(wp),float(wl))
        costMatrix.setAlpha(float(alpha.strip()))
        cmvalue=costMatrix.getCostMatrix()
        p1=phase1()
        twd='/app/data'
        p1.classifyDocuments(twd,twd+'/GPOL-ds-op-label.tuple.dictionary.199328.p',twd+'/ECAT-ds-op-label.tuple.dictionary.199328.p',199328,cmvalue,reclassify=False)
    except:
        raise

def p2caller(pl,pw,lp,lw,wp,wl,alpha,lambda_R):
    try:
        costMatrix=cm()
        costMatrix.setCostMatrix(float(pl),float(pw),float(lp),float(lw),float(wp),float(wl))
        costMatrix.setAlpha(float(alpha.strip()))
        cmvalue=costMatrix.getCostMatrix()
        costMatrix.setLam_R(float(lambda_R))
        lamR=lambda_R
        p2=phase2()
        twd='/app/data'
        p2.computeExpectation(twd,199328,cmvalue,lamR,twd+'/GPOL-ds-op-label.tuple.dictionary.199328.p',twd+'/ECAT-ds-op-label.tuple.dictionary.199328.p')
        Tau_rValue=p2.runphase2(twd+'/GPOL-ds-op-label.tuple.dictionary.199328.p',twd+'/ECAT-ds-op-label.tuple.dictionary.199328.p',twd+'/rcv1_GPOL.txt',twd,199328,0)
        return Tau_rValue
    except:
        raise

def p3caller(pl,pw,lp,lw,wp,wl,alpha,lambda_P):
    try:
        costMatrix=cm()
        costMatrix.setCostMatrix(float(pl),float(pw),float(lp),float(lw),float(wp),float(wl))
        costMatrix.setAlpha(float(alpha.strip()))
        cmvalue=costMatrix.getCostMatrix()
        costMatrix.setLam_P(float(lambda_P))
        lamP=float(lambda_P)
        twd='/app/data'
        p3=phase3()
        p3.computeExpectation(twd,199328,cmvalue,lamP,twd+'/ECAT-ds-op-label.tuple.dictionary.199328.p')
        Tau_pValue=p3.runphase3(twd+'/ECAT-ds-op-label.tuple.dictionary.199328.p',twd+'/rcv1_ECAT.txt',twd,199328,0)
        return Tau_pValue
    except:
        raise

@app.route('/hybridmodel/', methods=['POST'])
def hybridmodel():
    username=request.form['uname']
    pl=request.form['lamPL']
    pw=request.form['lamPW']
    lp=request.form['lamLP']
    lw=request.form['lamLW']
    wp=request.form['lamWP']
    wl=request.form['lamWL']
    lambda_R=request.form['lamR']
    lambda_P=request.form['lamP']    
    app.logger.info("User Inputs; Username is %s",username)
    app.logger.info("pl= %s",pl)
    app.logger.info("pw= %s",pw)
    app.logger.info("lp= %s",lp)
    app.logger.info("lw= %s",lw)
    app.logger.info("wp= %s",wp)
    app.logger.info("wl= %s",wl)
    app.logger.info("Lambda_P= %s",lambda_P)
    app.logger.info("Lambda_R= %s",lambda_R)
    alpha="1.0"
    p1caller(pl,pw,lp,lw,wp,wl,alpha)
    Tau_r=p2caller(pl,pw,lp,lw,wp,wl,alpha,float(lambda_R))
    Tau_p=p3caller(pl,pw,lp,lw,wp,wl,alpha,float(lambda_P))
    Tau_r_percent=float(Tau_r)/199328*100.0
    Tau_p_percent=float(Tau_p)/199328*100.0
    msg="NONE"
    if Tau_r>0 and Tau_r<199328:
        msg="Review Something"
    elif Tau_r==0:
        msg="Review Nothing"
    else:
        msg="Review Everything"
    return render_template('form_action.html', Taur=Tau_r, Tau_rpercent=Tau_r_percent, Taup=Tau_p, Tau_ppercent=Tau_p_percent, message=msg)

if __name__ == '__main__':
    handler = RotatingFileHandler('/app/logs/logfile.log', maxBytes=10000, backupCount=10)
    FORMAT = "%(asctime)-15s %(message)s"
    fmt = logging.Formatter(FORMAT,datefmt='%Y-%m-%d %H:%M:%S')
    FORMAT = "%(asctime)-15s %(message)s"
    handler.setFormatter(fmt)
    handler.setLevel(logging.INFO)
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=80)
