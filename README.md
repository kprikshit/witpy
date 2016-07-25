# witpy
A python library for [Wit.ai](http://wit.ai).

## Reason behind creating this
I was tired of bugs and incorrect and missing documentation of the official Wit.ai python library.
Hence, I decided to sit through one night and understand the code and working of Wit and build a library which could 
handle everything thown at it. 

This is the product of a long night, some red bulls and some number of coffees. Enjoy!!!

## Usage
On their way

## Version
The API version for this library is `20160516`. Support for rest is on the way!

# Overview
`witpy` provides a WitPy class with the following methods:
* `message` - the Wit [message API](https://wit.ai/docs/http/20160330#get-intent-via-text-link)
* `converse` - the low-level Wit [converse API](https://wit.ai/docs/http/20160330#converse-link)
* `run_actions` - a higher-level method to the Wit converse API
* `interactive` - starts an interactive conversation with your bot


### WitPy class

The Wit constructor takes the following parameters:
* `access_token` - the access token of your Wit instance
* `actions` -  the dictionary with your actions

### WitPy Function

Every function that you right will have only one argument named request.
This is a dictionary and a general structure of a request object is as following:

``` python
request = {
	'session_id': session_id,
	'context': dict(context),
	'text': message,
	'entities': response_json.get('entities'),
}
```

Every action/function should return a dict. This dictionary is the context that will be 
passed to the Wit application



### Logging

Default logging is to `STDOUT` with `INFO` level.

You can set your logging level as follows:
``` python
from witpy import WitPy
import logging


def custom_say(request):
	print request.get('Message', 'No Message Returned')


def custom_merge(request):
	received_ctx = request.get('context', {})
	received_ctx['some_entity'] = request.get('entities', {})
											.get('some_entity', 0.0)
	return received_ctx


def get_all_challenge_type(request):
	ctx = request.get('context', {})
	challenge_types = ['mathematics', 'algorithms', 'machine-learning']
	ctx['types'] =  challenge_types
	return ctx


token = '<your wit application token>'
actions = {
	'say': say,
	'merge': custom_merge,
	'get_all_challenge_types': get_all_challenge_types,
}

wc = WitPy(token, actions)
wc.logger.setLevel(logging.WARNING)
```

You can also specify a custom logger object in the Wit constructor:
``` python
from witpy import WitPy
wc = WitPy(access_token=access_token, actions=actions, logger=custom_logger)
```

### Important
I am not gonna lie or hide the fact that this is a fork of `https://github.com/wit-ai/pywit.git`. 
However, this library is better than the one provided in handling a lot of cases 
