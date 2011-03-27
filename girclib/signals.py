# -*- coding: utf-8 -*-
"""
    girclib.signals
    ~~~~~~~~~~~~~~~


    :copyright: © 2011 UfSoft.org - :email:`Pedro Algarvio (pedro@algarvio.me)`
    :license: BSD, see LICENSE for more details.
"""

from girclib.gblinker import signal

on_connected = signal('on-connected', """\
Called once connected to the IRC network.

:param emitter: The signal emitter, in this case a
                :class:`~girclib.client.IRCTransport` instance.
:type  emitter: ``object``

""")

on_quited = signal('on-quited', """\
Called once quited from the IRC network.

:param emitter: The signal emitter, in this case a
                :class:`~girclib.client.IRCTransport` instance.
:type  emitter: ``object``

""")

on_disconnected = signal('on-disconnected', """\
Called once disconnected from the IRC network.

:param emitter: The signal emitter, in this case a
                :class:`~girclib.client.IRCTransport` instance.
:type  emitter: ``object``

""")

on_rpl_created = signal("on-rpl-created", """\
Called with creation date information about the server, usually at logon.

:type when: ``str``
:param when: A string describing when the server was created, probably.

""")

on_rpl_yourhost = signal("on_rpl_yourhost", """\
Called with daemon information about the server, usually at logon.

:type info: ``str``
:param when: A string describing what software the server is running, probably.

""")

on_rpl_myinfo = signal("on-rpl-myinfo", """\
Called with information about the server, usually at logon.

:type servername: ``str``
:param servername: The hostname of this server.

:type version: ``str``
:param version: A description of what software this server runs.

:type umodes: ``str``
:param umodes: All the available user modes.

:type cmodes: ``str``
:param cmodes: All the available channel modes.

""")

on_rpl_luserclient = signal("on-rpl-luserclient", """\
Called with information about the number of connections, usually at logon.

:type info: ``str``
:param info: A description of the number of clients and servers
             connected to the network, probably.

""")

on_rpl_bounce = signal("on_rpl_bounce", """\
Called with information about where the client should reconnect.

:type info: ``str``
:param info: A plain-text description of the address that should be connected to.

""")

on_rpl_isupport = signal("on-rpl-isupport", """\
Called with various information about what the server supports.

:type options: ``list`` of ``str``
:param options: Descriptions of features or limits of the server, possibly in
                the form "NAME=VALUE".

""")

on_rpl_luserchannels = signal("on_rpl_luserchannels", """\
Called with the number of channels existing on the server.

:type channels: ``int``
:param channels: Number of channels existing on the server.

""")

on_rpl_luserop = signal("on-rpl-luserop", """\
Called with the number of ops logged on to the server.

:type  ops: ``int``
:param ops: Number of operators logged on to the server.

""")

on_rpl_luserme = signal("on-rpl-luserme", """\
Called with information about the server connected to.

:type  info: ``str``
:param info: A plain-text string describing the number of users and servers
             connected to this server.

""")

on_rpl_topic = signal("on-rpl-topic", """\
Called with the initial information about the channel's topic

:type  channel: ``str``
:param channel: The channel name.

:type  topic: ``str``
:param topic: The channel's topic.
""")

on_rpl_notopic = signal("on-rpl-topic", """\
Called when the channel has no topic set

:type  channel: ``str``
:param channel: The channel name.

""")

on_rpl_namreply = signal("on-rpl-namreply", """\
Called whenever we receive a channel's user list. The user's list is only
complete when :meth:`~girclib.signals.on_rpl_endofnames` is called.

:param emitter: The signal emitter
:type  emitter: ``object``

:type  channel: ``str``
:param channel: The channel name.

:type  users: ``list``
:param users: List of channel users.

:type  privacy: ``str``
:param privacy: Channel privacy. One of ``@`` (secret channel), ``*`` (private
    channel) or ``=`` (public channel).

""")

on_rpl_endofnames = signal("on-rpl-endofnames", """\
Called once we have received all channel's users. See
:meth:`~girclib.signals.on_rpl_namreply`.

:param emitter: The signal emitter
:type  emitter: ``object``

:type  channel: ``str``
:param channel: The channel name.

""")

on_rpl_list = signal("on_rpl_list", """\
Called for each of the channels from a network when our client issues
:class:`~girclib.irc.IRCCommandsHelper.list`.

:param emitter: The signal emitter
:type  emitter: ``object``

:type  channel: ``str``
:param channel: The channel name.

:type  ucount: ``int``
:param ucount: The number of users in the channel.

:type  topic: ``str``
:param topic: The channel's topic.
""")

on_rpl_listend = signal("on_rpl_listend", """\
Called once we have the full list of channels on the network. See
:class:`~girclib.irc.IRCCommandsHelper.list` and
:class:`~girclib.signals.on_rpl_list`.

:param emitter: The signal emitter
:type  emitter: ``object``

""")

on_privmsg = signal('on-privmsg', """\
Called when I receive a message from a user to me.

:param emitter: The signal emitter
:type  emitter: ``object``

:param user: The user the message is coming from.
:type  user: ``str``

:param message: The message.
:type  message: ``str``

""")

on_chanmsg = signal('on-chanmsg', """\
Called when I receive a message from a channel.

:param emitter: The signal emitter
:type  emitter: ``object``

:param channel: The channel the message is coming from.
:type  channel: ``str``

:param user: The user who sent the message.
:type  user: ``str``

:param message: The message.
:type  message: ``str``

""")

on_joined = signal('on-joined', """\
Called when the client(we) finish joining a channel.  The ``channel`` has the
starting character (``#``, ``&``, ``!`` or ``+``) intact.

:param emitter: The signal emitter
:type  emitter: ``object``

:param channel: the channel joined
:type  channel: ``str``

""")

on_left = signal('on-left', """\
Called when the client(we) have left a channel.  The ``channel`` has the
starting character (``#``, ``&``, ``!`` or ``+``) intact.

:param emitter: The signal emitter
:type  emitter: ``object``

:param channel: the channel left
:type  channel: ``str``

""")

on_notice = signal('on-notice', """\
Called when I have a notice from a user to me or a channel.

If the client makes any automated replies, it must not do so in response to a
``NOTICE`` message, per the RFC::

    The difference between NOTICE and PRIVMSG is that
    automatic replies MUST NEVER be sent in response to a
    NOTICE message. [...] The object of this rule is to avoid
    loops between clients automatically sending something in
    response to something it received.


:param emitter: The signal emitter
:type  emitter: ``object``

:param user: the user sending the notice
:type  user: ``str``

:param channel: the channel where the notice is coming from
:type  channel: ``str``

:param message: the notice message
:type  message: ``str``

""")

on_mode_changed = signal('on-mode-changed', """\
Called when users or channel's modes are changed.

:param emitter: The signal emitter
:type  emitter: ``object``

:type user: ``str``
:param user: The user and hostmask which instigated this change.

:type channel: ``str``
:param channel: The channel where the modes are changed. If args is
                empty the channel for which the modes are changing. If the
                changes are at server level it could be equal to ``user``.

:type set: ``bool``
:param set: True if the mode(s) is being added, False if it is being removed.
            If some modes are added and others removed at the same time this
            function will be called twice, the first time with all the added
            modes, the second with the removed ones. (To change this behaviour
            override the ``irc_MODE`` method)

:type modes: ``str``
:param modes: The mode or modes which are being changed.

:type args: ``tuple``
:param args: Any additional information required for the mode change.

""")

on_pong = signal('on-pong', """\
Emitted with the results of a CTCP PING query.

:param emitter: The signal emitter
:type  emitter: ``object``

:param user: The user.
:type  user: ``str``

:param secs: Number of seconds
:type  secs: ``float``
""")

on_signed_on = signal('on-signed-on', """\
Called after successfully signing on to the server.

:param emitter: The signal emitter
:type  emitter: ``object``

""")

on_kicked = signal('on-kicked', """\
Called when I am kicked from a channel.

:param emitter: The signal emitter
:type  emitter: ``object``

:param channel: The channel being kicked from.
:type  channel: ``str``

:param kicker: The user that kicked.
:type  kicker: ``str``

:param message: The kick message.
:type  message: ``str``

""")

on_nick_changed = signal('on-nick-changed', """\
Called when my nick has been changed.

:param emitter: The signal emitter
:type  emitter: ``object``

:param nickname: The nickname.
:type  nickname: ``str``

""")

on_user_joined = signal('on-user-joined', """\
Called when I see another user joining a channel.

:param emitter: The signal emitter
:type  emitter: ``object``

:param channel: The channel the message is coming from.
:type  channel: ``str``

:param user: The joining.
:type  user: ``str``

""")

on_user_left = signal('on-user-joined', """\
Called when I see another user leaving a channel.

:param emitter: The signal emitter
:type  emitter: ``object``

:param channel: The channel the message is coming from.
:type  channel: ``str``

:param user: The user leaving.
:type  user: ``str``

""")

on_user_quit = signal('on-user-quit', """\
Called when I see another user disconnect from the network.

:param emitter: The signal emitter
:type  emitter: ``object``

:param user: The user quiting.
:type  user: ``str``

:param message: The quit message.
:type  message: ``str``

""")

on_user_kicked = signal('on-user-kicked', """\
Called when I observe someone else being kicked from a channel.

:param emitter: The signal emitter
:type  emitter: ``object``

:param kicked: The user being kicked.
:type  kicked: ``str``

:param channel: The channel the user is being kicked from.
:type  channel: ``str``

:param message: The kick message.
:type  channel: ``str``

""")

on_action = signal('on-action', """\
Called when I see a user perform an ``ACTION`` on a channel.

:param emitter: The signal emitter
:type  emitter: ``object``

:param user: The user that performed the ``ACTION``
:type  user: ``str``

:param channel: The channel the ``ACTION`` is coming from.
:type  channel: ``str``

:param data: The ``ACTION`` data.
:type  data: ``str``

""")

on_topic_changed = signal('on-topic-changed', """\
In channel, user changed the topic to ``new_topic``. Also called when first
joining a channel.

:param emitter: The signal emitter
:type  emitter: ``object``

:param user: The user changing the topic.
:type  user: ``str``

:param channel: The channel the topic is being changed.
:type  channel: ``str``

:param new_topic: The channel's new topic.
:type  new_topic: ``str``

""")

on_user_renamed = signal('on-user-renamed', """\
A user changed their name from oldname to newname.

:param emitter: The signal emitter
:type  emitter: ``object``

:param oldname: The old name.
:type  oldname: ``str``

:param newname: The new name.
:type  newname: ``str``

""")

on_motd = signal('on-motd', """\
I received a message-of-the-day banner from the server.

:param emitter: The signal emitter
:type  emitter: ``object``

:type motd: ``list``
:param motd: list of strings, where each string was sent as a separate
             message from the server.

To display and get a nicely formatted string, you might want to use::

    '\\n'.join(motd)

""")


on_nickname_in_use = signal("on-nickname-in-use", """\
Called when we try to register or change to a nickname that is already taken.

:param emitter: The signal emitter
:type  emitter: ``object``

:param nickname: The nickname which is in use.
:type  nickname: ``str``

""")

on_erroneous_nickname = signal("on-erroneous-nickname", """\
Called when we try to register or change to an illegal nickname.

The server should send this reply when the nickname contains any disallowed
characters.  The bot will stall, waiting for ``RPL_WELCOME``, if we don't handle
this during sign-on.

:note: The method uses the spelling *erroneus*, as it appears in the RFC,
       section 6.1.

:param emitter: The signal emitter
:type  emitter: ``object``

:param nickname: The erroneous nickname.
:type  nickname: ``str``

""")

on_password_mismatch = signal("on-password-mismatch", """
Emitted when the login was incorrect.

:param emitter: The signal emitter
:type  emitter: ``object``

""")

on_banned = signal("on-banned", """\
Emitted when the client has been banned from a channel.

:param emitter: The signal emitter
:type  emitter: ``object``

:param channel: The banned channel.
:type  channel: ``str``

:param message: The banned message.
:type  message: ``str``

""")

on_user_banned = signal("on-user-banned", """\
Emitted when the client has been banned from a channel.

:param emitter: The signal emitter
:type  emitter: ``object``

:param channel: The banned channel.
:type  channel: ``str``

:param user: The user banned.
:type  user: ``str``

:param message: The banned message.
:type  message: ``str``

""")

on_channels_available = signal("on-channels-available", """\
Emitted after issuing a LIST command and when the complete list of channels a
server handles is available.

:param emitter: The signal emitter
:type  emitter: ``object``

:param channels: A list of tuples in the form of (channel_name, users_count, topic)
:type  channels: ``list``

""")


# CTCP Signals
on_ctcp_query_ping = signal("on-ctcp-query-ping", """
Emitted when receiving a PING query.

A CTCP reply must be made with the data received.

:param emitter: The signal emitter
:type  emitter: ``object``

:param user: the nickname netmask querying
:type  user: ``str``

:param channel: the channel name
:type  channel: ``str``

:param data: the query data
:type  data: ``str``
""")

on_ctcp_query_finger = signal("on-ctcp-query-finger", """
Emitted when receiving a FINGER query.

:param emitter: The signal emitter
:type  emitter: ``object``

:param user: the nickname netmask querying
:type  user: ``str``

:param channel: the channel name
:type  channel: ``str``

:param data: the query data
:type  data: ``str``
""")

on_ctcp_query_version = signal("on-ctcp-query-version", """
Emitted when receiving a VERSION query.

:param emitter: The signal emitter
:type  emitter: ``object``

:param user: the nickname netmask querying
:type  user: ``str``

:param channel: the channel name
:type  channel: ``str``

:param data: the query data
:type  data: ``str``
""")

on_ctcp_query_source = signal("on-ctcp-query-source", """
Emitted when receiving a SOURCE query.

:param emitter: The signal emitter
:type  emitter: ``object``

:param user: the nickname netmask querying
:type  user: ``str``

:param channel: the channel name
:type  channel: ``str``

:param data: the query data
:type  data: ``str``
""")

on_ctcp_query_userinfo = signal("on-ctcp-query-userinfo", """
Emitted when receiving a SOURCE query.

:param emitter: The signal emitter
:type  emitter: ``object``

:param user: the nickname netmask querying
:type  user: ``str``

:param channel: the channel name
:type  channel: ``str``

:param data: the query data
:type  data: ``str``
""")

