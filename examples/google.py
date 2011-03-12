# -*- coding: utf-8 -*-
"""
    google
    ~~~~~~

    A simple bot which does searches on google and returns their results.


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

    def on_privmsg(self, emitter, user=None, channel=None, message=None):
        log.debug("Google search bot got a message")
        match = re.match(r'^(?:[^\s]+)(?:[\s]+)(?:find me)(?:[\s]+)(.*)$',
                         message.strip())
        if match:
            log.debug("Google search bot got a search string: %r",
                      match.group(0))
            results = self.fetch_result(match.group(1))
            if channel:
                user = channel
            if results:
                self.notice(user, "Search results: %s" % ', '.join(results))
            else:
                self.notice(user, "No results for %r" % match.group(1))


if __name__ == '__main__':
#    import logging
    from girclib.helpers import setup_logging
    format='%(asctime)s [%(lineno)-4s] %(levelname)-7.7s: %(message)s'
    setup_logging(format, 5)
    client = GoogleSearchBot('irc.freenode.net', 6667, 'girclib', 'gIRClib')
#    log = logging.getLogger('gIRClib')

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
        log.info("Exited!?\n\n")
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
