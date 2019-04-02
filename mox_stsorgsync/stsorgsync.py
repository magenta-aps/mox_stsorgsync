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


def stsorgsync_url(url):
    """format url like {BASE}/user
    """
    url = url.format(BASE=settings["STSORGSYNC_API_URL"])
    return url


def stsorgsync_get(url, **params):
    url = stsorgsync_url(url)
    try:
        r = requests.get(
            url, params=params, verify=settings["STSORGSYNC_CA_BUNDLE"]
        )
        r.raise_for_status()
        return r
    except Exception:
        logger.exception(url)
        raise


def stsorgsync_delete(url, **params):
    url = stsorgsync_url(url)
    try:
        r = requests.delete(
            url, **params, verify=settings["STSORGSYNC_CA_BUNDLE"]
        )
        r.raise_for_status()
        return r
    except Exception:
        logger.exception(url)
        raise


def stsorgsync_post(url, **params):
    url = stsorgsync_url(url)
    try:
        r = requests.post(
            url, **params, verify=settings["STSORGSYNC_CA_BUNDLE"]
        )
        r.raise_for_status()
        return r
    except Exception:
        logger.exception(url)
        raise


def user_uuids():
    return stsorgsync_get("{BASE}/user").json()


def delete_user(uuid):
    logger.info("delete user %s", uuid)
    stsorgsync_delete("{BASE}/user", params={"uuid": uuid})


def upsert_user(user):
    logger.info("upsert user %s", user["Uuid"])
    stsorgsync_post("{BASE}/user", json=user)


def orgunit_uuids():
    return stsorgsync_get("{BASE}/orgunit").json()


def delete_orgunit(uuid):
    logger.info("delete orgunit %s", uuid)
    stsorgsync_delete("{BASE}/orgunit", params={"uuid": uuid})


def upsert_orgunit(org_unit):
    logger.info("upsert orgunit %s", org_unit["Uuid"])
    stsorgsync_post("{BASE}/orgunit", json=org_unit)
