# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
from mox_stsorgsync import os2mo, stsorgsync, config
import collections
import argparse

# set warning-level for all loggers
[
    logging.getLogger(name).setLevel(logging.WARNING)
    for name in logging.root.manager.loggerDict
    if name != config.loggername
]

settings = config.settings
logging.basicConfig(
    format='%(levelname)s %(asctime)s %(name)s %(message)s',
    level=int(settings["MOX_LOG_LEVEL"]),
    filename=settings["MOX_LOG_FILE"]
)
logger = logging.getLogger(config.loggername)
logger.setLevel(int(settings["MOX_LOG_LEVEL"]))


def log_mox_config():
    """It is imperative for log-forensics to have as
    much configuration as possible logged at program start
    and end.
    """
    secrets = ["OS2MO_SAML_TOKEN"]
    logger.warning("-----------------------------------------")
    logger.warning("program configuration:")
    for k, v in sorted(settings.items()):
        if k in secrets:
            logger.warning("    %s=********", k)
        else:
            logger.warning("    %s=%r", k, v)


def log_mox_counters(counter):
    logger.info("-----------------------------------------")
    logger.info("program counters:")
    for k, v in sorted(counter.items()):
        logger.info("    %s: %r", k, v)


def sync_stsorgsync_orgunits(counter, cherrypicked=[]):
    logger.info("sync_stsorgsync_orgunits starting")

    if cherrypicked:
        logger.info("sync_stsorgsync_orgunits getting "
                    "cherrypicked organisational units from os2mo")
        os2mo_uuids = set(os2mo.pruned_tree(cherrypicked))
    else:
        logger.info("sync_stsorgsync_orgunits getting "
                    "all organisational units from os2mo")
        os2mo_uuids = set(os2mo.org_unit_uuids())

    counter["Orgenheder fundet i OS2MO"] = len(os2mo_uuids)

    logger.info("sync_stsorgsync_orgunits getting all "
                "organisational units from stsorgsync")

    if cherrypicked:
        logger.info("No deletion of organisational units attempted in "
                    "os2sync when cherrypicking")
    else:
        stsorgsync_uuids = set(stsorgsync.orgunit_uuids())
        counter["Orgenheder fundet i OS2Sync"] = len(stsorgsync_uuids)

        logger.info("sync_stsorgsync_orgunits deleting organisational "
                    "units from stsorgsync if deleted in os2mo")
        if len(os2mo_uuids):
            for uuid in set(stsorgsync_uuids - os2mo_uuids):
                counter["Orgenheder som slettes i OS2Sync"] += 1
                stsorgsync.delete_orgunit(uuid)

    logger.info("sync_stsorgsync_orgunits upserting "
                "organisational units in stsorgsync")

    allowed_unitids = []
    for i in os2mo_uuids:
        sts_orgunit = os2mo.get_sts_orgunit(i)
        if sts_orgunit:
            allowed_unitids.append(i)
            counter["Orgenheder som opdateres i OS2Sync"] += 1
            stsorgsync.upsert_orgunit(sts_orgunit)

    logger.info("sync_stsorgsync_orgunits done")

    return set(allowed_unitids)


def sync_stsorgsync_users(allowed_unitids, counter):
    logger.info("sync_stsorgsync_users starting")
    logger.info("sync_stsorgsync_users getting list "
                "of users from stsorgsync")

    stsorgsync_uuids = set(stsorgsync.user_uuids())
    counter["Medarbejdere fundet i OS2Sync"] = len(stsorgsync_uuids)

    logger.info("sync_stsorgsync_users getting list of users from os2mo")

    os2mo_uuids = set(os2mo.user_uuids())
    counter["Medarbejdere fundet i OS2MO"] = len(os2mo_uuids)

    logger.info("sync_stsorgsync_users deleting "
                "os2mo-deleted users in stsorgsync")

    if len(os2mo_uuids):
        for uuid in set(stsorgsync_uuids - os2mo_uuids):
            counter["Medarbejdere slettes i OS2Sync (del)"] += 1
            stsorgsync.delete_user(uuid)

    # insert/overwrite all users from os2mo
    # delete if user has no more positions
    logger.info("sync_stsorgsync_users upserting stsorgsync users")

    for i in os2mo_uuids:
        sts_user = os2mo.get_sts_user(i, allowed_unitids)

        if not sts_user["Positions"]:
            if i in stsorgsync_uuids:
                counter["Medarbejdere slettes i OS2Sync (pos)"] += 1
                stsorgsync.delete_user(i)
            continue

        stsorgsync.upsert_user(sts_user)
        counter["Medarbejdere overført til OS2SYNC"] += 1

    logger.info("sync_stsorgsync_users done")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Mox Stsorgsync')
    parser.add_argument('--cherrypick', dest='cherrypick', action='append',
                        nargs='+', help='add cherrypicked ou uuids one by one')
    args = vars(parser.parse_args())
    counter = collections.Counter()
    logger.info("mox_stsorgsync starting")
    log_mox_config()
    if not settings["OS2MO_ORG_UUID"]:
        settings["OS2MO_ORG_UUID"] = os2mo.os2mo_get("{BASE}/o/").json()[0][
            "uuid"
        ]
    if args["cherrypick"]:
        orgunit_uuids = sync_stsorgsync_orgunits(counter,
                                                 args["cherrypick"][0])
    else:
        orgunit_uuids = sync_stsorgsync_orgunits(counter)
    sync_stsorgsync_users(orgunit_uuids, counter)
    log_mox_counters(counter)
    log_mox_config()
    logger.info("mox_stsorgsync done")
