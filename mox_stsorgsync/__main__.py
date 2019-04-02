# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
from mox_stsorgsync import os2mo, stsorgsync, config


settings = config.settings

# set warning-level for all loggers
[
    logging.getLogger(i).setLevel(logging.WARNING)
    for i in logging.root.manager.loggerDict
]

logging.basicConfig(
    level=int(settings["MOX_LOG_LEVEL"]), filename=settings["MOX_LOG_FILE"]
)
logger = logging.getLogger("mox_stsorgsync")
logger.setLevel(int(settings["MOX_LOG_LEVEL"]))


def sync_stsorgsync_orgunits():
    os2mo_uuids = set(os2mo.org_unit_uuids())
    stsorgsync_uuids = set(stsorgsync.orgunit_uuids())

    # delete from stsorgsync what is not in os2mo
    if len(os2mo_uuids):
        for uuid in set(stsorgsync_uuids - os2mo_uuids):
            stsorgsync.delete_orgunit(uuid)

    for i in os2mo_uuids:
        sts_orgunit = os2mo.get_sts_orgunit(i)
        stsorgsync.upsert_orgunit(sts_orgunit)


def sync_stsorgsync_users():
    stsorgsync_uuids = set(stsorgsync.user_uuids())
    os2mo_uuids = set(os2mo.user_uuids())

    # delete from stsorgsync what is not in os2mo
    if len(os2mo_uuids):
        for uuid in set(stsorgsync_uuids - os2mo_uuids):
            stsorgsync.delete_user(uuid)

    # insert/overwrite all users from  os2mo
    for i in os2mo_uuids:
        sts_user = os2mo.get_sts_user(i)
        stsorgsync.upsert_user(sts_user)


if __name__ == "__main__":
    if not settings["OS2MO_ORG_UUID"]:
        settings["OS2MO_ORG_UUID"] = os2mo.os2mo_get("{BASE}/o/").json()[0][
            "uuid"
        ]
    sync_stsorgsync_orgunits()
    sync_stsorgsync_users()
