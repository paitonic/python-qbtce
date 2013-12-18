# BTC-E API
# DOCUMENTATION: https://btc-e.com/api/documentation

# TODO:
# - add exceptions
# - license

import urllib
import httplib
import json
import datetime
import time
import hashlib
import hmac
import sys

def t():
    """Returns current date.
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def retry_connection(f):
    """Decorator. Recconect on failure.
    """
    def retry(*args, **kwargs):
        seconds_to_retry = 5
        success = False
        while (success == False):
            try:
                result = f(*args, **kwargs)
                success = True
                return result
            except:
                print "{0}: {1} --> connection problems . retry in {2} seconds.".format(t(), f.__name__, seconds_to_retry)
                time.sleep(seconds_to_retry)
        # return None
    return retry

class Q:
    """BTC-E API class.
    Methods:
    __init__()      -- constructor. initialize class properties.
    __save_nonce()  -- save last nonce value to file.
    __incr_nonce()  -- increment nonce value.
    __load_nonce()  -- load last nonce value from file.
    public_query()  -- make public (non-auth required) API request.
    trade_query()   -- make trade (auth-required) API request.
    fee()           -- return pair fee.
    ticker()        -- return pair ticker.
    trades()        -- return pair trades.
    depth()         -- return pair depth.
    getInfo()       -- return information about account.
    TransHistory()  -- return transfer history.
    TradeHistory()  -- return trade history.
    ActiveOrders()  -- return active orders.
    Trade()         -- place trade order.
    CancelOrder()   -- cancel existing order.

    Usage:
    from qbtce import Q
    q = Q(key='KEY', secret='SECRET')
    q.ticker('btc_usd') # btc/usd ticker

    """


    # set default key and secret
    __default_key = ""
    __default_secret = ""

    # TODO: set nonce_prefix to last N letters of key/secret?
    def __init__(self, key=__default_key, secret=__default_secret, nonce_prefix=''):
        """Constructor 

        Initialize properties of 'Connection' instance.
        Keyword arguments:
        Name            Type     Desc
        key             str      BTC-E key
        secret          str      BTC-E secret
        nonce_prefix    str      prefix for nonce storage file
        """

        self.public_base_url = "https://btc-e.com/api/2/"
        self.BTCE_API_KEY = key
        self.BTCE_API_SECRET = secret

        self.nonce_storage = str(nonce_prefix) + "_nonce" # storage file
        self.nonce = self.__load_nonce()

    def __save_nonce(self):
        """Saves nonce value to file.
            self.nonce_storage is the file where nonce be saved to.
        """
        try:
            f = open(self.nonce_storage, "w")
            f.write(str(self.nonce))
            f.close()
        except:
            print '{0}: failed saving nonce value.'.format(t())
        
    def __incr_nonce(self):
        """Increment the nonce value.
            Define your own algorithm if you wish.
        """
        self.nonce += 1
        self.__save_nonce()
        return self.nonce
    
    def __load_nonce(self):
        """Load nonce value from storage self.nonce_storage) and assign it to self.nonce."""
        try:
            f = open(self.nonce_storage, "r")
            nonce = int(f.read())
            return nonce
        except:
            return 1

    def __public_query(self, method_name, pair):
        """Calls public API methods: fee, ticker, trades, depth and returns response as JSON object.

        Arguments:
        Name            Type    Desc
        method_name     str     method name as described in the API
        pair            str     pair upon the method is called on, i.e. 'btc_usd'

        Returns:
        Name        Type    Desc
        api_json    JSON    response from the server
        """
        
        request_url = self.public_base_url + pair + '/' + method_name

        connection = retry_connection(urllib.urlopen)
        api_response = connection(request_url)

        # try to parse JSON
        try:
            api_json = json.load(api_response)
        except:
            print "{0}: failed parsing JSON. Possible reasons: API has been changed? Bad request? Quitting.\nrequest_url = {1}".format(t(), request_url)
            sys.exit(1)

        return api_json


    def __trade_query(self, method_name, method_params):
        """Calls the trade API methods (auth-required): getInfo, TransHistory, TradeHistory, ActiveOrders, Trade, CancelOrder
        returns response as JSON object.

        Arguments:
        Name            Type    Desc
        method_name     str     method name as described in the API
        method_params   dict    method arguments, each method have different args!

        Returns:
        Name            Type    Desc
        api_json        JSON    response from the server
        """
        params = {'nonce': self.__incr_nonce(), 'method': method_name}
        
        # if parameters supplied, add them to the existing parameters.
        if method_params != {}:
            for e in method_params.keys():
                params[e] = method_params[e]
        
        # signing parameters with HMAC-SHA-512
        params = urllib.urlencode(params)
        sha512_hash = hmac.new(self.BTCE_API_SECRET, digestmod=hashlib.sha512)
        sha512_hash.update(params)
        sign = sha512_hash.hexdigest()
        headers = {"Content-type": "application/x-www-form-urlencoded",
                       "Key":self.BTCE_API_KEY,
                       "Sign":sign}
        conn = httplib.HTTPSConnection("btc-e.com")

        connection = retry_connection(conn.request)
        connection("POST", "/tapi", params, headers)

        response = conn.getresponse()

        # if response code is different than 200, print it
        if response.status != 200:
            print "{0}: response status: {1} reason: {2}".format(t(), response.status, response.reason)
        api_json = json.load(response)
        conn.close()
        
        # bad request handling
        if 'error' in api_json and str(api_json).find('invalid nonce') != -1:
            self.__incr_nonce()
        elif 'error' in api_json: # other error
            print "{0} an error has been occured.\napi_json: {1}".format(t(), api_json)
        return api_json

    # --- basic public methods --- #
    def fee(self, pair):
        """Return fee for requested pair.
        Arguments:
        Name    Type    Desc
        pair    str     valid pair like 'btc_usd, ltc_usd etc.'

        Returns:
        Name    Type    Desc
        -       JSON    fee
        """
        return self.__public_query('fee', pair)

    def ticker(self, pair):
        """Return ticker for requested pair."""
        return self.__public_query('ticker', pair)

    def trades(self, pair):
        """Return trades for requested pair."""
        return self.__public_query('trades', pair)

    def depth(self, pair):
        """Return depth for requested pair."""
        return self.__public_query('depth', pair)

    # --- basic trade methods --- #
    def getInfo(self):
        """return information about:
        -- currenct balance
        -- API key priviliges
        -- number of transactions
        -- number of open orders
        -- server time

        no arguments.
        returns JSON object
        """
        return self.__trade_query('getInfo', {})

    def TransHistory(self, params):
        """Return history of transactions
        Arguments:
        Name    Type    Desc
        params  dict    keys: from, count, from_id, 
                        end_id, order, since, end

        returns JSON object.
        """
        return self.conn.trade_query('TransHistory', params)

    def TradeHistory(self, params):
        """Return history of orders
        Arguments:
        Name    Type    Desc
        params  dict    keys: from, count, from_id, 
                        end_id, order, since, end, pair

        returns JSON object.
        """
        return self.__trade_query('TradeHistory', params)

    def ActiveOrders(self, params):
        """Return active orders
        Arguments:
        Name    Type    Desc
        params  dict    keys: pair

        returns JSON object.
        """
        return self.__trade_query('ActiveOrders', params)

    def Trade(self, params):
        """This method places an order.
        Arguments:
        Name    Type    Desc
        params  dict    keys: pair, type, rate, amount

        returns JSON object.
        """
        return self.__trade_query('Trade', params)

    def CancelOrder(self, params):
        """Cancel order.
        Arguments:
        Name    Type    Desc
        params  dict    keys: order_id

        returns JSON object.
        """
        return self.__trade_query('CancelOrder', params)

    # --- wrappers --- #
