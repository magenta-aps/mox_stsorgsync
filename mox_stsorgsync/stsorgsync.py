# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
import logging
from mox_stsorgsync.config import settings


logger = logging.getLogger("mox_stsorgsync")

session = requests.Session()
session.verify = settings["STSORGSYNC_CA_BUNDLE"]

session.headers = {
    "User-Agent": "mox_stsorgsync/0.1",
    "CVR":settings["STSORGSYNC_MUNICIPALITY"]
}


def stsorgsync_url(url):
    """format url like {BASE}/user
    """
    url = url.format(BASE=settings["STSORGSYNC_API_URL"])
    return url


def stsorgsync_get(url, **params):
    url = stsorgsync_url(url)
    try:
        r = session.get(url, params=params)
        r.raise_for_status()
        return r
    except Exception:
        logger.error(url + " " + r.text)
        logger.exception("")
        raise


def stsorgsync_delete(url, **params):
    url = stsorgsync_url(url)
    try:
        r = session.delete(url, **params)
        r.raise_for_status()
        return r
    except Exception:
        logger.error(url + " " + r.text)
        logger.exception("")
        raise


def stsorgsync_post(url, **params):
    url = stsorgsync_url(url)
    try:
        r = session.post(url, **params)
        r.raise_for_status()
        return r
    except Exception:
        logger.error(url + " " + r.text)
        logger.exception("")
        raise


def user_uuids():
    return stsorgsync_get("{BASE}/user").json()


def delete_user(uuid):
    logger.info("delete user %s", uuid)
    stsorgsync_delete("{BASE}/user/" +uuid)


def upsert_user(user):
    logger.info("upsert user %s", user["Uuid"])
    stsorgsync_post("{BASE}/user", json=user)


def orgunit_uuids():
    return stsorgsync_get("{BASE}/orgunit").json()


def delete_orgunit(uuid):
    logger.info("delete orgunit %s", uuid)
    stsorgsync_delete("{BASE}/orgunit/" + uuid)


def upsert_orgunit(org_unit):
    logger.info("upsert orgunit %s", org_unit["Uuid"])
    stsorgsync_post("{BASE}/orgunit/", json=org_unit)
