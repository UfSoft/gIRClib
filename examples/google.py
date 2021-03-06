# -*- coding: utf-8 -*-
"""
    google
    ~~~~~~

    A simple bot which does searches on google and returns their results.


    :copyright: © 2009 coleifer - https://github.com/coleifer/irc/blob/master/bots/google.py
    :copyright: © 2010 traviscline - https://github.com/traviscline/irc/blob/master/bots/google.py
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

class GoogleSearchBot(IRCClient):

    def fetch_result(self, query):
        log.debug("Querying google about %r", query)
        sock = httplib2.Http(timeout=1)
        headers, response = sock.request(
            'http://ajax.googleapis.com/ajax/services/search/web?v=2.0&q=%s' % \
            urllib.quote(query)
        )
        if headers['status'] in (200, '200'):
            response = json.loads(response)
            return [
                e['unescapedUrl'] for e in response['responseData']['results']
            ]

    def on_privmsg(self, emitter, user=None, message=None):
        log.debug("Google search bot got a private message")
        log.debug("user=%s, message=%s", user, message)
        match = re.match(r'^(?:find me)(?:[\s]+)(.*)$', message.strip())
        if match:
            log.debug("Google search bot got a search string: %r",
                      match.group(0))
            results = self.fetch_result(match.group(1))
            if results:
                self.msg(user.nick, "Search results: %s" % ', '.join(results))
            else:
                self.msg(user.nick, "No results for %r" % match.group(1))
        else:
            self.msg(user.nick, "Can't understand your command: \"%s\"" % message)

    def on_chanmsg(self, emitter, channel=None, user=None, message=None):
        log.debug("Google search bot got a channel message")
        log.debug("channel=%s, message=%s", channel, message)
        match = re.match(r'^(?:([^\s]+)(?:[\s]+))?(?:find me(?:[\:])?)(?:[\s]+)(.*)$',
                         message.strip())
        if match:
            addressing_me = match.group(1).rstrip(':')
            if addressing_me != self.nickname:
                return

            log.debug("Google search bot got a search string: %r",
                      match.group(0))
            results = self.fetch_result(match.group(2))
            if results:
                self.notice(channel, "%s: Search results: %s" % (
                    user.nick, ', '.join(results),
                ))
            else:
                self.notice(channel, "%: No results for %r" % (
                    user.nick, match.group(1)
                ))
        else:
            self.notice(channel,
                        "Can't understand your command: \"%s\"" % message)


if __name__ == '__main__':
    from girclib.helpers import setup_logging
    setup_logging(level=5)
    client = GoogleSearchBot('irc.freenode.net', 6667, 'girclib', 'gIRClib')

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
