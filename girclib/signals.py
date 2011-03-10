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

on_privmsg = signal('on-privmsg', """\
Called when I have a message from a user to me or a channel.

:param emitter: The signal emitter
:type  emitter: ``object``

:param channel: The channel the message is coming from.
:type  channel: ``str``

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

on_channel_users_available = signal("on-channel-users-available", """\
Emitted when the list of channel users is available.

:param emitter: The signal emitter
:type  emitter: ``object``

:param channel_users: The channel users list.
:type  channel_users: ``list``

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
#class Signal(NamedSignal):
#    def __init__(self, num, name, doc=None):
#        if doc:
#            doc = """``%s``: %s""" % (num, doc)
#        super(Signal, self).__init__(name, doc=doc)
#
#
#class Namespace(BaseNamespace):
#    """A mapping of signal names to signals."""
#
#    def signal(self, num, name, doc=None):
#        """Return the :class:`NamedSignal` *name*, creating it if required.
#
#        Repeated calls to this function will return the same signal object.
#
#        """
#        try:
#            return self[name]
#        except KeyError:
#            return self.setdefault(name, Signal(num, name, doc))
#
#signal = Namespace().signal
#
#RPL_WELCOME = signal("001", "RPL_WELCOME", """\
#Welcome to the Internet Relay Network ``<nick>!<user>@<host>``
#""")
#
#RPL_YOURHOST = signal("002", "RPL_YOURHOST", """\
#Your host is ``<servername>``, running version ``<ver>``
#""")
#
#RPL_CREATED = signal("003", "RPL_CREATED", """\
#This server was created ``<date>``
#""")
#
#RPL_MYINFO = signal("004", "RPL_MYINFO", """\
#``<servername>`` ``<version>`` ``<available user modes>`` ``<available channel modes>``
#""")
#
#RPL_ISUPPORT = signal("005", "RPL_ISUPPORT", """\
#Please see the `ISUPPORT document`_.
#
#.. _ISUPPORT document: http://www.irc.org/tech_docs/005.html
#""")
#
#RPL_BOUNCE = signal("010", "RPL_BOUNCE", """\
#Try server ``<server name>``, port ``<port number>``
#""")
#
#RPL_USERHOST = signal("302", "RPL_USERHOST", """\
#Reply format used by USERHOST to list replies to the query list:
#  * ``:*1<reply> *( " " <reply> )``
#
#Reply format used by USERHOST to list replies to the query list.
#The reply string is composed as follows::
#
#    reply = nickname [ "*" ] "=" ( "+" / "-" ) hostname
#
#The '``*``' indicates whether the client has registered as an Operator.
#The '``-``' or '``+``' characters represent whether the client has set an AWAY
#message or not respectively.
#""")
#
#RPL_ISON = signal("303", "RPL_ISON", """\
#Reply format used by ISON to list replies to the query list:
#    * ``:*1<nick> *( " " <nick> )``
#
#""")
#
#RPL_AWAY = signal("301", "RPL_AWAY", """``<nick> :<away message>``""")
#
#RPL_UNAWAY = '305'
#RPL_NOWAWAY = '306'
#RPL_WHOISUSER = '311'
#RPL_WHOISSERVER = '312'
#RPL_WHOISOPERATOR = '313'
#RPL_WHOISIDLE = '317'
#RPL_ENDOFWHOIS = '318'
#RPL_WHOISCHANNELS = '319'
#RPL_WHOWASUSER = '314'
#RPL_ENDOFWHOWAS = '369'
#RPL_LISTSTART = '321'
#RPL_LIST = '322'
#RPL_LISTEND = '323'
#RPL_UNIQOPIS = '325'
#RPL_CHANNELMODEIS = '324'
#RPL_NOTOPIC = '331'
#RPL_TOPIC = '332'
#RPL_INVITING = '341'
#RPL_SUMMONING = '342'
#RPL_INVITELIST = '346'
#RPL_ENDOFINVITELIST = '347'
#RPL_EXCEPTLIST = '348'
#RPL_ENDOFEXCEPTLIST = '349'
#RPL_VERSION = '351'
#RPL_WHOREPLY = '352'
#RPL_ENDOFWHO = '315'
#RPL_NAMREPLY = '353'
#RPL_ENDOFNAMES = '366'
#RPL_LINKS = '364'
#RPL_ENDOFLINKS = '365'
#RPL_BANLIST = '367'
#RPL_ENDOFBANLIST = '368'
#RPL_INFO = '371'
#RPL_ENDOFINFO = '374'
#RPL_MOTDSTART = '375'
#RPL_MOTD = '372'
#RPL_ENDOFMOTD = '376'
#RPL_YOUREOPER = '381'
#RPL_REHASHING = '382'
#RPL_YOURESERVICE = '383'
#RPL_TIME = '391'
#RPL_USERSSTART = '392'
#RPL_USERS = '393'
#RPL_ENDOFUSERS = '394'
#RPL_NOUSERS = '395'
#RPL_TRACELINK = '200'
#RPL_TRACECONNECTING = '201'
#RPL_TRACEHANDSHAKE = '202'
#RPL_TRACEUNKNOWN = '203'
#RPL_TRACEOPERATOR = '204'
#RPL_TRACEUSER = '205'
#RPL_TRACESERVER = '206'
#RPL_TRACESERVICE = '207'
#RPL_TRACENEWTYPE = '208'
#RPL_TRACECLASS = '209'
#RPL_TRACERECONNECT = '210'
#RPL_TRACELOG = '261'
#RPL_TRACEEND = '262'
#RPL_STATSLINKINFO = '211'
#RPL_STATSCOMMANDS = '212'
#RPL_ENDOFSTATS = '219'
#RPL_STATSUPTIME = '242'
#RPL_STATSOLINE = '243'
#RPL_UMODEIS = '221'
#RPL_SERVLIST = '234'
#RPL_SERVLISTEND = '235'
#RPL_LUSERCLIENT = '251'
#RPL_LUSEROP = '252'
#RPL_LUSERUNKNOWN = '253'
#RPL_LUSERCHANNELS = '254'
#RPL_LUSERME = '255'
#RPL_ADMINME = '256'
#RPL_ADMINLOC = '257'
#RPL_ADMINLOC = '258'
#RPL_ADMINEMAIL = '259'
#RPL_TRYAGAIN = '263'
#ERR_NOSUCHNICK = '401'
#ERR_NOSUCHSERVER = '402'
#ERR_NOSUCHCHANNEL = '403'
#ERR_CANNOTSENDTOCHAN = '404'
#ERR_TOOMANYCHANNELS = '405'
#ERR_WASNOSUCHNICK = '406'
#ERR_TOOMANYTARGETS = '407'
#ERR_NOSUCHSERVICE = '408'
#ERR_NOORIGIN = '409'
#ERR_NORECIPIENT = '411'
#ERR_NOTEXTTOSEND = '412'
#ERR_NOTOPLEVEL = '413'
#ERR_WILDTOPLEVEL = '414'
#ERR_BADMASK = '415'
#ERR_UNKNOWNCOMMAND = '421'
#ERR_NOMOTD = '422'
#ERR_NOADMININFO = '423'
#ERR_FILEERROR = '424'
#ERR_NONICKNAMEGIVEN = '431'
#ERR_ERRONEUSNICKNAME = '432'
#ERR_NICKNAMEINUSE = '433'
#ERR_NICKCOLLISION = '436'
#ERR_UNAVAILRESOURCE = '437'
#ERR_USERNOTINCHANNEL = '441'
#ERR_NOTONCHANNEL = '442'
#ERR_USERONCHANNEL = '443'
#ERR_NOLOGIN = '444'
#ERR_SUMMONDISABLED = '445'
#ERR_USERSDISABLED = '446'
#ERR_NOTREGISTERED = '451'
#ERR_NEEDMOREPARAMS = '461'
#ERR_ALREADYREGISTRED = '462'
#ERR_NOPERMFORHOST = '463'
#ERR_PASSWDMISMATCH = '464'
#ERR_YOUREBANNEDCREEP = '465'
#ERR_YOUWILLBEBANNED = '466'
#ERR_KEYSET = '467'
#ERR_CHANNELISFULL = '471'
#ERR_UNKNOWNMODE = '472'
#ERR_INVITEONLYCHAN = '473'
#ERR_BANNEDFROMCHAN = '474'
#ERR_BADCHANNELKEY = '475'
#ERR_BADCHANMASK = '476'
#ERR_NOCHANMODES = '477'
#ERR_BANLISTFULL = '478'
#ERR_NOPRIVILEGES = '481'
#ERR_CHANOPRIVSNEEDED = '482'
#ERR_CANTKILLSERVER = '483'
#ERR_RESTRICTED = '484'
#ERR_UNIQOPPRIVSNEEDED = '485'
#ERR_NOOPERHOST = '491'
#ERR_NOSERVICEHOST = '492'
#ERR_UMODEUNKNOWNFLAG = '501'
#ERR_USERSDONTMATCH = '502'
