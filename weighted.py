import numpy as np
#import pandas
#import scikit.learn
#import sciPy

MAX_LOOKBACK = 2520

def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
  nLookback = CLOSE.shape[0]
  nMarkets = CLOSE.shape[1]

  r = 0.6 # discount rate

  p = range(nLookback)
  b = np.nansum(np.multiply(np.power(r, p)[:, np.newaxis], CLOSE[-1] - CLOSE[-nLookback:]), axis = 0)

  longEquity = np.array(b > 0)
  shortEquity = ~longEquity

  pos = np.zeros((1, nMarkets))
  pos[0, longEquity] = 1
  pos[0, shortEquity] = -1

  weights = pos / np.nansum(abs(pos))

  return weights, settings

def mySettings():
  settings={}

  # S&P 100 stocks
  settings['markets'] = ['CASH','AAPL','ABBV','ABT','ACN','AEP','AIG','ALL', \
  'AMGN','AMZN','APA','APC','AXP','BA','BAC','BAX','BK','BMY','BRKB','C', \
  'CAT','CL','CMCSA','COF','COP','COST','CSCO','CVS','CVX','DD','DIS','DOW', \
  'DVN','EBAY','EMC','EMR','EXC','F','FB','FCX','FDX','FOXA','GD','GE', \
  'GILD','GM','GOOGL','GS','HAL','HD','HON','HPQ','IBM','INTC','JNJ','JPM', \
  'KO','LLY','LMT','LOW','MA','MCD','MDLZ','MDT','MET','MMM','MO','MON', \
  'MRK','MS','MSFT','NKE','NOV','NSC','ORCL','OXY','PEP','PFE','PG','PM', \
  'QCOM','RTN','SBUX','SLB','SO','SPG','T','TGT','TWX','TXN','UNH','UNP', \
  'UPS','USB','UTX','V','VZ','WAG','WFC','WMT','XOM']

  # Futures Contracts
  # settings['markets']  = ['CASH','F_AD', 'F_BO', 'F_BP', 'F_C', 'F_CD',  \
  # 'F_CL', 'F_DJ', 'F_EC', 'F_ES', 'F_FV', 'F_GC', 'F_HG', 'F_HO', 'F_LC', \
  # 'F_LN', 'F_NG', 'F_NQ', 'F_RB', 'F_S', 'F_SF', 'F_SI', 'F_SM', 'F_SP', \
  # 'F_TY', 'F_US', 'F_W', 'F_YM']

  settings['lookback'] = MAX_LOOKBACK # 504
  settings['budget'] = 10**6
  settings['slippage'] = 0.05


  return settings
