# -*- coding: utf-8 -*-
"""
    girclib.client
    ~~~~~~~~~~~~~~~~


    :copyright: © 2011 UfSoft.org - :email:`Pedro Algarvio (pedro@algarvio.me)`
    :license: BSD, see LICENSE for more details.
"""

import socket
import gevent
import girclib
import logging
from girclib import signals
from girclib.helpers import parse_raw_irc_command
from girclib.irc import BaseIRCClient, ServerSupportedFeatures, IRCUser

log = logging.getLogger(__name__)

class IRCClient(BaseIRCClient):
    source_url   = girclib.__url__
    version_name = girclib.__package_name__
    version_num  = girclib.__version__
    version_env  = 'Linux'
    userinfo     = None
    erroneous_nick_fallback = "%s-Client" % girclib.__package_name__

    def __init__(self, host="", port=6667, nickname="girclib", username=None,
                 realname="gIRClib", password=None, encoding="utf-8"):
        self.host = host
        self.port = port
        self.nickname = nickname
        self.username = username
        self.realname = realname
        self.password = password
        self.connect_signals()

    def connect(self):
        BaseIRCClient.connect(self, self.host, self.port, use_ssl=False)

    def connect_signals(self):
        signals.on_connected.connect(self.on_connected, sender=self)
        signals.on_ctcp_query_finger.connect(self.on_ctcp_query_finger, sender=self)
        signals.on_rpl_topic.connect(self.on_rpl_topic, sender=self)
        signals.on_rpl_created.connect(self.on_rpl_created, sender=self)
        signals.on_rpl_yourhost.connect(self.on_rpl_yourhost, sender=self)
        signals.on_rpl_myinfo.connect(self.on_rpl_myinfo, sender=self)
        signals.on_rpl_bounce.connect(self.on_rpl_bounce, sender=self)
        signals.on_rpl_isupport.connect(self.on_rpl_isupport, sender=self)
        signals.on_rpl_luserclient.connect(self.on_rpl_luserclient, sender=self)
        signals.on_rpl_luserop.connect(self.on_rpl_luserop, sender=self)
        signals.on_rpl_luserchannels.connect(self.on_rpl_luserchannels, sender=self)
        signals.on_rpl_luserme.connect(self.on_rpl_luserme, sender=self)
        signals.on_motd.connect(self.on_motd, sender=self)
        signals.on_nickname_in_use.connect(self.on_nickname_in_use, sender=self)
        signals.on_erroneous_nickname.connect(self.on_erroneous_nickname, sender=self)
        signals.on_password_mismatch.connect(self.on_password_mismatch, sender=self)
        signals.on_signed_on.connect(self.on_signed_on, sender=self)
        signals.on_joined.connect(self.on_joined, sender=self)
        signals.on_user_joined.connect(self.on_user_joined, sender=self)
        signals.on_left.connect(self.on_left, sender=self)
        signals.on_user_left.connect(self.on_user_left, sender=self)
        signals.on_user_quit.connect(self.on_user_quit, sender=self)
        signals.on_mode_changed.connect(self.on_mode_changed, sender=self)
        signals.on_chanmsg.connect(self.on_chanmsg, sender=self)
        signals.on_privmsg.connect(self.on_privmsg, sender=self)
        signals.on_notice.connect(self.on_notice, sender=self)
        signals.on_nick_changed.connect(self.on_nick_changed, sender=self)
        signals.on_user_renamed.connect(self.on_user_renamed, sender=self)
        signals.on_kicked.connect(self.on_kicked, sender=self)
        signals.on_user_kicked.connect(self.on_user_kicked, sender=self)
        signals.on_topic_changed.connect(self.on_topic_changed, sender=self)
        signals.on_banned.connect(self.on_banned, sender=self)
        signals.on_user_banned.connect(self.on_user_banned, sender=self)

    def on_connected(self, emitter):
        log.debug("Connected to %s:%s", self.network_host, self.network_port)
        self.register(self.nickname, hostname=socket.gethostname(),
                      servername=socket.gethostname())

    def on_ctcp_query_finger(self, emitter, user=None, channel=None, data=None):
        """
        In case you implement a finger reply, a response should be made like::

            emitter.ctcp_make_reply(nick_from_netmask(user), [('FINGER', reply)])


        See :meth:`~girclib.signals.on_ctcp_query_finger`.

        """

    def on_rpl_topic(self, emitter, user=None, channel=None, new_topic=None):
        """
        See :meth:`~girclib.signals.on_rpl_topic`.
        """

    def on_rpl_notopic(self, emitter, user=None, channel=None):
        """
        See :meth:`~girclib.signals.on_rpl_notopic`.
        """

    def on_rpl_created(self, emitter, when=None):
        """
        See :meth:`~girclib.signals.on_rpl_created`.
        """

    def on_rpl_yourhost(self, emitter, info=None):
        """
        See :meth:`~girclib.signals.on_rpl_yourhost`.
        """

    def on_rpl_myinfo(self, emitter, servername=None, version=None, umodes=None,
                      cmodes=None):
        """
        See :meth:`~girclib.signals.on_rpl_myinfo`.
        """

    def on_rpl_bounce(self, emitter, info=None):
        """
        See :meth:`~girclib.signals.on_rpl_bounce`.
        """

    def on_rpl_isupport(self, emitter, options=None):
        """
        See :meth:`~girclib.signals.on_rpl_isupport`.
        """

    def on_rpl_luserclient(self, emitter, info=None):
        """
        See :meth:`~girclib.signals.on_rpl_luserclient`.
        """

    def on_rpl_luserop(self, emitter, ops=None):
        """
        See :meth:`~girclib.signals.on_rpl_luserop`.
        """

    def on_rpl_luserchannels(self, emitter, channels=None):
        """
        See :meth:`~girclib.signals.on_rpl_luserchannels`.
        """

    def on_rpl_luserme(self, emitter, info=None):
        """
        See :meth:`~girclib.signals.on_rpl_luserme`.
        """

    def on_signed_on(self, emitter):
        """
        Here you can join channels for example

        See :meth:`~girclib.signals.on_signed_on`.
        """

    def on_motd(self, emitter, motd=None):
        """
        See :meth:`~girclib.signals.on_motd`.
        """

    def on_nickname_in_use(self, emitter, nickname=None):
        """
        See :meth:`~girclib.signals.on_nickname_in_use`.
        """
        emitter.set_nick("_%s" % nickname)

    def on_erroneous_nickname(self, emitter, nickname=None):
        """
        See :meth:`~girclib.signals.on_erroneous_nickname`.
        """
        emitter.set_nick(self.erroneous_nick_fallback)

    def on_password_mismatch(self, emitter):
        """
        See :meth:`~girclib.signals.on_password_mismatch`.
        """

    def on_joined(self, emitter, channel=None):
        """
        See :meth:`~girclib.signals.on_joined`.
        """

    def on_user_joined(self, emitter, channel=None, user=None):
        """
        See :meth:`~girclib.signals.on_user_joined`.
        """

    def on_left(self, emitter, channel=None):
        """
        See :meth:`~girclib.signals.on_left`.
        """

    def on_user_left(self, emitter, channel=None, user=None):
        """
        See :meth:`~girclib.signals.on_user_left`.
        """

    def on_user_quit(self, emitter, user=None, message=None):
        """
        See :meth:`~girclib.signals.on_user_quit`.
        """

    def on_mode_changed(self, emitter, user=None, channel=None, set=None,
                        modes=None, args=None):
        """
        See :meth:`~girclib.signals.on_mode_changed`.
        """

    def on_chanmsg(self, emitter, channel=None, user=None, message=None):
        """
        See :meth:`~girclib.signals.on_chanmsg`.
        """

    def on_privmsg(self, emitter, user=None, message=None):
        """
        See :meth:`~girclib.signals.on_privmsg`.
        """

    def on_notice(self, emitter, user=None, channel=None, message=None):
        """
        See :meth:`~girclib.signals.on_notice`.
        """

    def on_nick_changed(self, emitter, user=None, newnick=None):
        """
        See :meth:`~girclib.signals.on_nick_changed`.
        """

    def on_user_renamed(self, emitter, user=None, newnick=None):
        """
        See :meth:`~girclib.signals.on_user_renamed`.
        """

    def on_kicked(self, emitter, channel=None, kicker=None, message=None):
        """
        See :meth:`~girclib.signals.on_kicked`.
        """


    def on_user_kicked(self, emitter, channel=None, kicked=None, kicker=None,
                       message=None):
        """
        See :meth:`~girclib.signals.on_user_kicked`.
        """

    def on_banned(self, emitter, channel=None, message=None):
        """
        See :meth:`~girclib.signals.on_banned`.
        """

    def on_user_banned(self, emitter, channel=None, user=None, message=None):
        """
        See :meth:`~girclib.signals.on_user_banned`.
        """

    def on_topic_changed(self, emitter, user=None, channel=None, new_topic=None):
        """
        See :meth:`~girclib.signals.on_topic_changed`.
        """


if __name__ == '__main__':
    from girclib.helpers import setup_logging
    format='%(asctime)s [%(lineno)-4s] %(levelname)-7.7s: %(message)s'
    setup_logging(format, 5)
    client = IRCClient('irc.freenode.net', 6667, 'girclib', 'gIRClib')
#    log = logging.getLogger('gIRClib')

    # Just for the fun, start telnet backdoor on port 2000
    from gevent.backdoor import BackdoorServer
    server = BackdoorServer(('127.0.0.1', 2000), locals=locals())
    server.start()

    nicks = []

    @signals.on_rpl_namreply.connect
    def on_rpl_namreply(emitter, users=None, channel=None, privacy=None):
        if users:
            nicks.extend(users)


    @signals.on_rpl_endofnames.connect
    def on_rpl_endofnames(emitter, channel=None):
        gevent.sleep(2)
        for nick in nicks:
            if nick == "girclib":
                continue
            client.ping(nick)


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
