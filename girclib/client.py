# -*- coding: utf-8 -*-
"""
    girclib.client
    ~~~~~~~~~~~~~~~~


    :copyright: © 2011 UfSoft.org - :email:`Pedro Algarvio (pedro@algarvio.me)`
    :license: BSD, see LICENSE for more details.
"""

import gevent
import girclib
from girclib import signals
from girclib.helpers import nick_from_netmask, parse_raw_irc_command
from girclib.irc import BaseIRCClient, ServerSupportedFeatures

class IRCClient(BaseIRCClient):
    source_url   = girclib.__url__
    version_name = girclib.__package_name__
    version_num  = girclib.__version__
    version_env  = 'Linux'
    userinfo     = None
    erroneous_nick_fallback = "%s-Client" % girclib.__package_name__

    def __init__(self, host="", port=6667, nickname="girclib", username=None,
                 realname="gIRClib", password=None, encoding="utf-8"):
        BaseIRCClient.__init__(self)
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
        signals.on_connected.connect(self.on_connected)
        signals.on_ctcp_query_ping.connect(self.on_ctcp_query_ping)
        signals.on_ctcp_query_finger.connect(self.on_ctcp_query_finger)
        signals.on_ctcp_query_version.connect(self.on_ctcp_query_version)
        signals.on_ctcp_query_source.connect(self.on_ctcp_query_source)
        signals.on_ctcp_query_userinfo.connect(self.on_ctcp_query_userinfo)
        signals.on_rpl_topic.connect(self.on_rpl_topic)
        signals.on_rpl_created.connect(self.on_rpl_created)
        signals.on_rpl_yourhost.connect(self.on_rpl_yourhost)
        signals.on_rpl_myinfo.connect(self.on_rpl_myinfo)
        signals.on_rpl_bounce.connect(self.on_rpl_bounce)
        signals.on_rpl_isupport.connect(self.on_rpl_isupport)
        signals.on_rpl_luserclient.connect(self.on_rpl_luserclient)
        signals.on_rpl_luserop.connect(self.on_rpl_luserop)
        signals.on_rpl_luserchannels.connect(self.on_rpl_luserchannels)
        signals.on_rpl_luserme.connect(self.on_rpl_luserme)
        signals.on_motd.connect(self.on_motd)
        signals.on_nickname_in_use.connect(self.on_nickname_in_use)
        signals.on_erroneous_nickname.connect(self.on_erroneous_nickname)
        signals.on_password_mismatch.connect(self.on_password_mismatch)
        signals.on_signed_on.connect(self.on_signed_on)
        signals.on_joined.connect(self.on_joined)
        signals.on_channel_users_available.connect(self.on_channel_users_available)
        signals.on_user_joined.connect(self.on_user_joined)
        signals.on_left.connect(self.on_left)
        signals.on_user_left.connect(self.on_user_left)
        signals.on_user_quit.connect(self.on_user_quit)
        signals.on_mode_changed.connect(self.on_mode_changed)
        signals.on_privmsg.connect(self.on_privmsg)
        signals.on_notice.connect(self.on_notice)
        signals.on_nick_changed.connect(self.on_nick_changed)
        signals.on_user_renamed.connect(self.on_user_renamed)
        signals.on_kicked.connect(self.on_kicked)
        signals.on_user_kicked.connect(self.on_user_kicked)
        signals.on_topic_changed.connect(self.on_topic_changed)

    def on_connected(self, emitter):
        log.debug("Connected to %s:%s", self.network_host, self.network_port)
        self.register(self.nickname)

    def on_ctcp_query_ping(self, emitter, user=None, channel=None, data=None):
        """
        See :meth:`~girclib.signals.on_ctcp_query_ping`.
        """
        emitter.ctcp_make_reply(nick_from_netmask(user), [("PING", data)])

    def on_ctcp_query_finger(self, emitter, user=None, channel=None, data=None):
        """
        In case you implement a finger reply, a response should be made like::

            emitter.ctcp_make_reply(nick_from_netmask(user), [('FINGER', reply)])


        See :meth:`~girclib.signals.on_ctcp_query_finger`.

        """

    def on_ctcp_query_version(self, emitter, user=None, channel=None, data=None):
        """
        See :meth:`~girclib.signals.on_ctcp_query_version`.
        """
        if not self.version_name:
            return

        emitter.ctcp_make_reply(nick_from_netmask(user), [
            ('VERSION', '%s:%s:%s' % (self.version_name,
                                      self.version_num or '',
                                      self.version_env or ''))
        ])

    def on_ctcp_query_source(self, emitter, user=None, channel=None, data=None):
        """
        See :meth:`~girclib.signals.on_ctcp_query_source`.
        """
        if self.source_url:
            # The CTCP document (Zeuge, Rollo, Mesander 1994) says that SOURCE
            # replies should be responded to with the location of an anonymous
            # FTP server in host:directory:file format.  I'm taking the liberty
            # of bringing it into the 21st century by sending a URL instead.
            emitter.ctcp_make_reply(nick_from_netmask(user), [
                ('SOURCE', self.source_url), ('SOURCE', None)
            ])

    def on_ctcp_query_userinfo(self, emitter, user=None, channel=None, data=None):
        """
        See :meth:`~girclib.signals.on_ctcp_query_userinfo`.
        """
        if self.userinfo:
            emitter.ctcp_make_reply(nick_from_netmask(user), [
                ('USERINFO', self.userinfo)
            ])

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

    def on_channel_users_available(self, emitter, channel_users=None):
        """
        See :meth:`~girclib.signals.on_channel_users_available`.
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

    def on_privmsg(self, emitter, user=None, channel=None, message=None):
        """
        See :meth:`~girclib.signals.on_privmsg`.
        """

    def on_notice(self, emitter, user=None, channel=None, message=None):
        """
        See :meth:`~girclib.signals.on_notice`.
        """

    def on_nick_changed(self, emitter, nickname=None):
        """
        See :meth:`~girclib.signals.on_nick_changed`.
        """

    def on_user_renamed(self, emitter, oldname=None, newname=None):
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

    def on_topic_changed(self, emitter, user=None, channel=None, new_topic=None):
        """
        See :meth:`~girclib.signals.on_topic_changed`.
        """


if __name__ == '__main__':
    import logging
    from girclib.helpers import setup_logging
    format='%(asctime)s [%(lineno)-4s] %(levelname)-7.7s: %(message)s'
    setup_logging(format, 5)
    client = IRCClient('irc.freenode.net', 6667, 'girclib', 'gIRClib')
    log = logging.getLogger('gIRClib')

    @signals.on_motd.connect
    def _on_motd(emitter, motd=None):
        log.info("Received MOTD")
        client.join("ufs")

    client.connect()

    try:
        while True:
            gevent.sleep(1)
    except KeyboardInterrupt:

        @signals.on_disconnected.connect
        def disconnected(emitter):
            log.info("Exited!?")

        client.disconnect()
