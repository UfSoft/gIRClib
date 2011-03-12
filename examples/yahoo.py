# -*- coding: utf-8 -*-
"""
    yahoo
    ~~~~~

    A simple bot which does searches on yahoo answers and returns their results.


    :copyright: © 2009 coleifer - https://github.com/coleifer/irc/blob/master/bots/google.py
    :copyright: © 2011 UfSoft.org - :email:`Pedro Algarvio (pedro@algarvio.me)`
    :license: BSD, see LICENSE for more details.
"""

import re
import json
import gevent
import urllib
import logging
import httplib2
from gevent import monkey
from girclib import signals
from girclib.client import IRCClient
from girclib.helpers import nick_from_netmask

log = logging.getLogger(__name__)

class YahooAnswerBot(IRCClient):

    def fetch_result(self, query):
        log.debug("Querying yahoo answers about %r", query)
        sock = httplib2.Http(timeout=1)
        headers, response = sock.request(
            'http://answers.yahooapis.com/AnswersService/V1/questionSearch?' +
            'appid=YahooDemo&query=%s&output=json' % urllib.quote(query)
        )
        if headers['status'] in (200, '200'):
            response = json.loads(response)
            if len(response['all']['questions']):
                question_id = response['all']['questions'][0]['Id']
                headers, response = sock.request(
                    'http://answers.yahooapis.com/AnswersService/V1/' +
                    'getQuestion?appid=YahooDemo&question_id=%s&output=json' \
                    % urllib.quote(question_id)
                )
                response = json.loads(response)
                if headers['status'] in (200, '200'):
                    chosen = response['all']['question'][0]['ChosenAnswer']
                    return chosen.encode('utf-8', 'replace')

    def on_privmsg(self, emitter, user=None, channel=None, message=None):
        log.debug("Yahoo search bot got a message")
        log.debug("user=%s, channel=%s, message=%s", user, channel, message)
        match = re.match(
            r'^(?:(?:[^\s]+)(?:[\s]+))?(?:answer me)(?:[\s]+)(.*)$',
            message.strip()
        )
        if match:
            log.debug("Yahoo search bot got a search string: %r",
                      match.group(0))
            answer = self.fetch_result(match.group(1))
            if channel != self.nickname:
                user = channel
                say = self.notice
            else:
                say = self.msg
                user = nick_from_netmask(user)
            if answer:
                say(user, "Answer: %s" % answer)
            else:
                say(user, "Yahoo answers cannot answer %r" % match.group(1))
                say(user, "Try: \"Does napping make you smarter?\"")


if __name__ == '__main__':
    from girclib.helpers import setup_logging
    format='%(asctime)s [%(lineno)-4s] %(levelname)-7.7s: %(message)s'
    setup_logging(format, 5)
    client = YahooAnswerBot('irc.freenode.net', 6667, 'girclib', 'gIRClib')

    # Just for the fun, start telnet backdoor on port 2000
    from gevent.backdoor import BackdoorServer
    server = BackdoorServer(('127.0.0.1', 2000), locals=locals())
    server.start()

    @signals.on_signed_on.connect
    def _on_motd(emitter):
        log.info("Signed on. Let's join #ufs")
        client.join("ufs")

    @signals.on_disconnected.connect
    def disconnected(emitter):
        log.info("Exited!?")
        try:
            gevent.shutdown()
        except AssertionError:
            # Shutting down is only possible from MAIN greenlet
            pass

    client.connect()

    try:
        while True:
            gevent.sleep(10)
    except KeyboardInterrupt:
        client.disconnect()

