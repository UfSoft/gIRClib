# -*- coding: utf-8 -*-
"""
    girclib.exceptions
    ~~~~~~~~~~~~~~~~~~


    :copyright: © 2011 UfSoft.org - :email:`Pedro Algarvio (pedro@algarvio.me)`
    :license: BSD, see LICENSE for more details.
"""

class IRCBadMessage(Exception):
    pass

class IRCBadModes(ValueError):
    """
    A malformed mode was encountered while attempting to parse a mode string.
    """

class UnhandledCommand(RuntimeError):
    """
    A command dispatcher could not locate an appropriate command handler.
    """

