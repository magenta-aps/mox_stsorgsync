# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This program is meant to disassemble the log from
os2sync and print the xml in human readble form
"""

import sys
import xmltodict
import pathlib
import io
import re
import collections


def flatten(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def keycleaner(path, key, value):
    return key.split(":")[-1], value


def line_transform(line):
    time, loglevel, action, extra, textpart = (
        "????-??-?? ??:??:??", "LOGLEVL?", "", "", ""
    )
    lineparts = re.split(" (?=\<\?xml)", line)
    if len(lineparts) == 2:
        textpart, xmlpart = lineparts
        try:
            xmldata = xmltodict.parse(
                xmlpart,
                postprocessor=keycleaner,
                process_namespaces=True,
                namespace_separator=':',
                namespaces={}
            )
            xmldata = {
                k.split(".")[-1]: v
                for k, v in flatten(xmldata).items()
            }
            extra = ", ".join(["%s: %r" % item for item in xmldata.items()])
        except:
            extra = (
                "os2sync_log_printer failed on xml on this line: " +
                lineparts[1]
            )
    else:
        textpart = line
    textparts = textpart.split(" - ")
    if len(textparts) > 0:
        time = textparts[0]
    if len(textparts) > 1:
        loglevel = textparts[1].strip().split(" ")[0]
    if len(textparts) > 2:
        action = textparts[2]
    if len(textparts) > 3:
        extra = extra + ", " + textparts[3]
    return "%s %s %s %s" % (time, loglevel, action, extra)


def file_transform(log):

    # log is an open file?
    if isinstance(log, io.IOBase):
        pass

    # filename? open it
    elif (
        isinstance(log, str) and
        pathlib.Path(log).exists()
    ):
        log = open(log, 'r')

    # no? log must be a string
    else:
        log = io.StringIO(log)

    for line in log:
        print(line_transform(line))


def main():
    if len(sys.argv) > 1:
        log = sys.argv[1]
    else:
        log = "/var/log/os2sync/service.log"
    file_transform(log)


if __name__ == "__main__":
    main()
