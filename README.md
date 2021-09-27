<div align="center">
  <h1>Crypto Commando Trader</h1>
  <p>Automated python based cryptographic trading engine built using hard coded rulesets based on conceptualized and customized delegation levels commissioned through CoinBase Pro API Platform by Tim Kovacic using CBPro SDK by DanPaguin</p><br>
  <img width="560" height="456" src="https://static.wixstatic.com/media/c11e26_98214627f32540f7939870093be0a03b~mv2.png/v1/fill/w_560,h_456,al_c,q_85,usm_0.66_1.00_0.01/vectorstock_19626918_edited.webp">
</div>
<br>

# Prerequisites
1) Download and Install Git Bash Terminal (https://gitforwindows.org/)
2) Download and Install Python (https://www.python.org/downloads/)
3) Open Git Bash Terminal and Execute:

```
  pip install cbpro
  pip install numpy
  pip install matplotlib
```

4) Fill out the config.py in /CC with your Coinbase Pro API token information (KEY, SEC, and PHR)

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
