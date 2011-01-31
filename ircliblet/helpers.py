# -*- coding: utf-8 -*-
"""
    ircliblet.helpers
    ~~~~~~~~~~~~~~~~~


    :copyright: © 2011 UfSoft.org - :email:`Pedro Algarvio (pedro@algarvio.me)`
    :license: BSD, see LICENSE for more details.
"""

import re
import sys
import types
import string
import logging
import textwrap
from ircliblet.constants import numeric_to_symbolic
from ircliblet.exceptions import IRCBadModes, UnhandledCommand

NUL     = chr(0)
CR      = chr(015)
NL      = chr(012)
LF      = NL
SPC     = chr(040)

# This includes the CRLF terminator characters.
MAX_COMMAND_LENGTH = 512
CHANNEL_PREFIXES = '&#!+'

if sys.version_info >= (3,0,0):
    def to_uni(x, encoding='utf-8'):
        """ Convert anything to unicode """
        return str(x, encoding=encoding) if isinstance(x, bytes) else str(x)
else:
    bytes = str
    def to_uni(x, encoding='utf-8'):
        """ Convert anything to unicode """
        return x if isinstance(x, unicode) else unicode(str(x), encoding=encoding)

def to_bytes(data, encoding='utf-8'):
    """ Convert anything to bytes """
    return data.encode(encoding) if isinstance(data, unicode) else bytes(data)

if sys.version_info >= (3,0,0):
    native = to_uni
else:
    native = to_bytes
native.__doc__ = """ Convert anything to native strings """

def ascii(data):
    """Convert an ASCII string to a native string"""
    return native(data, encoding='ascii')

def parse_modes(modes, params, param_modes=('', '')):
    """
    Parse an IRC mode string.

    The mode string is parsed into two lists of mode changes (added and
    removed), with each mode change represented as `(mode, param)` where mode
    is the mode character, and param is the parameter passed for that mode, or
    `None` if no parameter is required.

    :type modes: `str`
    :param modes: Modes string to parse.

    :type params: `list`
    :param params: Parameters specified along with `modes`.

    :type param_modes: `(str, str)`
    :param param_modes: A pair of strings (`(add, remove)`) that indicate which
                        modes take parameters when added or removed.

    :returns: Two lists of mode changes, one for modes added and the other for
              modes removed respectively, mode changes in each list are
              represented as `(mode, param)`.

    """
    if len(modes) == 0:
        raise IRCBadModes('Empty mode string')

    if modes[0] not in '+-':
        raise IRCBadModes('Malformed modes string: %r' % (modes,))

    changes = ([], [])

    direction = None
    count = -1
    for ch in modes:
        if ch in '+-':
            if count == 0:
                raise IRCBadModes('Empty mode sequence: %r' % (modes,))
            direction = '+-'.index(ch)
            count = 0
        else:
            param = None
            if ch in param_modes[direction]:
                try:
                    param = params.pop(0)
                except IndexError:
                    raise IRCBadModes('Not enough parameters: %r' % (ch,))
            changes[direction].append((ch, param))
            count += 1

    if len(params) > 0:
        raise IRCBadModes('Too many parameters: %r %r' % (modes, params))

    if count == 0:
        raise IRCBadModes('Empty mode sequence: %r' % (modes,))

    return changes

def split(text, length=80):
    """
    Split a string into multiple lines.

    White-space near ``str[length]`` will be preferred as a breaking point.
    "``\\n``" will also be used as a breaking point.

    :param str: The string to split.
    :type  str: ``str``

    :param length: The maximum length which will be allowed for any string in
                   the result.
    :type  length: ``int``

    :rtype: ``list`` of ``str``

    """
    return [chunk for line in text.split(ascii('\n')) for
            chunk in textwrap.wrap(line, length)]

def _int_or_default(value, default=None):
    """
    Convert a value to an integer if possible.

    :rtype: ``int`` or type of ``default``
    :returns: An integer when ``value`` can be converted to an integer,
              otherwise return ``default``
    """
    if value:
        try:
            return int(value)
        except (TypeError, ValueError):
            pass
    return default

def nick_from_netmask(netmask):
    """
    Return the nickname from a netmask

    :rtype: ``str``
    :returns: Returns the nickname part of a netmask.

    """
    return netmask.split(ascii('!'))[0]

X_DELIM = chr(001)

def ctcp_extract(message):
    """Extract CTCP data from a string.

    Returns a dictionary with two items:
        * **extended**: a list of CTCP ``(tag, data)`` tuples
        * **normal**: a list of strings which were not inside a CTCP delimiter
    """

    extended_messages = []
    normal_messages = []
    retval = {'extended': extended_messages,
              'normal': normal_messages }

    messages = native(message).split(X_DELIM)
    odd = 0

    # X1 extended data X2 nomal data X3 extended data X4 normal...
    while messages:
        if odd:
            extended_messages.append(messages.pop(0))
        else:
            normal_messages.append(messages.pop(0))
        odd = not odd

    extended_messages[:] = filter(None, extended_messages)
    normal_messages[:] = filter(None, normal_messages)

    extended_messages[:] = map(ctcp_dequote, extended_messages)
    for i in xrange(len(extended_messages)):
        m = string.split(extended_messages[i], SPC, 1)
        tag = m[0]
        if len(m) > 1:
            data = m[1]
        else:
            data = None

        extended_messages[i] = (tag, data)

    return retval

# CTCP escaping
M_QUOTE= chr(020)

m_quote_table = {
    NUL: M_QUOTE + '0',
    NL: M_QUOTE + 'n',
    CR: M_QUOTE + 'r',
    M_QUOTE: M_QUOTE + M_QUOTE
    }

m_dequote_table = {}
for k, v in m_quote_table.items():
    m_dequote_table[v[-1]] = k
del k, v

m_escape_re = re.compile('%s.' % (re.escape(M_QUOTE),), re.DOTALL)

def low_quote(s):
    for c in (M_QUOTE, NUL, NL, CR):
        s = string.replace(s, c, m_quote_table[c])
    return s

def low_dequote(s):
    def sub(matchobj, m_dequote_table=m_dequote_table):
        s = matchobj.group()[1]
        try:
            s = m_dequote_table[s]
        except KeyError:
            s = s
        return s

    return m_escape_re.sub(sub, s)

X_QUOTE = '\\'

x_quote_table = {
    X_DELIM: X_QUOTE + 'a',
    X_QUOTE: X_QUOTE + X_QUOTE
    }

x_dequote_table = {}

for k, v in x_quote_table.items():
    x_dequote_table[v[-1]] = k

x_escape_re = re.compile('%s.' % (re.escape(X_QUOTE),), re.DOTALL)

def ctcp_quote(s):
    for c in (X_QUOTE, X_DELIM):
        s = string.replace(s, c, x_quote_table[c])
    return s

def ctcp_dequote(s):
    def sub(matchobj, x_dequote_table=x_dequote_table):
        s = matchobj.group()[1]
        try:
            s = x_quote_table[s]
        except KeyError:
            s = s
        return s

    return x_escape_re.sub(sub, s)

def ctcp_stringify(messages):
    """
    :type  messages: ``list``
    :param messages: a list of extended messages.  An extended message is a
                     ``(tag, data)`` tuple, where 'data' may be ``None``, a
                     ``string``, or a ``list`` of strings to be joined with
                     white-space.

    :rtype: ``str``
    :returns: *Stringified* message
    """
    coded_messages = []
    for (tag, data) in messages:
        if data:
            if not isinstance(data, types.StringType):
                try:
                    # data as list-of-strings
                    data = " ".join(map(str, data))
                except TypeError:
                    # No?  Then use it's %s representation.
                    pass
            m = native("%s %s" % (tag, data))
        else:
            m = native(tag)
        m = ctcp_quote(m)
        m = native("%s%s%s" % (X_DELIM, m, X_DELIM))
        coded_messages.append(m)
    return native("").join(coded_messages)


def parse_raw_irc_command(element):
    """
    This function parses a raw irc command and returns a tuple
    of (prefix, command, args).
    The following is a pseudo BNF of the input text::

        <message>  ::= [':' <prefix> <SPACE> ] <command> <params> <crlf>
        <prefix>   ::= <servername> | <nick> [ '!' <user> ] [ '@' <host> ]
        <command>  ::= <letter> { <letter> } | <number> <number> <number>
        <SPACE>    ::= ' ' { ' ' }
        <params>   ::= <SPACE> [ ':' <trailing> | <middle> <params> ]

        <middle>   ::= <Any *non-empty* sequence of octets not including SPACE
                       or NUL or CR or LF, the first of which may not be ':'>
        <trailing> ::= <Any, possibly *empty*, sequence of octets not including
                       NUL or CR or LF>

        <crlf>     ::= CR LF


    """
    parts = element.strip().split(ascii(" "))
    if parts[0].startswith(ascii(":")):
        prefix = parts[0][1:]
        command = parts[1]
        args = parts[2:]
    else:
        prefix = None
        command = parts[0]
        args = parts[1:]

    if command.isdigit():
        try:
            command = numeric_to_symbolic[command]
        except KeyError:
            logging.warn('unknown numeric event %s' % command)
#    command = command.lower()
    command = command.upper()

    if args[0].startswith(ascii(":")):
        args = [ascii(" ").join(args)[1:]]
    else:
        for idx, arg in enumerate(args):
            if arg.startswith(ascii(":")):
                args = args[:idx] + [ascii(" ").join(args[idx:])[1:]]
                break

    return (prefix, command, args)

class _CommandDispatcherMixin(object):
    """
    Dispatch commands to handlers based on their name.

    Command handler names should be of the form ``prefix_COMMAND_NAME``,
    where ``prefix`` is the value specified by ``prefix``, and must
    accept the parameters as given to ``dispatch``.

    Attempting to mix this in more than once for a single class will cause
    strange behaviour, due to ``prefix`` being overwritten.

    :type prefix: ``str``
    :ivar prefix: Command handler prefix, used to locate handler attributes
    """
    prefix = None

    def dispatch(self, command_name, *args):
        """
        Perform actual command dispatch.
        """
        def _get_method_name(command):
            return '%s_%s' % (self.prefix, command)

        def _get_method(name):
            return getattr(self, _get_method_name(name), None)

        method = _get_method(command_name)
        if method is not None:
            return method(*args)

        method = _get_method('unknown')
        if method is None:
            raise UnhandledCommand("No handler for %r could be found" %
                                   (_get_method_name(command_name),))
        return method(command_name, *args)


def setup_logging(format=None):
    if format is None:
        format='%(asctime)s.%(msecs)03.0f [%(name)-10s:%(lineno)-4s] %(levelname)-7.7s: %(message)s'
    logging.basicConfig(
        format=format,
        datefmt="%H:%M:%S",
#        level=logging.DEBUG
        level=5
    )
