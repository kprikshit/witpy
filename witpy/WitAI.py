import requests
import os
import uuid
import sys
import logging
import json
import urllib

from chatbot_functions import *

WIT_API_HOST = os.getenv('WIT_URL', 'https://api.wit.ai')
WIT_API_VERSION = os.getenv('WIT_API_VERSION', '20160516')
DEFAULT_MAX_STEPS = 10
INTERACTIVE_PROMPT = '> '

WIT_RESPONSE_TYPES = ['error', 'msg', 'merge', 'stop', 'action']


class WitsyError(Exception):
    pass


def req(logger, access_token, method, path, params, **kwargs):
    """
    Make request to Wit AI Servers
    :param logger:
    :param access_token:
    :param method:
    :param path:
    :param params:
    :param kwargs:
    :return:
    """
    full_url = WIT_API_HOST + path
    logger.debug('Making request: %s %s %s', method, full_url, params)
    rsp = requests.post(
        full_url,
        headers={
            'authorization': 'Bearer ' + access_token,
            'accept': 'application/json',
            'content-type': 'application/json',
        },
        params=params, 
        **kwargs
    )
    if rsp.status_code > 200:
        logger.error('Wit responded with status: ' + str(rsp.status_code) + ' (' + rsp.reason + ')')
        raise WitsyError('Wit responded with status: ' + str(rsp.status_code) + ' (' + rsp.reason + ')')

    r_json = rsp.json()
    if 'error' in r_json:
        logger.error('Wit responded with an error: ' + r_json['error'])
        raise WitsyError('Wit responded with an error: ' + r_json['error'])

    logger.debug('Request Response %s %s %s', method, full_url, r_json)
    logger.debug(r_json)
    return r_json


def validate_actions(logger, actions_dict):

    if not isinstance(actions_dict, dict):
        logger.warn('The second parameter should be a dictionary.')

    # Some functions that must be there
    for action in ['merge', 'say']:
        if action not in actions_dict:
            logger.warn('The \'' + action + '\' action is missing. ')

    for action in actions_dict.keys():
        if not hasattr(actions_dict[action], '__call__'):
            logger.warn('The \'' + action + '\' action should be a function.')
    return actions_dict


class WitAI:

    actions = {}
    access_token = None

    def __init__(self, access_token, actions=None, logger=None):
        self.access_token = access_token
        self.logger = logger or logging.getLogger(__name__)
        if actions:
            self.actions = validate_actions(self.logger, actions)

    def message(self, msg, verbose=None):
        params = {}
        if verbose:
            params['verbose'] = True
        if msg:
            params['q'] = msg
        resp = req(self.logger, self.access_token, 'GET', '/message', params)
        return resp

    def converse(self, session_id, message, context=None, verbose=None):
        if context is None:
            context = {}
        params = {'session_id': session_id}
        if verbose:
            params['verbose'] = True
        if message:
            params['q'] = message
        resp = req(self.logger, self.access_token, 'POST', '/converse', params, json=context)
        return resp

    def __run_actions(self, session_id, message, context, i, verbose):
        if i <= 0:
            print ('Max steps reached, stopping.')
            return context
        response_json = self.converse(session_id, message, context, verbose)

        if 'type' not in response_json:
            print ('Couldn\'t find type in Wit response')
            return context

        response_type = response_json['type'].lower()
        if response_type not in WIT_RESPONSE_TYPES:
            self.logger.error('Unknown response type received: %s', response_type)
            return context

        self.logger.debug('Context: %s', context)
        self.logger.debug('Response type: %s', response_type)

        if response_type == 'merge':
            response_json['type'] = 'action'
            response_json['action'] = 'merge'

        if response_type == 'error':
            self.logger.error(response_json)
            raise WitsyError('Wit returned an error. Nothing can be done')

        if response_type == 'stop':
            return context

        request = {
            'session_id': session_id,
            'context': dict(context),
            'text': message,
            'entities': response_json.get('entities'),
        }

        if response_type == 'msg':
            response = {
                'text': response_json.get('msg').encode('utf8'),
                'quickreplies': response_json.get('quickreplies'),
            }
            if self.actions.get('say', None):
                print "doing nowwwww"
                self.actions['say'](request, response)
            else:
                self.logger.info(response)
        elif response_type == 'action':
            action = response_json['action']
            if action:
                context = self.actions[action](request)
                self.logger.info("context updated to: " + str(context))
                if context is None:
                    self.logger.warn('missing context - did you forget to return it?')
                    context = {}
        return self.__run_actions(session_id, '', context, i-1, verbose)

    def run_actions(self, session_id, message, context=None, max_steps=DEFAULT_MAX_STEPS, verbose=None):
        if not self.actions:
            self.throw_must_have_actions()

        if context is None:
            context = {}
        return self.__run_actions(session_id, message, context, max_steps, verbose)

    def interactive(self, context=None, max_steps=DEFAULT_MAX_STEPS):
        if not self.actions:
            self.throw_must_have_actions()
        if max_steps <= 0:
            raise WitsyError('max iterations reached')
        if context is None:
            context = {}

        session_id = uuid.uuid1()
        while True:
            try:
                message = raw_input(INTERACTIVE_PROMPT).rstrip()
            except (KeyboardInterrupt, EOFError):
                return
            if message.lower() in ['exit', 'quit']:
                break
            context = self.run_actions(session_id, message, context, max_steps)

    def throw_if_action_missing(self, action_name):
        if action_name and action_name not in self.actions:
            raise WitsyError('unknown action: ' + str(action_name))

    def throw_must_have_actions(self):
        raise WitsyError('You must provide the `actions` parameter to be able to use runActions. ')
