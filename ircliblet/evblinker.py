# -*- coding: utf-8 -*-
"""
    ircliblet.evblinker
    ~~~~~~~~~~~~~~~~~~~


    :copyright: © 2011 UfSoft.org - :email:`Pedro Algarvio (pedro@algarvio.me)`
    :license: BSD, see LICENSE for more details.
"""

#@PydevCodeAnalysisIgnore

import eventlet
import logging
import blinker.base

log = logging.getLogger(__name__)

class NamedSignal(blinker.base.NamedSignal):
    def __init__(self, name, doc=None):
        super(NamedSignal, self).__init__(name, doc=doc)
        self.pool = eventlet.GreenPool()

    def send(self, *sender, **kwargs):
        """Emit this signal on behalf of *sender*, passing on \*\*kwargs.

        Returns a list of 2-tuples, pairing receivers with their return
        value. The ordering of receiver notification is undefined.

        :param \*sender: Any object or ``None``.  If omitted, synonymous
                         with ``None``.  Only accepts one positional argument.

        :param \*\*kwargs: Data to be sent to receivers.

        :type _waitall: ``bool``
        :param _waitall: Boolean value which if set to ``True`` will not use
                         eventlet's Pile and will run the receivers one after
                         the other until all have finished.
        """
        waitall = kwargs.pop('_waitall', False)
        # Using '*sender' rather than 'sender=None' allows 'sender' to be
        # used as a keyword argument- i.e. it's an invisible name in the
        # function signature.
        if len(sender) == 0:
            sender = None
        elif len(sender) > 1:
            raise TypeError('send() accepts only one positional argument, '
                            '%s given' % len(sender))
        else:
            sender = sender[0]

        try:
            sender_name = '.'.join([str(sender.__module__),
                                    sender.__class__.__name__])
        except:
            sender_name = sender

        log.log(5, "signal: %r  sender: %r  kwargs: %r",
                self.name, sender_name, kwargs)

        if not self.receivers:
            return []

        if waitall:
            results = []
            for receiver in self.receivers_for(sender):
                try:
                    results.append((receiver, receiver(sender, **kwargs)))
                except Exception, err:
                    log.exception(err)
            return results

        def spawned_receiver(receiver, sender, kwargs):
            log.log(5, "spawned %r for signal %r, sender: %r  kwargs: %r",
                    receiver, self.name, sender, kwargs)
            try:
                return receiver, eventlet.spawn(receiver, sender, **kwargs)
            except Exception, err:
                log.error("Failed to run spawned function")
                log.exception(err)

        pile = eventlet.GreenPile(self.pool)
        for receiver in self.receivers_for(sender):
            log.log(5, "Spawning for receiver: %s", receiver)
            pile.spawn(spawned_receiver, receiver, sender, kwargs)
        return pile

#    def connect(self, receiver, sender=blinker.base.ANY, weak=True):
#        return blinker.base.NamedSignal.connect(
#            self, receiver, sender=sender, weak=weak
#        )



class Namespace(blinker.base.Namespace):
    """A mapping of signal names to signals."""

    def signal(self, name, doc=None):
        """Return the :class:`NamedSignal` *name*, creating it if required.

        Repeated calls to this function will return the same signal object.

        """
        try:
            return self[name]
        except KeyError:
            return self.setdefault(name, NamedSignal(name, doc))

signal = Namespace().signal

