# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import json
from mox_stsorgsync import stsorgsync, config, __main__ as mox
import collections
import pathlib
import time

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


def delete_stsorgsync_users(donefile="./delete_stsorgsync_users.json"):
    done = {}
    deljson = pathlib.Path(donefile)
    if deljson.exists():
        done.update(json.loads(deljson.read_text()))
    deljson.write_text(json.dumps(done))
    while True:
        stsorgsync_uuids = set(stsorgsync.user_uuids())
        if not len(stsorgsync_uuids):
            break
        for uuid in stsorgsync_uuids:
            if uuid in done:
                continue
            logger.info("deleting: %s", uuid)
            stsorgsync.delete_user(uuid)
            done[uuid] = True
        deljson.write_text(json.dumps(done))
        time.sleep(450)


if __name__ == "__main__":
    counter = collections.Counter()
    logger.info("delete users starting")
    mox.log_mox_config()

    delete_stsorgsync_users()
    mox.log_mox_counters(counter)
