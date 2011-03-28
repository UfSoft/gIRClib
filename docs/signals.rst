.. _signals:

Signals
=======

Signaling support is provided by the excellent `blinker`_ library.

What are signals?  Signals help you decouple applications by sending
notifications when actions occur elsewhere in the core framework or
another decoupled part of the application.  In short, signals allow certain
senders to notify subscribers that something happened.

gIRClib comes with a bunch of signals.
Also keep in mind that signals are intended to notify subscribers
and should not encourage subscribers to modify data.

The big advantage of signals over handlers is that you can safely
subscribe to them for the split of a second.  These temporary subscriptions
are helpful for unittesting for example.

Subscribing to Signals
----------------------

To subscribe to a signal, you can use the
:meth:`~blinker.base.Signal.connect` method of a signal.  The first
argument is the function that should be called when the signal is emitted,
the optional second argument specifies a sender.  To unsubscribe from a
signal, you can use the :meth:`~blinker.base.Signal.disconnect` method.



Decorator Based Signal Subscriptions
------------------------------------

With Blinker 1.1 you can also easily subscribe to signals by using the
:meth:`~blinker.base.NamedSignal.connect` decorator::

    from girclib.signals import on_connected

    @on_connected.connect
    def on_connected_signal(sender):
      print 'Connected!'


gIRClib Signaling
=================

Signaling is used throughout the library to handle the several actions needed
to interact with an IRC server.

.. module:: girclib.signals

Signals
-------

.. autofunction:: on_connected(emitter)
.. autofunction:: on_quited(emitter)
.. autofunction:: on_disconnected(emitter)
.. autofunction:: on_privmsg(emitter, channel=None, message=None)
.. autofunction:: on_chanmsg(emitter, channel=None, user=None, message=None)
.. autofunction:: on_joined(emitter, channel=None)
.. autofunction:: on_left(emitter, channel=None)
.. autofunction:: on_notice(emitter, user=None, channel=None, message=None)
.. autofunction:: on_mode_changed(emitter, user=None, channel=None, set=None, modes=None, args=None)
.. autofunction:: on_pong(emitter, user=None, secs=None)
.. autofunction:: on_signed_on(emitter)
.. autofunction:: on_kicked(emitter, channel=None, kicker=None, message=None)
.. autofunction:: on_nick_changed(emitter, user=None)
.. autofunction:: on_user_joined(emitter, user=None, channel=None)
.. autofunction:: on_user_left(emitter, user=None, channel=None)
.. autofunction:: on_user_quit(emitter, user=None, message=None)
.. autofunction:: on_user_kicked(emitter, channel=None, kicked=None, kicker=None, message=None)
.. autofunction:: on_action(emitter, user=None, channel=None, data=None)
.. autofunction:: on_topic_changed(emitter, user=None, channel=None, new_topic=None)
.. autofunction:: on_user_renamed(emitter, user=None, newname=None)
.. autofunction:: on_motd(emitter, motd=None)
.. autofunction:: on_nickname_in_use(emitter, nickname=None)
.. autofunction:: on_erroneous_nickname(emitter, nickname=None)
.. autofunction:: on_password_mismatch(emitter)
.. autofunction:: on_banned(emitter, channel=None, message=None)
.. autofunction:: on_user_banned(emitter, channel=None, user=None, message=None)


Server Queries
~~~~~~~~~~~~~~

These are queries from the IRC server we're connecting to to this IRC client.

Signals
.......

.. autofunction:: on_ctcp_query_ping(emitter, user=None, channel=None, data=None)
.. autofunction:: on_ctcp_query_finger(emitter, user=None, channel=None, data=None)
.. autofunction:: on_ctcp_query_version(emitter, user=None, channel=None, data=None)
.. autofunction:: on_ctcp_query_source(emitter, user=None, channel=None, data=None)
.. autofunction:: on_ctcp_query_userinfo(emitter, user=None, channel=None, data=None)


Server Replies
~~~~~~~~~~~~~~

These are replies from the IRC server we're connecting to to this IRC client.

Signals
.......

.. autofunction:: on_rpl_created(emitter, when=None)
.. autofunction:: on_rpl_yourhost(emitter, info=None)
.. autofunction:: on_rpl_myinfo(emitter, servername=None, version=None, umodes=None, cmodes=None)
.. autofunction:: on_rpl_luserme(emitter, info=None)
.. autofunction:: on_rpl_luserclient(emitter, info=None)
.. autofunction:: on_rpl_luserchannels(emitter, channels=None)
.. autofunction:: on_rpl_luserop(emitter, channels=None)
.. autofunction:: on_rpl_bounce(emitter, info=None)
.. autofunction:: on_rpl_isupport(emitter, options=None)
.. autofunction:: on_rpl_topic(emitter, user=None, channel=None, topic=None)
.. autofunction:: on_rpl_notopic(emitter, user=None, channel=None)
.. autofunction:: on_rpl_namreply(emitter, channel=None, users=None, privacy)
.. autofunction:: on_rpl_endofnames(emitter, channel=None)
.. autofunction:: on_rpl_list(emitter, channel=None, count=None, topic=None)
.. autofunction:: on_rpl_listend(emitter)


.. _blinker: http://pypi.python.org/pypi/blinker
