# -*- coding: utf-8 -*-
"""
    girclib.gblinker
    ~~~~~~~~~~~~~~~~


    :copyright: © 2011 UfSoft.org - :email:`Pedro Algarvio (pedro@algarvio.me)`
    :license: BSD, see LICENSE for more details.
"""

import logging
import blinker.base
from gevent.pool import Pool

log = logging.getLogger(__name__)

class NamedSignal(blinker.base.NamedSignal):
    def __init__(self, name, doc=None):
        super(NamedSignal, self).__init__(name, doc=doc)
        self.pool = Pool()

    def send(self, *sender, **kwargs):
        """Emit this signal on behalf of *sender*, passing on \*\*kwargs.

        Returns a list of 2-tuples, pairing receivers with their return
        value. The ordering of receiver notification is undefined.

        :param \*sender: Any object or ``None``.  If omitted, synonymous
                         with ``None``.  Only accepts one positional argument.

        :param \*\*kwargs: Data to be sent to receivers.

        """
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

        log.log(5, "signal: %r  sender: %r  kwargs: %r  receivers: %r",
                self.name, sender_name, kwargs, self.receivers)

        if not self.receivers:
            return []

        results = []

        def spawned_receiver(receiver, sender, kwargs):
            log.log(5, "spawned %r for signal %r, sender: %r  kwargs: %r",
                    receiver, self.name, sender, kwargs)
            try:
                results.append((receiver, receiver(sender, **kwargs)))
            except Exception, err:
                log.error("Failed to run spawned function")
                log.exception(err)

        for receiver in self.receivers_for(sender):
            log.log(5, "Spawning for receiver: %s", receiver)
            self.pool.spawn(spawned_receiver, receiver, sender, kwargs)

        # Wait for results
        self.pool.join()
        return results

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
