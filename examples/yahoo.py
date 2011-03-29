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

    def on_chanmsg(self, emitter, user=None, channel=None, message=None):
        log.debug("Yahoo search bot got a channel message")
        log.debug("user=%s, channel=%s, message=%s", user, channel, message)
        match = re.match(
            r'^(?:([^\s]+)(?:[\s]+))?(?:answer me)(?:[\s]+)(.*)$',
            message.strip()
        )
        if match:
            addressing_me = match.group(1).rstrip(':')
            if addressing_me != self.nickname:
                return

            log.debug("Yahoo search bot got a search string: %r", match.group(0))

            answer = self.fetch_result(match.group(2))
            if answer:
                self.notice(channel, "%s: %s" % (user.nick, answer))
            else:
                self.notice(channel, "%s: Yahoo answers cannot answer %r" % (
                    user.nick, match.group(1)
                ))
                self.notice(
                    channel, "%s: Try \"Does napping make you smarter?\"" %
                    user.nick
                )

    def on_privmsg(self, emitter, user=None, channel=None, message=None):
        log.debug("Yahoo search bot got a private message")
        log.debug("user=%s, channel=%s, message=%s", user, channel, message)
        match = re.match(r'^(?:answer me)(?:[\s]+)(.*)$', message.strip())
        if match:
            log.debug("Yahoo search bot got a search string: %r",
                      match.group(0))
            answer = self.fetch_result(match.group(1))
            if answer:
                self.msg(user.nick, "Answer: %s" % answer)
            else:
                self.msg(user.nick, "Yahoo answers cannot answer %r" %
                         match.group(1))
                self.msg(user.nick, "Try: \"Does napping make you smarter?\"")
        else:
            self.msg(user.nick, "Can't understand your command: \"%s\"" %
                     message)


if __name__ == '__main__':
    from girclib.helpers import setup_logging
    setup_logging(level=5)
    client = YahooAnswerBot('irc.freenode.net', 6667, 'girclib', 'gIRClib')

    # Just for the fun, start telnet backdoor on port 2000
    from gevent.backdoor import BackdoorServer
    server = BackdoorServer(('127.0.0.1', 2000), locals=locals())
    server.start()

    @signals.on_signed_on.connect
    def _on_motd(emitter):
        log.info("Signed on. Let's join #ufs")
        client.join("#ufs")

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

