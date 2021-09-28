<div align="center">
  <h1>Crypto Commando Monitor</h1>
  <p>Automated python based cryptographic trading engine built using hard coded rulesets based on conceptualized and customized delegation levels commissioned through CoinBase Pro API Platform by Tim Kovacic using CBPro SDK by DanPaguin</p><br>
  <img src="https://static.wixstatic.com/media/c11e26_98214627f32540f7939870093be0a03b~mv2.png/v1/fill/w_560,h_456,al_c,q_85,usm_0.66_1.00_0.01/vectorstock_19626918_edited.webp">
</div>
<br>

# How To Use CC Monitor
In order to use this tool you must identify what coin and fiat you want to trade against and configure the tool accordingly. You must also understand what delegation level you desire and what trade volume you desire.

Given you selected ADA as your coin and USD as your fiat.
Given you selected $0.05 cents as your delegation level.
Given you selected a trade volume of 20 ADA.

This program bases the day's trades off of yesterday's starting price (YSP).
Given a YSP of $1.00 USD / 1 ADA.

This program will generate 10 delegations. 
5 delegation levels above.
5 delegation levels below.

These delegations will be seperated in price by your provided delegation level based from the day's YSP.

```
DELEGATION10 => $1.25 => 5/5  trade volume order => buy/sell 20 ADA
DELEGATION09 => $1.2  => 4/5  trade volume order => buy/sell 16 ADA
DELEGATION08 => $1.15 => 3/5  trade volume order => buy/sell 12 ADA
DELEGATION07 => $1.1  => 2/5  trade volume order => buy/sell 8 ADA
DELEGATION06 => $1.05 => 1/5  trade volume order => buy/sell 4 ADA
YSP          => $1.00 => 1/10 trade volume order => buy/sell 2 ADA
DELEGATION05 => $0.95 => 1/5  trade volume order => buy/sell 4 ADA
DELEGATION04 => $0.9  => 2/5  trade volume order => buy/sell 8 ADA
DELEGATION03 => $0.85 => 3/5  trade volume order => buy/sell 12 ADA
DELEGATION02 => $0.8  => 4/5  trade volume order => buy/sell 16 ADA
DELEGATION01 => $0.75 => 5/5  trade volume order => buy/sell 20 ADA
```

If today's current price (TCP) breaks into the delegation above it will trigger a sell order and if it breaks into the delegation below it will trigger a buy order. Delegation 1 and 10 will trigger a full trade volume order. Delegation 2 and 9 will trigger a 4/5 trade volume order. Delegation 3 and 8 will trigger a 3/5 trade volume order. Delegation 4 and 7 will trigger a 2/5 trade volume order. Delegation 5 and 6 will trigger a 1/5 trade volume order.

If TCP breaks below Delegation Level 5 and crosses back up past the YSP it will trigger a sell order for 1/10 trade volume.
If TCP breaks above Delegation level 6 and crosses back below past the YSP it will trigger a buy order for 1/10 trade volume.

<img src="https://github.com/tkovacic/Crypto-Commando-Monitor/blob/main/readme1.PNG?raw=true">
</div>

Your margins are the max coin and fiat you need on hand for that 24 hour period to account for possible max price jump or dump with a total in fiat to account for both.
Your holdings are the current coin and fiat you have on hand in your Coinbase Pro account.

<img src="https://github.com/tkovacic/Crypto-Commando-Monitor/blob/main/readme2.PNG?raw=true">
</div>

# Prerequisites
1) Register an account on Coinbase Pro (https://pro.coinbase.com/)
1) Download and Install Git Bash Terminal (https://gitforwindows.org/)
2) Download and Install Python (https://www.python.org/downloads/)
3) Open Git Bash Terminal and Execute:

```
  pip install cbpro
  pip install numpy
  pip install matplotlib
```

4) Rename "tmp-config.py" in /CC to "config.py" and fill it out with your Coinbase Pro API token information (KEY, SEC, and PHR)

```
#API KEY DETAILS FOR CLIENT CONNECTION TO YOUR COINBASE PRO ACCOUNT
API_KEY
API_SEC
API_PHR
```

5) Fill out the config.py in /CC with your desired Coinbase Market Pair and the Account ID for your selected Coin and Fiat

```
#FIAT BASED COIN-PAIR FROM COINBASE PRO LISTINGS (ALWAYS IN [COIN]-[FIAT] FORMAT Ex: ADA-USD)
MARKET
#THE COINBASE PRO ID FOR YOUR SELECTED COIN
COIN_ID
#THE COINBASE PRO ID FOR YOUR SELECTED FIAT
FIAT_ID
```

6) Open Git Bash Terminal in the directory of run.py and type:

```
python run.py
```

 # Configuration

```
#THE SECONDS IT TAKES THIS TOOL REFRESH
SEC_INTERVAL="60"
#THE MAX LENGTH OF THE CHART (MAX CHARTED INTERVALS)
CHART_LENGTH="60"
#THE DISTANCE BETWEEN BUY / SELL POINTS FROM YESTERDAY'S OPENING PRICE CALLED DELEGATION LEVELS
DELEGATION_LEVEL="0.05"
#THE MAX VOLUME OF COIN THAT WILL BE BOUGHT OR SOLD ON BOTH ENDS OF DELEGATION LEVELS
TRADE_VOLUME="20"
```

 # Interface Legend
 - BO = "Buy Orders"
 - SO = "Sell Orders"
 - UDL = "Upper Delegation Level"
 - YSP = "Yesterday's Starting Price"
 - LDL = "Lower Delegation Level"
 - TCP = "Today's Current Price"
 
 # Troubleshooting
 1) "ERROR [cc_engine.py:191] Caught exception: could not convert string to float: a" is recieved when you have set your shortLengh or longLength too long and the granularity too low so there is too much data for the CBPro API to return and will fail
 2) "ERROR [cc_engine.py:239] Caught exception: 'bids' ERROR [cc_mgb_beta.py:179] Caught exception: list index out of range ERROR [cc_engine.py:191] Caught exception: could not convert string to float: a" is recieved when you have set your increment_pace too short so that the multiple API calls being generated exceed the 10 per second limit and will fail
 3) A sell or buy order will not go through if the respective coin or fiat is not present to afford the transaction and will fail but will still cycle the engine and adjust the targeted prices
 
 # Future Features
 1) Email and text notification of configured events
 2) Capture and analysis of sources to derive and integrate fundemental indicators
 
 # Credits
 shout out to the cbpro SDK made by https://github.com/danpaquin from https://github.com/danpaquin/coinbasepro-python/blob/master/cbpro/public_client.py
