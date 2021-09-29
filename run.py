#Title: run.py
#Author: Timothy Damir Kovacic
import cbpro

import time
import logging
from datetime import date, datetime, timedelta
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.append("./CC");
import config
from util import obtainUpperDelegation, obtainLowerDelegation, evaluateDelegationLevelCrossing, identifyLastDelegationLevel, calculateDelegationLevels, fetchCurrentQuote, fetchYesterdayQuote, printInterface

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',datefmt='%Y-%m-%d:%H:%M:%S',level=logging.ERROR);
logger = logging.getLogger(__name__);

global OKCYAN;
OKCYAN = '\033[96m';
global OKGREEN;
OKGREEN = '\033[92m';
global FAIL;
FAIL = '\033[91m';
global WARN;
WARN = '\033[93m';

print("Author: Timothy Damir Kovacic");
print("Date: September 2021");
time.sleep(1);

global st;
st = time.time();
global cycle_count;
cycle_count = 0;
global increment_pace;
increment_pace = float(config.SEC_INTERVAL);

print("Keep Alive Interval: " + str(increment_pace) + " sec");
print("Auto-Save Every " + str(config.SAVE_INTERVAL) + " Intervals");
print("Max Charted Intervals: " + str(config.CHART_LENGTH));
time.sleep(1);

print("Loading Data...");

global dl;
dl = float(config.DELEGATION_LEVEL);
global tv;
tv = float(config.TRADE_VOLUME);
global pp;
pp = -1.00;
global cp;
cp = -1.00;
global yp;
yp = -1.00;
global ldl;
ldl = -1.0;
global lb;
lb = -9999999999;
global ls;
ls = 9999999999;
global yData;
yData = [];
global d;
d = 0.0;
global market;
market = str(config.MARKET);
global autoSave;
autoSave = 0;

global purchases;
purchases = [];
global sales;
sales = [];
global profits;
profits = 0.00;

print("Delegation Levels: " + str(dl) + " " + str(market)[4:]);
print("Trade Volume: " + str(tv) + " " + str(market)[0:3]);
print("Retraction Rate: " + str(float(config.RETRACTION_RATE) * 100) + "%");

cdaModeText = "INACTIVE";
if(config.CDA_MODE >= 1):
    cdaModeText = "ACTIVE";
print("CDA MODE: " + cdaModeText);
time.sleep(2);

print("Selected Coin: " + str(market)[0:3]);
print("Selected Fiat: " + str(market)[4:]);
time.sleep(1);

print("Starting...");
time.sleep(15);

plt.ion();
plt.title("CC " + str(market)[0:3] + " Monitor [YSP Delta: Calibrating...]");
plt.xlabel(str(increment_pace) + " Second Intervals");
plt.ylabel(str(market)[4:] + " Price per " + str(market)[0:3]);
plt.show();

ypData = [];
pData = [];
sData = [];
udData = [];
ldData = [];

while True:
    os.system('cls');
    st = time.time();

    cycle_count = cycle_count + 1;
    print(OKCYAN + "Market: " + str(market));
    print("Interval: " + str(cycle_count));
    print("Runtime: " + str((float(cycle_count) * float(increment_pace))) + " Seconds");

    client = cbpro.AuthenticatedClient(config.API_KEY,config.API_SEC,config.API_PHR);

    pp = cp;
    cp = fetchCurrentQuote(market, client);
    pyp = float(yp);
    yp = fetchYesterdayQuote(market, client);
    delegationLevels = calculateDelegationLevels(dl, yp);

    if(float(pyp) != float(yp)):
        ldl = identifyLastDelegationLevel(delegationLevels, yp, cp);

    yData.append(float(cp));

    if(ldl < 0):
        ldl = identifyLastDelegationLevel(delegationLevels, yp, cp);
    tmpLdl = ldl;

    metaData = evaluateDelegationLevelCrossing(market, delegationLevels, ldl, yp, cp, tv, lb, ls, purchases, sales, profits, client);
    ldl = metaData[0];
    lb = metaData[1];
    ls = metaData[2];
    purchases = metaData[3];
    sales = metaData[4];
    profits = metaData[5];

    if(float(tmpLdl) != float(ldl)):
        print("LDL Transitioned from: " + str(float(tmpLdl)) + " to: " + str(float(ldl)));

    tmpDelta = round((((float(cp) - float(yp)) / float(cp)) * 100),2);

    ypData.append(float(yp));
    if(len(purchases) > 0):
        pData.append(purchases[-1]);
    else:
        pData.append(yData[-1]);
    if(len(sales) > 0):
        sData.append(sales[-1]);
    else:
        sData.append(yData[-1]);

    upperDelegation = obtainUpperDelegation(ldl, yp, delegationLevels);
    lowerDelegation = obtainLowerDelegation(ldl, yp, delegationLevels);

    udData.append(float(upperDelegation));
    ldData.append(float(lowerDelegation));

    chartLength = float(-1 * float(config.CHART_LENGTH));

    pData = pData[int(chartLength):];
    sData = sData[int(chartLength):];
    udData = udData[int(chartLength):];
    ypData = ypData[int(chartLength):];
    ldData = ldData[int(chartLength):];
    yData = yData[int(chartLength):];

    plt.plot(pData,c='r', ls=':', label="BO");
    plt.plot(sData,c='g', ls=':', label="SO");
    plt.plot(udData,c='y', ls='dashed', label="UDL");
    plt.plot(ypData,c='k', ls='dashed', label="YSP");
    plt.plot(ldData,c='m', ls='dashed', label="LDL");
    plt.plot(yData,c='b', label="TCP");

    plt.legend();
    plt.draw();
    plt.pause(0.0001);
    plt.clf();
    plt.title("CC " + str(market)[0:3] + " Monitor [YSP Delta: " + str(tmpDelta) + "%]");
    plt.xlabel(str(increment_pace) + " Second Intervals");
    plt.ylabel(str(market)[4:] + " Price per " + str(market)[0:3]);
    plt.show();

    printInterface(market, tv, dl, pp, cp, yp, ldl, lb, ls, profits, tmpDelta, client);

    if(float(autoSave) >= float(config.SAVE_INTERVAL)):
        autoSave = 0;
    else:
        autoSave = autoSave + 1;

    time.sleep(increment_pace - ((time.time() - st) % increment_pace));
