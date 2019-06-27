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
    format='%(levelname)s %(asctime)s %(name)s %(message)s',
    level=int(settings["MOX_LOG_LEVEL"]),
    filename=settings["MOX_LOG_FILE"]
)
logger = logging.getLogger("mox_stsorgsync")
logger.setLevel(int(settings["MOX_LOG_LEVEL"]))


def sync_stsorgsync_orgunits():
    logger.info("sync_stsorgsync_orgunits starting")
    logger.info("sync_stsorgsync_orgunits getting "
                "all organisational units from os2mo")
    os2mo_uuids = set(os2mo.org_unit_uuids())

    logger.info("sync_stsorgsync_orgunits getting all "
                "organisational units from stsorgsync")

    stsorgsync_uuids = set(stsorgsync.orgunit_uuids())

    # delete from stsorgsync what is not in os2mo

    logger.info("sync_stsorgsync_orgunits deleting organisational "
                "units from stsorgsync if deleted in os2mo")

    if len(os2mo_uuids):
        for uuid in set(stsorgsync_uuids - os2mo_uuids):
            stsorgsync.delete_orgunit(uuid)

    logger.info("sync_stsorgsync_orgunits upserting "
                "organisational units in stsorgsync")

    allowed_unitids = []
    for i in os2mo_uuids:
        sts_orgunit = os2mo.get_sts_orgunit(i)
        if sts_orgunit:
            allowed_unitids.append(i)
            stsorgsync.upsert_orgunit(sts_orgunit)

    logger.info("sync_stsorgsync_orgunits done")

    return set(allowed_unitids)


def sync_stsorgsync_users(allowed_unitids):
    logger.info("sync_stsorgsync_users starting")
    logger.info("sync_stsorgsync_users getting list "
                "of users from stsorgsync")

    stsorgsync_uuids = set(stsorgsync.user_uuids())

    logger.info("sync_stsorgsync_users getting list of users from os2mo")

    os2mo_uuids = set(os2mo.user_uuids())

    logger.info("sync_stsorgsync_users deleting "
                "os2mo-deleted users in stsorgsync")

    if len(os2mo_uuids):
        for uuid in set(stsorgsync_uuids - os2mo_uuids):
            stsorgsync.delete_user(uuid)

    # insert/overwrite all users from os2mo
    # delete if user has no more positions
    logger.info("sync_stsorgsync_users upserting stsorgsync users")

    for i in os2mo_uuids:
        sts_user = os2mo.get_sts_user(i, allowed_unitids)

        if not sts_user["Positions"]:
            if i in stsorgsync_uuids:
                stsorgsync.delete_user(i)
            continue

        stsorgsync.upsert_user(sts_user)

    logger.info("sync_stsorgsync_users done")


if __name__ == "__main__":
    logger.info("mox_stsorgsync starting")
    if not settings["OS2MO_ORG_UUID"]:
        settings["OS2MO_ORG_UUID"] = os2mo.os2mo_get("{BASE}/o/").json()[0][
            "uuid"
        ]
    orgunit_uuids = sync_stsorgsync_orgunits()
    sync_stsorgsync_users(orgunit_uuids)
    logger.info("mox_stsorgsync done")
