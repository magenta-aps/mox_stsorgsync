""# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import datetime
import logging
from mox_stsorgsync import os2mo, stsorgsync, config

settings=config.settings

# set warning-level for all loggers
[
    logging.getLogger(i).setLevel(logging.WARNING)
    for i in logging.root.manager.loggerDict
]

logging.basicConfig(level=int(settings["MOX_LOG_LEVEL"]),
                    filename=settings["MOX_LOG_FILE"])

logger = logging.getLogger("mox_stsorgsync")


def upsert_stsorgsync_orgunits():
    os2mo_uuids = os2mo.org_unit_uuids()
    for i in os2mo_uuids:
        sts_org_unit = os2mo.get_sts_orgunit(i)
        errs = []
        # check for required attributes
        # stsorgsync.upsert_org_unit(sts_user)


def upsert_stsorgsync_users():
    os2mo_uuids = os2mo.user_uuids()
    for i in os2mo_uuids:
        sts_user = os2mo.get_sts_user(i)
        errs = []
        # check for required attributes
        if not len(sts_user["Positions"]):
            errs.append("No positions")
        if not sts_user.get("Location"):
            errs.append("No Location")
        if not sts_user.get("Email"):
            errs.append("No Email")
        if len(errs):
            logger.warning("Skipping user: %s because %r", i, errs)
            continue
        stsorgsync.upsert_user(sts_user)

if __name__ == "__main__":
    upsert_stsorgsync_orgunits()
    #upsert_stsorgsync_users()

