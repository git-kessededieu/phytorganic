import re
import time
import unicodedata
from datetime import datetime, timedelta

from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.filter(name = 'get_label')
def get_label(status, label_name = None, class_name = None):
    result = {
        -1: {label_name: 'Rejeté', class_name: 'danger'},
        0: {label_name: 'En attente', class_name: 'primary'},
        1: {label_name: 'Validé', class_name: 'success'}
    }[status]

    return result, label_name


@register.filter()
def to_int(value):
    return int(value)


@register.filter(name = 'link_name')
def link_name(path, page_number):
    output = re.search('(page=\d+)', path)
    if output is not None:
        # print(str(output.group(1)))
        return path.replace(str(output.group(1)), "page={}".format(page_number))
    if re.search('(page=\d+)', path):
        path.replace()
    page_number = str(page_number)
    if '?' in path:
        return path + "&page=" + page_number
    return path + "?page=" + page_number


@register.filter(name = 'proper_paginate')
def proper_paginate(paginator, current_page, neighbors = 2):
    if paginator.num_pages > 2 * neighbors:
        start_index = max(1, current_page - neighbors)
        end_index = min(paginator.num_pages, current_page + neighbors)
        if end_index < start_index + 2 * neighbors:
            end_index = start_index + 2 * neighbors
        elif start_index > end_index - 2 * neighbors:
            start_index = end_index - 2 * neighbors
        if start_index < 1:
            end_index -= start_index
            start_index = 1
        elif end_index > paginator.num_pages:
            start_index -= (end_index - paginator.num_pages)
            end_index = paginator.num_pages
        page_list = [f for f in range(start_index, end_index + 1)]
        return page_list[:(2 * neighbors + 1)]
    return paginator.page_range


@register.filter(name = 'from_unix')
def from_unix(value):
    return datetime.datetime.fromtimestamp(int(value))


@register.filter(name = 'to_date')
def to_date(value):
    if len(value) > 19:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f+00:00')
    return datetime.strptime(value + ".000000", '%Y-%m-%d %H:%M:%S.%f')


@register.filter(name = 'print_timestamp')
def print_timestamp(timestamp):
    try:
        # assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp)
    except ValueError:
        return None
    # specify format here
    # return datetime.datetime.fromtimestamp(ts)
    return time.strftime("%Y-%m-%d", time.gmtime(ts))


@register.filter(name = 'from_timestamp')
def from_timestamp(timestamp):
    try:
        # assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp)
        if timestamp < 0:
            the_date = datetime(1970, 1, 1) + timedelta(seconds = ts / 1000.0)
        else:
            the_date = datetime.fromtimestamp(ts / 1000.0)
    except ValueError:
        return None
    return the_date.strftime('%Y-%m-%d')


@register.simple_tag
def to_plural(n_str, singular, plural = None):
    """ A better pluralization template tag.
        The syntax is ``{% plural number "singular" "plural" %}``, where the
        ``plural`` is optional (the ``singular`` with an ``"s"`` suffix
        will be used if none is provided).
        By default numbers will be formatted using the ``{:,}`` formatter, so
        they will include a comma: ``1,234,567``.
        If the ``singular`` and ``plural`` strings can contain a ``{``, they
        will be treated as ``str.format`` templates::

            > There {% plural cats|length "is {} cat" "are {} cats" %}.
            There is 1 cat.
            > There {% plural dogs|length "is {} dog" "are {} dogs" %}.
            There are 4 dogs.
        Unlike Django's ``pluralize`` filter, ``plural`` does *not* take the
        length of lists; the ``|length`` filter can be used instead::
            > You have {% friends "friend" %}.
            You have ['Alex'] friends.
            > You have {% friends|length "friend" %}.
            You have 1 friend.
        Examples::
            > I have {% plural dog_count "dog" %}.
            I have 3 dogs.
            > You have {% plural ox_count "ox" "oxen" %}
            You have 1 ox.
            > There {% plural cats|length "is {} cat" "are {} cats" %}!
            There are 16 cats!
            > The plural will save you {% plural hours "hour" %}.
            The plural tag will save you 12,345 hours.
        """

    try:
        n = int(n_str)
    except (TypeError, ValueError):
        n = None

    if plural is None:
        plural = singular + u"s"

    formatstr = singular if n == 1 else plural
    if "{" not in formatstr:
        default_format = u"{:,} " if n is not None else u"{} "
        formatstr = default_format + formatstr

    return formatstr.format(n_str)


@register.filter(name = 'get_rate')
def get_rate(total = None, value = None):
    return round((value / total) * 100, 2)


@register.simple_tag
def get_user_infos(username):
    try:
        return User.objects.get(username = username)
    except User.DoesNotExist:
        return 'Unknown'


@register.filter
def null_value(value = ''):
    if value.lower() == 'null':
        return None
    return value


@register.filter
def in_list(value, the_list):
    value = str(value)
    return value in the_list.split(',')


@register.filter
def dateuntil(date):
    d0 = datetime.now().date()
    d1 = date.date()
    delta = d0 - d1
    return delta.days


@register.filter
def remove_accents(s):
    return unicodedata.normalize('NFD', s).encode('ascii', 'ignore')


@register.filter
def index(_list, i):
    return _list[int(i)]
