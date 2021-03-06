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


### Wit class

The Wit constructor takes the following parameters:
* `access_token` - the access token of your Wit instance
* `actions` -  the dictionary with your actions

### Logging

Default logging is to `STDOUT` with `INFO` level.

You can set your logging level as follows:
``` python
from witpy import WitPy
import logging
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
However, this library is much better then the one provided. 
