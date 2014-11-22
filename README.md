python-qbtce
============

```qbtce``` is a tool for interacting with the btc-e.com API, with this tool you can get ticker, depth, create orders, cancel order and more.

##### Usage
Let's create an object to work with the API.
```python
import qbtce
api = qbtce.API()
```
```qbtce.API()``` also accepts ```key``` and ```secret``` parameters which is required for trading, however, for accessing public methods like ticker, depth, etc, those 
parameters can be skipped.


##### Ticker
```python
	api.ticker("ltc_usd")
```

```json
	{u'ltc_usd': {u'avg': 3.508,
	  u'buy': 3.529999,
	  u'high': 3.6,
	  u'last': 3.53,
	  u'low': 3.416,
	  u'sell': 3.5171,
	  u'updated': 1416668112,
	  u'vol': 135779.64027,
	  u'vol_cur': 38658.10338}}
```
##### Ticker for multiple currencies
```python
api.ticker("ltc_usd", "btc_usd")
```

```json
{u'btc_usd': {u'avg': 353.804995,
  u'buy': 352.7,
  u'high': 362.603,
  u'last': 352.7,
  u'low': 345.00699,
  u'sell': 352.522,
  u'updated': 1416668214,
  u'vol': 2104478.11369,
  u'vol_cur': 5950.96141},
 u'ltc_usd': {u'avg': 3.508,
  u'buy': 3.537062,
  u'high': 3.6,
  u'last': 3.53706,
  u'low': 3.416,
  u'sell': 3.5171,
  u'updated': 1416668214,
  u'vol': 135707.07088,
  u'vol_cur': 38637.47309}}
```

##### Depth with an optional limit parameter
```python
api.depth("btc_usd", limit=5)
```

```json
{u'btc_usd': {u'asks': [[351.86, 1.60132646],
   [352.5, 1.2066],
   [352.69, 0.01],
   [352.701, 0.14266935],
   [352.807, 0.011]],
  u'bids': [[351.641, 0.021],
   [351.64, 0.021],
   [351.601, 0.07],
   [351.6, 1.5],
   [351.503, 0.01141469]]}}
```


For trading, you have to create key and a secret in your btc-e account.
Then, just create an object with key and a secret.

##### Using trading api
```python
	import qbtce
	api = qbtce.API(key="...", secret="...")
```

##### Sell 1 NMC @ 0.85
```python
api.trade(pair="nmc_usd", type="sell", rate=0.85, amount=1)
```

```json
{u'funds': {u'btc': 0,
  u'cnh': 0,
  u'eur': 0,
  u'ftc': 0,
  u'gbp': 0,
  u'ltc': 0,
  u'nmc': 0,
  u'nvc': 0,
  u'ppc': 0,
  u'rur': 0,
  u'trc': 0,
  u'usd': 0.86726519,
  u'xpm': 0},
 u'order_id': 0,
 u'received': 1,
 u'remains': 0}
```

##### Active orders
```python
	api.active_orders()
```

```json
	{u'461587001': {u'amount': 1.0,
	  u'pair': u'nmc_usd',
	  u'rate': 0.88,
	  u'status': 0,
	  u'timestamp_created': 1416666122,
	  u'type': u'sell'}}
```

##### Order information
```python
api.order_info(order_id=461587001)
```

```json
{u'461587001': {u'amount': 1.0,
  u'pair': u'nmc_usd',
  u'rate': 0.88,
  u'start_amount': 1.0,
  u'status': 0,
  u'timestamp_created': 1416666122,
  u'type': u'sell'}}
```

##### Account information
```python
	api.get_account_info()
```

```json
{u'funds': {u'btc': 0,
  u'cnh': 0,
  u'eur': 0,
  u'ftc': 0,
  u'gbp': 0,
  u'ltc': 0,
  u'nmc': 0,
  u'nvc': 0,
  u'ppc': 0,
  u'rur': 0,
  u'trc': 0,
  u'usd': 0.86726519,
  u'xpm': 0},
 u'open_orders': 1,
 u'rights': {u'info': 1, u'trade': 1, u'withdraw': 0},
 u'server_time': 1416666392,
 u'transaction_count': 0}
```

##### Cancel order
```python
api.cancel_order(order_id=461587001)
```

```json
	{u'funds': {u'btc': 0.15926435,
	  u'cnh': 0,
	  u'eur': 0,
	  u'ftc': 0,
	  u'gbp': 0,
	  u'ltc': 28.22469696,
	  u'nmc': 11.10283754,
	  u'nvc': 0,
	  u'ppc': 0,
	  u'rur': 0,
	  u'trc': 0,
	  u'usd': 0.86726519,
	  u'xpm': 0},
	 u'order_id': 461587001}
```