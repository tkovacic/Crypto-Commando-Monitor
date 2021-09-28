#Title: util.py
#Author: Timothy Damir Kovacic
import cbpro

import time
import logging
from datetime import date, datetime, timedelta
from pytz import timezone
import os
import sys
import config

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',datefmt='%Y-%m-%d:%H:%M:%S',level=logging.ERROR);
logger = logging.getLogger(__name__);
eastern = timezone('US/Eastern');

global OKCYAN;
OKCYAN = '\033[96m';
global OKGREEN;
OKGREEN = '\033[92m';
global FAIL;
FAIL = '\033[91m';
global WARN;
WARN = '\033[93m';

def printInterface(market, tv, dl, pp, cp, yp, ldl, lb, ls, tmpDelta, client):
    print(OKCYAN + "Yesterday's Starting Price (YSP): " + str(round(float(yp),3)) + " " + str(market)[4:]);
    print(OKCYAN + "Today's Delta (TD): " + str(tmpDelta) + "%");
    print(OKCYAN + "Current Delegation Level (CDL): " + str(ldl));
    print("");
    if(float(pp) > 0):
        print(OKCYAN + "Today's Previous Price (TPP): " + str(round(float(pp),3)) + " " + str(market)[4:]);
        print("Today's Current Price (TCP): " + str(float(cp)) + " " + str(market)[4:]);
    else:
        print(OKCYAN + "Calibrating...");
    print("");

    totalAdaHoldings = (float(tv) + ((4/5) * float(tv)) + ((3/5) * float(tv)) + ((2/5) * float(tv)) + ((1/5) * float(tv)) + ((1/10) * float(tv)));
    totalUsdHoldings = float(totalAdaHoldings) * float(cp);

    print("Margins: " + str(totalAdaHoldings) + " " + str(market)[0:3] + " / " + str(round(float(totalUsdHoldings),2)) + " " + str(market)[4:] + " || Total: " + str(round(float(totalUsdHoldings)*2,2)) + " " + str(market)[4:]);
    print("Holding: " + str(round(float(client.get_account(config.COIN_ID)["balance"]),2)) + " " + str(market)[0:3] + " / " + str(round(float(client.get_account(config.FIAT_ID)["balance"]),2)) + " " + str(market)[4:] + " || Total: " + str(round((round(float(client.get_account(config.COIN_ID)["balance"]),2) * float(cp)) + round(float(client.get_account(config.FIAT_ID)["balance"]),2)),2) + " " + str(market)[4:]);
    print("");

    if(float(lb) == -9999999999):
        print("Last BO Price: N/A");
    else:
        print("Last BO Price: " + str(lb) + " " + str(market)[4:]);

    if(float(ls) == 9999999999):
        print("Last SO Price: N/A");
    else:
        print("Last SO Price: " + str(ls) + " " + str(market)[4:]);

def fetchCurrentQuote(market, client):
    bids = client.get_product_order_book(str(market));
    q = bids["bids"][0][0];
    return str(q);

def fetchYesterdayQuote(market, client):
    today = datetime.now();
    yesterday = today - timedelta(1);
    past = today - timedelta(2);
    stats = client.get_product_historic_rates(str(market), start=past, end=yesterday, granularity=86400)
    s = stats[0][4];
    return str(s);

def placeBuyOrder(market, client, volume, cp, lb, ls):
    if(float(cp) < float(ls)):
        client.place_market_order(str(market),"buy",str(volume));
        lb = cp;

    return lb;

def placeSellOrder(market, client, volume, cp, lb, ls):
    if(float(cp) > float(lb)):
        client.place_market_order(str(market),"sell",str(volume));
        ls = cp;

    return ls;

def obtainUpperDelegation(ldl, yp, delegationLevels):
    if(float(ldl) == 0.0):
        return float(delegationLevels[8]);
    elif(float(ldl) == 1.0):
        return float(delegationLevels[7]);
    elif(float(ldl) == 2.0):
        return float(delegationLevels[6]);
    elif(float(ldl) == 3.0):
        return float(delegationLevels[5]);
    elif(float(ldl) == 4.0):
        return float(yp);
    elif(float(ldl) == 5.0):
        return float(delegationLevels[0]);
    elif(float(ldl) == 6.0):
        return float(delegationLevels[1]);
    elif(float(ldl) == 7.0):
        return float(delegationLevels[2]);
    elif(float(ldl) == 8.0):
        return float(delegationLevels[3]);
    elif(float(ldl) == 9.0):
        return float(delegationLevels[4]);
    elif(float(ldl) == 10.0):
        return float(delegationLevels[4]);

def obtainLowerDelegation(ldl, yp, delegationLevels):
    if(float(ldl) == 0.0):
        return float(delegationLevels[9]);
    elif(float(ldl) == 1.0):
        return float(delegationLevels[9]);
    elif(float(ldl) == 2.0):
        return float(delegationLevels[8]);
    elif(float(ldl) == 3.0):
        return float(delegationLevels[7]);
    elif(float(ldl) == 4.0):
        return float(delegationLevels[6]);
    elif(float(ldl) == 5.0):
        return float(delegationLevels[5]);
    elif(float(ldl) == 6.0):
        return float(yp);
    elif(float(ldl) == 7.0):
        return float(delegationLevels[0]);
    elif(float(ldl) == 8.0):
        return float(delegationLevels[1]);
    elif(float(ldl) == 9.0):
        return float(delegationLevels[2]);
    elif(float(ldl) == 10.0):
        return float(delegationLevels[3]);

def calculateDelegationLevels(dl, yp):
    pd1 = float(yp) + float(dl);
    pd2 = float(pd1) + float(dl);
    pd3 = float(pd2) + float(dl);
    pd4 = float(pd3) + float(dl);
    pd5 = float(pd4) + float(dl);
    nd1 = float(yp) - float(dl);
    nd2 = float(nd1) - float(dl);
    nd3 = float(nd2) - float(dl);
    nd4 = float(nd3) - float(dl);
    nd5 = float(nd4) - float(dl);

    output = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0];
    output[0] = float(pd1);
    output[1] = float(pd2);
    output[2] = float(pd3);
    output[3] = float(pd4);
    output[4] = float(pd5);
    output[5] = float(nd1);
    output[6] = float(nd2);
    output[7] = float(nd3);
    output[8] = float(nd4);
    output[9] = float(nd5);

    return output;

def evaluateDelegationLevelCrossing(market, dll, ldl, yp, cp, tv, lb, ls, purchases, sales, client):
    pd1 = float(dll[0]);
    pd2 = float(dll[1]);
    pd3 = float(dll[2]);
    pd4 = float(dll[3]);
    pd5 = float(dll[4]);

    nd = float(yp);

    nd1 = float(dll[5]);
    nd2 = float(dll[6]);
    nd3 = float(dll[7]);
    nd4 = float(dll[8]);
    nd5 = float(dll[9]);

    if(float(ldl) == 0.0):
        if(float(cp) >= float(nd4)):
            ldl = 1.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Sell " + str(v) + " " + str(market)[0:3]);
            ls = placeSellOrder(market,client, v, cp, lb, ls);
            sales.append(float(cp));
        elif(float(cp) <= float(nd5)):
            ldl = 0.0;
    elif(float(ldl) == 1.0):
        if(float(cp) >= float(nd3)):
            ldl = 2.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Sell " + str(v) + " " + str(market)[0:3]);
            ls = placeSellOrder(market,client, v, cp, lb, ls);
            sales.append(float(cp));
        elif(float(cp) <= float(nd5)):
            ldl = 0.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Purchase " + str(v) + " " + str(market)[0:3]);
            lb = placeBuyOrder(market,client, v, cp, lb, ls);
            purchases.append(float(cp));
    elif(float(ldl) == 2.0):
        if(float(cp) >= float(nd2)):
            ldl = 3.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Sell " + str(v) + " " + str(market)[0:3]);
            ls = placeSellOrder(market,client, v, cp, lb, ls);
            sales.append(float(cp));
        elif(float(cp) <= float(nd4)):
            ldl = 1.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Purchase " + str(v) + " " + str(market)[0:3]);
            lb = placeBuyOrder(market,client, v, cp, lb, ls);
            purchases.append(float(cp));
    elif(float(ldl) == 3.0):
        if(float(cp) >= float(nd1)):
            ldl = 4.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Sell " + str(v) + " " + str(market)[0:3]);
            ls = placeSellOrder(market,client, v, cp, lb, ls);
            sales.append(float(cp));
        elif(float(cp) <= float(nd3)):
            ldl = 2.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Purchase " + str(v) + " " + str(market)[0:3]);
            lb = placeBuyOrder(market,client, v, cp, lb, ls);
            purchases.append(float(cp));
    elif(float(ldl) == 4.0):
        if(float(cp) >= float(nd)):
            ldl = 5.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Sell " + str(v) + " " + str(market)[0:3]);
            ls = placeSellOrder(market,client, v, cp, lb, ls);
            sales.append(float(cp));
        elif(float(cp) <= float(nd2)):
            ldl = 3.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Purchase " + str(v) + " " + str(market)[0:3]);
            lb = placeBuyOrder(market,client, v, cp, lb, ls);
            purchases.append(float(cp));
    elif(float(ldl) == 5.0):
        if(float(cp) <= float(nd1)):
            ldl = 4.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Purchase " + str(v) + " " + str(market)[0:3]);
            lb = placeBuyOrder(market,client, v, cp, lb, ls);
            purchases.append(float(cp));
        elif(float(cp) >= float(pd1)):
            ldl = 6.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Sell " + str(v) + " " + str(market)[0:3]);
            ls = placeSellOrder(market,client, v, cp, lb, ls);
            sales.append(float(cp));
    elif(float(ldl) == 6.0):
        if(float(cp) <= float(nd)):
            ldl = 5.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Purchase " + str(v) + " " + str(market)[0:3]);
            lb = placeBuyOrder(market,client, v, cp, lb, ls);
            purchases.append(float(cp));
        elif(float(cp) >= float(pd2)):
            ldl = 7.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Sell " + str(v) + " " + str(market)[0:3]);
            ls = placeSellOrder(market,client, v, cp, lb, ls);
            sales.append(float(cp));
    elif(float(ldl) == 7.0):
        if(float(cp) <= float(pd1)):
            ldl = 6.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Purchase " + str(v) + " " + str(market)[0:3]);
            lb = placeBuyOrder(market,client, v, cp, lb, ls);
            purchases.append(float(cp));
        elif(float(cp) >= float(pd3)):
            ldl = 8.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Sell " + str(v) + " " + str(market)[0:3]);
            ls = placeSellOrder(market,client, v, cp, lb, ls);
            sales.append(float(cp));
    elif(float(ldl) == 8.0):
        if(float(cp) <= float(pd2)):
            ldl = 7.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Purchase " + str(v) + " " + str(market)[0:3]);
            lb = placeBuyOrder(market,client, v, cp, lb, ls);
            purchases.append(float(cp));
        elif(float(cp) >= float(pd4)):
            ldl = 9.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Sell " + str(v) + " " + str(market)[0:3]);
            ls = placeSellOrder(market,client, v, cp, lb, ls);
            sales.append(float(cp));
    elif(float(ldl) == 9.0):
        if(float(cp) <= float(pd3)):
            ldl = 8.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Purchase " + str(v) + " " + str(market)[0:3]);
            lb = placeBuyOrder(market,client, v, cp, lb, ls);
            purchases.append(float(cp));
        elif(float(cp) >= float(pd5)):
            ldl = 10.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Sell " + str(v) + " " + str(market)[0:3]);
            ls = placeSellOrder(market,client, v, cp, lb, ls);
            sales.append(float(cp));
    elif(float(ldl) == 10.0):
        if(float(cp) <= float(pd4)):
            ldl = 9.0;
            v = calculateDelegationTradeVolume(float(ldl),float(tv));
            print("Ordered to Purchase " + str(v) + " " + str(market)[0:3]);
            lb = placeBuyOrder(market,client, v, cp, lb, ls);
            purchases.append(float(cp));
        elif(float(cp) >= float(pd5)):
            ldl = 10.0;

    output = [0.0,0.0,0.0,[],[]];
    output[0] = ldl;
    output[1] = lb;
    output[2] = ls;
    output[3] = purchases;
    output[4] = sales;

    return output;

def calculateDelegationTradeVolume(dl, tv):
    if(float(dl) == 0 or float(dl) == 10):
        v = float(tv);

    if(float(dl) == 1 or float(dl) == 9):
        v = (4 / 5) * float(tv);

    if(float(dl) == 2 or float(dl) == 8):
        v = (3 / 5) * float(tv);

    if(float(dl) == 3 or float(dl) == 7):
        v = (2 / 5) * float(tv);

    if(float(dl) == 4 or float(dl) == 6):
        v = (1 / 5) * float(tv);

    if(float(dl) == 5):
        v = (1 / 10) * float(tv);

    return float(v);

def identifyLastDelegationLevel(dll, yp, cp):
    pd1 = float(dll[0]);
    pd2 = float(dll[1]);
    pd3 = float(dll[2]);
    pd4 = float(dll[3]);
    pd5 = float(dll[4]);

    nd = float(yp);

    nd1 = float(dll[5]);
    nd2 = float(dll[6]);
    nd3 = float(dll[7]);
    nd4 = float(dll[8]);
    nd5 = float(dll[9]);

    if(float(cp) > float(pd5)):
        return 10.0;

    if((float(pd4) <= float(cp)) and float(cp) <= float(pd5)):
        return 9.0;

    if((float(pd3) <= float(cp)) and float(cp) <= float(pd4)):
        return 8.0;

    if((float(pd2) <= float(cp)) and float(cp) <= float(pd3)):
        return 7.0;

    if((float(pd1) <= float(cp)) and float(cp) <= float(pd2)):
        return 6.0;

    if((float(nd) <= float(cp)) and float(cp) <= float(pd1)):
        return 5.0;

    if((float(nd1) <= float(cp)) and float(cp) <= float(nd)):
        return 5.0;

    if((float(nd2) <= float(cp)) and float(cp) <= float(nd1)):
        return 4.0;

    if((float(nd3) <= float(cp)) and float(cp) <= float(nd2)):
        return 3.0;

    if((float(nd4) <= float(cp)) and float(cp) <= float(nd3)):
        return 2.0;

    if((float(nd5) <= float(cp)) and float(cp) <= float(nd4)):
        return 1.0;

    if(float(cp) < float(nd5)):
        return 0.0;
