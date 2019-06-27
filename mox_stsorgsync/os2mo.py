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
session.verify = settings["OS2MO_CA_BUNDLE"]
session.headers = {
    "SESSION": settings["OS2MO_SAML_TOKEN"],
    "User-Agent": "mox_stsorgsync/0.1",
}
TRUNCATE_LENGTH = max(36, int(settings.get("STSORGSYNC_TRUNCATE", 200)))


# truncate and warn all strings in dictionary,
# ensure not shortening uuids
def strip_truncate_and_warn(d, root, length=TRUNCATE_LENGTH):
    for k, v in list(d.items()):
        if isinstance(v, dict):
            strip_truncate_and_warn(v, root)
        elif isinstance(v, str):
            v = d[k] = v.strip()
            if len(v) > length:
                v = d[k] = v[:length]
                logger.warning(
                    "truncating to %d key '%s' for"
                    " uuid '%s' to value '%s'",
                    length,
                    k,
                    root["Uuid"],
                    v
                )


def os2mo_url(url):
    """format url like {BASE}/o/{ORG}/e
    """
    url = url.format(
        BASE=settings["OS2MO_SERVICE_URL"], ORG=settings["OS2MO_ORG_UUID"]
    )
    return url


def os2mo_get(url, **params):
    url = os2mo_url(url)
    try:
        r = session.get(url, params=params)
        r.raise_for_status()
        return r
    except Exception:
        logger.exception(url)
        raise


def user_uuids():
    return [
        e["uuid"]
        for e in os2mo_get("{BASE}/o/{ORG}/e/", limit=100000).json()["items"]
    ]


def addresses_to_user(user, addresses):
    for a in addresses:
        if a["address_type"]["scope"] == "EMAIL":
            user["Email"] = {"Value": a["name"], "Uuid": a["uuid"]}
        if a["address_type"]["scope"] == "PHONE":
            user["Phone"] = {"Value": a["name"], "Uuid": a["uuid"]}
        if a["address_type"]["scope"] == "DAR":
            user["Location"] = {"Value": a["name"], "Uuid": a["uuid"]}


def engagements_to_user(user, engagements, allowed_unitids):
    for e in engagements:
        if e["org_unit"]["uuid"] in allowed_unitids:
            user["Positions"].append(
                {
                    "OrgUnitUuid": e["org_unit"]["uuid"],
                    "Name": e["job_function"]["name"],
                    "Uuid": e["uuid"],
                }
            )


def get_sts_user(uuid, allowed_unitids):
    base = os2mo_get("{BASE}/e/" + uuid + "/").json()
    sts_user = {
        "Uuid": uuid,
        "UserId": uuid,
        "Positions": [],
        "Person": {"Name": base["name"], "Uuid": uuid},
    }
    addresses_to_user(
        sts_user, os2mo_get("{BASE}/e/" + uuid + "/details/address").json()
    )
    engagements_to_user(
        sts_user,
        os2mo_get("{BASE}/e/" + uuid + "/details/engagement").json(),
        allowed_unitids
    )
    # show_all_details(uuid,"e")
    strip_truncate_and_warn(sts_user, sts_user)
    return sts_user


def org_unit_uuids():
    return [
        e["uuid"]
        for e in os2mo_get("{BASE}/o/{ORG}/ou", limit=100000).json()["items"]
    ]


def itsystems_to_orgunit(orgunit, itsystems):
    for i in itsystems:
        orgunit["ItSystemUuids"].append(i["itsystem"]["uuid"])


def addresses_to_orgunit(orgunit, addresses):
    for a in addresses:
        if a["address_type"]["scope"] == "EMAIL":
            orgunit["Email"] = {"Value": a["name"], "Uuid": a["uuid"]}
        elif a["address_type"]["scope"] == "PNUMBER":
            orgunit["Ean"] = {"Value": a["name"], "Uuid": a["uuid"]}
        elif a["address_type"]["scope"] == "PHONE":
            orgunit["Phone"] = {"Value": a["name"], "Uuid": a["uuid"]}
        elif a["address_type"]["scope"] == "DAR":
            orgunit["Post"] = {"Value": a["value"], "Uuid": a["uuid"]}
        elif a["address_type"]["scope"] == "TEXT":
            orgunit["Location"] = {"Value": a["name"], "Uuid": a["uuid"]}


def get_sts_orgunit(uuid):
    base = parent = os2mo_get("{BASE}/ou/" + uuid + "/").json()

    if not parent["uuid"] == settings["OS2MO_TOP_UNIT_UUID"]:
        while parent.get("parent"):
            if parent["uuid"] == settings["OS2MO_TOP_UNIT_UUID"]:
                break
            parent = parent["parent"]

    if not parent["uuid"] == settings["OS2MO_TOP_UNIT_UUID"]:
        # not part of right tree
        return None

    sts_org_unit = {"ItSystemUuids": [], "Name": base["name"], "Uuid": uuid}

    if base.get("parent") and "uuid" in base["parent"]:
        sts_org_unit["ParentOrgUnitUuid"] = base["parent"]["uuid"]

    itsystems_to_orgunit(
        sts_org_unit, os2mo_get("{BASE}/ou/" + uuid + "/details/it").json()
    )
    addresses_to_orgunit(
        sts_org_unit,
        os2mo_get("{BASE}/ou/" + uuid + "/details/address").json(),
    )

    # show_all_details(uuid,"ou")
    strip_truncate_and_warn(sts_org_unit, sts_org_unit)
    return sts_org_unit


def show_all_details(uuid, objtyp):
    import pprint

    print(" ---- details ----\n")
    for d, has_detail in (
        os2mo_get("{BASE}/" + objtyp + "/" + uuid + "/details").json().items()
    ):
        if has_detail:
            print("------------ detail ---- " + d)
            pprint.pprint(
                os2mo_get(
                    "{BASE}/" + objtyp + "/" + uuid + "/details/" + d
                ).json()
            )
    print(" ---- end of details ----\n")
