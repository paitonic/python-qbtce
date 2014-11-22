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
        while (not success):
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

    """


    def __init__(self, key="", secret=""):
        """Constructor

        Initialize properties of 'Connection' instance.
        Keyword parameters:
        Name            Type     Desc
        key             str      BTC-E key
        secret          str      BTC-E secret
        """

        self.public_base_url = "https://btc-e.com/api/2/"
        self.public_api3_url = "https://btc-e.com/api/3/"
        self.BTCE_API_KEY = key
        self.BTCE_API_SECRET = secret

    def __get_nonce(self):
        """Get new nonce value.
        """
        return int(time.time())

    def public_api3(self, *args, **kwargs):
        """
        """
        method = kwargs.get('method')
        params = kwargs.get('params')

        if params:
            params = urllib.urlencode(params)

        pairs = kwargs.get('pairs', None)
        if pairs:
            pairs = '-'.join(pairs)
        
        # build the request url
        request_url = "{location}{method}/{pairs}?{params}".format(
            location=self.public_api3_url,
            method=method,
            pairs=pairs or '',
            params=params or ''
            )
        # create connection
        connection = retry_connection(urllib.urlopen)
        api_response = connection(request_url)

        # try parsing api response (json)
        try:
            api_json = json.load(api_response)
        except:
            print "{0} {1} : JSON parsing failed.\n".format(t(), request_url)
            sys.exit(1)

        return api_json

    def __trade_query(self, method_name, method_params):
        """Calls the trade API methods (auth-required): getInfo, TransHistory, TradeHistory, ActiveOrders, Trade, CancelOrder
        returns response as list of json's.

        Parameters:
        Name            Type    Desc
        method_name     str     method name as described in the API
        method_params   dict    method parameters, each method have different args!

        Returns:
        Name            Type                    Desc
        api_json        list of json(dict)    response from the server
        """
        params = {'nonce': self.__get_nonce(), 'method': method_name}

        # if parameters supplied, add them to the existing parameters.
        if method_params != {}:
            for e in method_params.keys():
                params[e] = method_params[e]

        # signing parameters with HMAC-SHA-512
        params = urllib.urlencode(params)
        sha512_hash = hmac.new(self.BTCE_API_SECRET, digestmod=hashlib.sha512)
        sha512_hash.update(params)
        sign = sha512_hash.hexdigest()
        headers = {"Content-type": "application/x-www-form-urlencoded", "Key": self.BTCE_API_KEY, "Sign": sign}
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
            self.__get_nonce()
        elif 'error' in api_json:  # other error
            print "{0} an error has been occured.\napi_json: {1}".format(t(), api_json)
        return api_json

    # --- public api v3 --- #
    def fee(self, *args, **kwargs):
        """
        """
        params = {
            'ignore_invalid': kwargs.get('ignore_invalid', 0)
        }
        return self.public_api3(method='fee', params=params, pairs=args)

    def ticker(self, *args, **kwargs):
        """
        """

        params = {
            'ignore_invalid': kwargs.get('ignore_invalid', 0)
            }
        return self.public_api3(method='ticker', params=params, pairs=args)

    def trades(self, *args, **kwargs):
        """
        """
        params = {
            'ignore_invalid': kwargs.get('ignore_invalid', 0)
            }
        return self.public_api3(method='trades', params=params, pairs=args)

    def depth(self, *args, **kwargs):
        """
        """
        params = {
            'limit': kwargs.get("limit", None),
            'ignore_invalid': kwargs.get('ignore_invalid', 0)
            }
        return self.public_api3(method='depth', params=params, pairs=args)

    def info(self):
        """
        """
        return self.public_api3(method='info')

    # --- trade methods --- #
    def getInfo(self):
        """Returns information about:
        -- current balance
        -- API key priviliges
        -- number of transactions
        -- number of open orders
        -- server time

        Parameters: None
        Returns:
        Name    Type                Desc
        -       list of json(dict)  various information about the account.
        """
        return self.__trade_query('getInfo', {})

    def TransHistory(self, params):
        """Returns history of transactions
        Parameters:
        Name    Type    Desc
        params  dict    keys: from, count, from_id,
                        end_id, order, since, end

        Returns:
        Name    Type                Desc
        -       list of json(dict)  transaction history.
        """
        return self.conn.trade_query('TransHistory', params)

    def TradeHistory(self, params):
        """Returns history of orders
        Parameters:
        Name    Type    Desc
        params  dict    allowed keys: 'from', 'count', 'from_id',
                        'end_id', 'order', 'since', 'end', 'pair'

        Returns:
        Name    Type                Desc
        -       list of json(dict)     history of orders.
        """
        return self.__trade_query('TradeHistory', params)

    def ActiveOrders(self, params):
        """Returns active orders
        Parameters:
        Name    Type    Desc
        params  dict    allowed keys: 'pair'. i.e {'pair': 'ltc_usd'}

        Returns:
        Name    Type                Desc
        -       list of json(dict)  active orders
        """
        return self.__trade_query('ActiveOrders', params)

    def Trade(self, params):
        """This method places an order.
        Parameters:
        Name    Type    Desc
        params  dict    allowed keys: 'pair', 'type', 'rate', 'amount'

        Returns:
        Name    Type                Desc
        -       list of json(dict)  returns funds, remains, received and more.
        """
        return self.__trade_query('Trade', params)

    def CancelOrder(self, params):
        """Cancel order.
        Parameters:
        Name    Type    Desc
        params  dict    keys: order_id

        Returns:
        Name    Type                Desc
        -       list of json(dict)  return order_id, funds.
        """
        return self.__trade_query('CancelOrder', params)