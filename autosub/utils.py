import logging
import re
import socket
import subprocess
from string import capwords
import time
import urllib2
import codecs
import os
import tvdb_api

from library import version

import autosub
from autosub.db import IdCache
from autosub.version import RELEASE_VERSION

log = logging.getLogger(__name__)

LOG_PARSER = re.compile('^((?P<date>\d{4}\-\d{2}\-\d{2})\ (?P<time>\d{2}:\d{2}:\d{2},\d{3}) (?P<loglevel>\w+))',
                        re.IGNORECASE)


def run_cmd(cmd):
    process = subprocess.Popen(cmd,
                               shell=True,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    shell = process.stdout.read()
    shellerr = process.stderr.read()
    process.wait()
    return shell, shellerr


def connect_url(url):
    response = None
    errorcode = None
    socket.setdefaulttimeout(autosub.TIMEOUT)
    try:
        response = urllib2.urlopen(url)
        errorcode = response.getcode()
    except urllib2.HTTPError, e:
        errorcode = e.getcode()

    if errorcode == 200:
        log.debug("API: HTTP Code: 200: OK!")
    else:
        log.error("HTTP Code: %s: NOT OK!" % errorcode)

    return response


def check_version():
    """
    Check version

    Return values:
    0 Same version
    1 New version
    2 New (higher) release, same version
    3 New lower release, higher version
    4 Release lower, version lower
    """
    try:
        req = urllib2.Request(autosub.VERSIONURL)
        req.add_header("User-agent", autosub.USERAGENT)
        resp = urllib2.urlopen(req, None, autosub.TIMEOUT)
        respone = resp.read()
        resp.close()
    except:
        log.error("The server returned an error for request %s" % autosub.VERSIONURL)
        return None
    try:
        match = re.search('(Alpha|Beta|Stable) (\d+)\.(\d+)\.(\d+)', respone)
        version_online = match.group(0)
    except:
        return None

    release = version_online.split(' ')[0]
    versionnumber = version.StrictVersion(version_online.split(' ')[1])

    running_release = RELEASE_VERSION.split(' ')[0]
    running_versionnumber = version.StrictVersion(RELEASE_VERSION.split(' ')[1])

    if release == running_release: #Alpha = Alpha
        if versionnumber > running_versionnumber: #0.5.6 > 0.5.5
            return 1
        else: #0.5.6 = 0.5.6
            return 0
    elif release > running_release: #Beta > Alpha
        if versionnumber == running_versionnumber: #0.5.5 = 0.5.5
            return 2
        elif versionnumber > running_versionnumber: #0.5.6 > 0.5.5
            return 4
    elif release < running_release: #Alpha < Beta
        if versionnumber > running_versionnumber: #0.5.6 > 0.5.5
            return 3


def clean_series_name(series_name):
    """Clean up series name by removing any . and _
    characters, along with any trailing hyphens.

    Is basically equivalent to replacing all _ and . with a
    space, but handles decimal numbers in string, for example:

    >>> clean_series_name("an.example.1.0.test")
    'an example 1.0 test'
    >>> clean_series_name("an_example_1.0_test")
    'an example 1.0 test'

    Stolen from dbr's tvnamer
    """
    try:
        series_name = re.sub("(\D)\.(?!\s)(\D)", "\\1 \\2", series_name)
        series_name = re.sub("(\d)\.(\d{4})", "\\1 \\2", series_name)  # if it ends in a year then don't keep the dot
        series_name = re.sub("(\D)\.(?!\s)", "\\1 ", series_name)
        series_name = re.sub("\.(?!\s)(\D)", " \\1", series_name)
        series_name = series_name.replace("_", " ")
        series_name = re.sub("-$", "", series_name)
        return capwords(series_name.strip())
    except TypeError:
        log.debug("There is no SerieName to clean")


def return_upper(text):
    """
    Return the text converted to uppercase.
    When not possible return nothing.
    """
    try:
        text = text.upper()
        return text
    except:
        pass


def name_mapping(show_name):
    if show_name.upper() in autosub.USERNAMEMAPPINGUPPER.keys():
        log.debug("Found match in user's namemapping for %s" % show_name)
        return autosub.USERNAMEMAPPINGUPPER[show_name.upper()]
    elif show_name.upper() in autosub.NAMEMAPPINGUPPER.keys():
        log.debug("Found match for %s" % show_name)
        return autosub.NAMEMAPPINGUPPER[show_name.upper()]


def skip_show(show_name, season, episode):
    if show_name.upper() in autosub.SKIPSHOWUPPER.keys():
        log.debug("Found %s in skipshow dictonary" % show_name)
        for seasontmp in autosub.SKIPSHOWUPPER[show_name.upper()]:
            if seasontmp == '0':
                log.debug("Variable of %s is set to 0, skipping the complete Serie" % show_name)
                return True
            elif int(seasontmp) == int(season):
                log.debug("Season matches variable of %s, skipping season" % show_name)
                return True


def get_showid(show_name):
    log.debug('trying to get showid for %s' % show_name)
    show_id = name_mapping(show_name)
    if show_id:
        log.debug('showid from namemapping %s' % show_id)
        return int(show_id)

    show_id = IdCache().get_id(show_name)
    if show_id:
        log.debug('showid from cache %s' % show_id)
        if show_id == -1:
            log.error('Showid not found for %s' % show_name)
            return
        return int(show_id)

    # Do we have enough api calls?
    if check_apicalls():
        show = tvdb_api.Tvdb()[show_name]
        if show:
            show_id = show['id']
    else:
        log.warning("Out of API calls")
        return None

    if show_id:
        log.debug('Showid from api %s' % show_id)
        IdCache().set_id(show_id, show_name)
        log.info('%r added to cache with %s' % (show_name, show_id))
        return int(show_id)

    log.error('Showid not found for %s' % show_name)
    IdCache().set_id(-1, show_name)


def check_apicalls(use=False):
    currentime = time.time()
    lastrun = autosub.APICALLSLASTRESET
    interval = autosub.APICALLSRESETINT

    if currentime - lastrun > interval:
        autosub.APICALLS = autosub.APICALLSMAX
        autosub.APICALLSLASTRESET = time.time()

    if autosub.APICALLS > 0:
        if use:
            autosub.APICALLS -= 1
        return True
    else:
        return False


def display_logfile(loglevel):
    max_lines = 500
    data = []
    if os.path.isfile(autosub.LOGFILE):
        f = codecs.open(autosub.LOGFILE, 'r', autosub.SYSENCODING)
        data = f.readlines()
        f.close()

    final_data = []

    num_lines = 0

    for x in reversed(data):
        try:
            matches = LOG_PARSER.search(x)
            matchdic = matches.groupdict()
            if (matchdic['loglevel'] == loglevel.upper()) or (loglevel == ''):
                num_lines += 1
                if num_lines >= max_lines:
                    break
                final_data.append(x)
        except:
            continue
    result = "".join(final_data)
    return result


def convert_timestamp(datestring):
    date_object = time.strptime(datestring, "%Y-%m-%d %H:%M:%S")
    return "%02i-%02i-%i %02i:%02i:%02i " % (
        date_object[2], date_object[1], date_object[0], date_object[3], date_object[4], date_object[5],)


def convert_timestamp_table(datestring):
    #used for the sorted table
    date_object = time.strptime(datestring, "%Y-%m-%d %H:%M:%S")
    return "%04i%02i%02i%02i%02i%02i" % (
        date_object[0], date_object[1], date_object[2], date_object[3], date_object[4], date_object[5])


def check_mobile_device(req_useragent):
    for MUA in autosub.MOBILEUSERAGENTS:
        if MUA.lower() in req_useragent.lower():
            return True
    return False


# Thanks to: http://stackoverflow.com/questions/1088392/sorting-a-python-list-by-key-while-checking-for-string-or-float
def get_attr(name):
    def inner_func(o):
        try:
            rv = float(o[name])
        except ValueError:
            rv = o[name]
        return rv

    return inner_func