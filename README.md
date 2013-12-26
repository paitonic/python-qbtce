python-qbtce
============

BTC-E API - implementation of btc-e.com API (crypto-currency exchange).

## Usage examples
	# importing Q class from qbtce.py
	from qbtce import Q

	# get last trades for LTC/USD pair
	last_trades = q.trades('ltc_usd')

	# to use api methods that require auth:
	# you can set default key&secret in qbtce.py or call the constructor with key, secret arguments.
	q = Q(key='YOUR_KEY', secret='YOUR_SECRET')
	
	# now, it is possible to call all the methods that require auth.
	response = q.getInfo()



## Q class

### \_\_init\_\_(key=\_\_default\_key, secret=\_\_default\_secret, nonce\_prefix='')
Class constructor.
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>key</td><td>str</td><td>btc-e public key (optional)</td>
</tr>
<tr>
<td>secret</td><td>str</td><td>btc-e secret key (optional)</td>
</tr>
<tr>
<td>nonce_prefix</td><td>str</td><td>prefix for filename (optional)</td>
</tr>
</table>

### \_\_save\_nonce(self)
Responsible for saving nonce value to file (self.nonce_storage)

### \_\_incr\_nonce(self)
Incrementing nonce value.

### \_\_load\_nonce(self)
Loads nonce value from storage(file self.nonce_storage).

### \_\_public\_query(self, method\_name, pair)
Accepts method_name, pair and makes the actual call to btc-e. used for public methods such as: fee, ticker, trades, depth.

#### Parameters
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>method_name</td><td>str</td><td>method name as described in the API</td>
</tr>
<tr>
<td>pair</td><td>str</td><td>pair upon the method is called on, i.e. 'btc_usd'</td>
</tr>
</table>

#### Returns
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>api_json</td><td>list of json(dict)</td><td>response from the server</td>
</tr>
</table>

### \_\_trade\_query(self, method\_name, method\_params):
Calls the btc-e API methods for trading (auth-required): getInfo, TransHistory, TradeHistory, ActiveOrders, Trade, CancelOrder
returns response as list of json's.

#### Parameters
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>method_name</td><td>str</td><td>method name as described in the API</td>
</tr>
<tr>
<td>method_params</td><td>dict</td><td>method arguments, each method have different args!</td>
</tr>
</table>

#### Returns
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>api_json</td><td>list of json(dict)</td><td>response from the server</td>
</table>

### ------ btc-e API public (non-auth-required) methods ------
### fee(self, pair)
Return fee for requested pair.

#### Parameters
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>pair</td><td>str</td><td>valid pair like 'btc_usd', 'ltc_usd' etc.</td>
</table>

#### Returns
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>-</td><td>list of json</td><td>fee</td>
</table>


### ticker(self, pair)
Return ticker for requested pair.
#### Parameters
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>pair</td><td>str</td><td>valid pair like 'btc_usd', 'ltc_usd' etc.</td>
</table>
#### Returns
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>-</td><td>list of json</td><td>fee</td>
</table>

### def trades(self, pair)
Return trades for requested pair.
#### Parameters
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>pair</td><td>str</td><td>valid pair like 'btc_usd', 'ltc_usd' etc.</td>
</table>
#### Returns
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>-</td><td>list of json(dict)</td><td>fee</td>
</table>

### depth(self, pair)
Return depth for requested pair.
#### Parameters
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>pair</td><td>str</td><td>valid pair like 'btc_usd', 'ltc_usd' etc.</td>
</table>
#### Returns
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>-</td><td>list of json(dict)</td><td>fee</td>
</table>

### ------ btc-e API trade methods (auth-required) ------
### getInfo(self)
Returns following information:

* current balance
* API key priviliges
* number of transactions
* number of open orders
* server time
	
#### Parameters: None
#### Returns
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>-</td><td>list of json(dict)</td><td>various information about the account.</td>
</table>

### TransHistory(self, params)
Returns history of transactions

####  Parameters:
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>params</td><td>dict</td><td>keys: from, count, from_id, end_id, order, since, end with their values. i.e {'count': 5}</td>
</table>
#### Returns
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>-</td><td>list of json(dict)</td><td>transaction history.</td>
</table>

### TradeHistory(self, params)
Returns history of orders

####  Parameters:
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>params</td><td>dict</td><td>allowed keys: 'from', 'count', 'from_id', 
                        'end_id', 'order', 'since', 'end', 'pair'</td>
</table>
#### Returns
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>-</td><td>list of json(dict)</td><td>יhistory of orders.</td>
</table>

### ActiveOrders(self, params)
Returns active orders
#### Parameters:
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>params</td><td>dict</td><td>allowed keys: 'pair'. i.e {'pair': 'ltc_usd'}</td>
</table>
#### Returns
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>-</td><td>list of json(dict)</td><td>active orders</td>
</table>

### Trade(self, params)
Place new order.
####  Parameters:
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>params</td><td>dict</td><td>allowed keys: 'from', 'count', 'from_id', 
                        'end_id', 'order', 'since', 'end', 'pair'</td>
</table>
#### Returns
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>-</td><td>list of json(dict)</td><td>returns funds, remains, received and more.</td>
</table>

### CancelOrder(self, params)
Cancel order.
#### Parameters
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>-</td><td>list of json(dict)</td><td>returns funds, remains, received and more.</td>
</table>
#### Returns
<table>
<tr>
<th>Name</th><th>Type</th><th>Description</th>
</tr>
<tr>
<td>-</td><td>list of json(dict)</td><td>return order_id, funds.</td>
</table>