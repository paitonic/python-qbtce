# BTC-E API

import urllib
import httplib
import json
import datetime
import time
import hashlib
import hmac
import sys


def curr_date():
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
                print "{0}: {1} --> connection problems . retry in {2} seconds.".format(curr_date(), f.__name__, seconds_to_retry)
                time.sleep(seconds_to_retry)
        # return None
    return retry


class API:
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

        self.trade_api_resource = "/tapi"
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
            print "{0} {1} : JSON parsing failed.\n".format(curr_date(), request_url)
            sys.exit(1)

        return api_json

    def trade_api(self, method, post_params={}):
        """
        """

        # add required parameters
        post_params['nonce'] = self.__get_nonce()
        post_params['method'] = method

        # sign parameters with HMAC-SHA-512
        encoded_params = urllib.urlencode(post_params)
        sha512_hash = hmac.new(self.BTCE_API_SECRET, digestmod=hashlib.sha512)
        sha512_hash.update(encoded_params)
        sign = sha512_hash.hexdigest()

        # setting headers
        headers = {"Content-type": "application/x-www-form-urlencoded", "Key": self.BTCE_API_KEY, "Sign": sign}

        # connection
        conn = httplib.HTTPSConnection("btc-e.com")
        connection = retry_connection(conn.request)
        connection("POST", self.trade_api_resource, encoded_params, headers)

        # receiving response
        response = conn.getresponse()

        # if response code is different than 200, print it
        if response.status != 200:
            print "{0}: response status: {1} reason: {2}".format(curr_date(), response.status, response.reason)

        # try to parse the response, on failure -- exit.
        try:
            parsed_response = json.load(response)
        except:
            print "{0} {1} : JSON parsing failed.\n".format(curr_date(), response)
            sys.exit(1)
        finally:
            conn.close()

        # api returned error
        if 'error' in parsed_response:
            print "{date}: {error}".format(date=curr_date(), error=parsed_response)
            return None
        else:
            return parsed_response['return']

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
    def get_account_info(self):
        """
        """
        return self.trade_api('getInfo')

    def transfer_history(self, *args, **kwargs):
        """
        """
        return self.trade_api('TransHistory', kwargs)

    def trade_history(self, *args, **kwargs):
        """
        """
        return self.trade_api('TradeHistory', kwargs)

    def active_orders(self, *args, **kwargs):
        """
        """
        return self.trade_api('ActiveOrders', kwargs)

    def trade(self, *args, **kwargs):
        """
        """
        return self.trade_api('Trade', kwargs)

    def cancel_order(self, *args, **kwargs):
        """
        """
        return self.trade_api('CancelOrder', kwargs)

    def order_info(self, *args, **kwargs):
        """
        """
        return self.trade_api('OrderInfo', kwargs)
