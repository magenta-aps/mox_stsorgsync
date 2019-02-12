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
os2mo_headers = {
    "SESSION": settings["OS2MO_SAML_TOKEN"]
}


def os2mo_url(url):
    """format url like {BASE}/o/{ORG}/e
    """
    url = url.format(
        BASE=settings["OS2MO_SERVICE_URL"],
        ORG=settings["OS2MO_ORG_UUID"],
    )
    return url


def os2mo_get(url, **params):
    url = os2mo_url(url)
    try:
        r = requests.get(
            url,
            headers=os2mo_headers,
            params=params,
            verify=settings["OS2MO_CA_BUNDLE"]
        )
        r.raise_for_status()
        return r
    except Exception:
        logger.exception(url)
        raise


def user_uuids():
    return [e["uuid"] for e in os2mo_get("{BASE}/o/{ORG}/e").json()["items"]]


def addresses_to_user(user, addresses):
    for a in addresses:
        if a['address_type']['scope'] == "EMAIL":
            user["Email"] = {"Value": a["name"], "Uuid": a["uuid"]}
        if a['address_type']['scope'] == "PHONE":
            user["Phone"] = {"Value": a["name"], "Uuid": a["uuid"]}
        if a['address_type']['scope'] == "DAR":
            user["Location"] = {"Value": a["name"], "Uuid": a["uuid"]}


def engagements_to_user(user, engagements):
    for e in engagements:
        user["Positions"].append({
            "OrgUnitUuid": e["org_unit"]["uuid"],
            "Name": e["job_function"]["name"],
            "Uuid": e["uuid"],
        })


def get_sts_user(uuid):
    base = os2mo_get("{BASE}/e/" + uuid + "/").json()
    sts_user = {
      "Uuid": uuid,
      "UserId": uuid,
      "Positions": [],
      "Person": {
        "Name": base["name"],
        "Uuid": uuid,
      }
    }
    addresses_to_user(
        sts_user,
        os2mo_get("{BASE}/e/" + uuid + "/details/address").json()
    )
    engagements_to_user(
        sts_user,
        os2mo_get("{BASE}/e/" + uuid + "/details/engagement").json()
    )
    return sts_user


def org_unit_uuids():
    return [e["uuid"] for e in os2mo_get("{BASE}/o/{ORG}/ou").json()["items"]]


def itsystems_to_orgunit(orgunit, itsystems):
    for i in itsystems:
        orgunit["ItSystemUuids"].append(i["itsystem"]["uuid"])


def addresses_to_orgunit(orgunit, addresses):
    for a in addresses:
        if a['address_type']['scope'] == "EMAIL":
            orgunit["Email"] = {"Value": a["name"], "Uuid": a["uuid"]}
        elif a['address_type']['scope'] == "PHONE":
            orgunit["Phone"] = {"Value": a["name"], "Uuid": a["uuid"]}
        elif a['address_type']['scope'] == "DAR":
            orgunit["Post"] = {"Value": a["value"], "Uuid": a["uuid"]}
            orgunit["Location"] = {"Value": a["name"], "Uuid": a["uuid"]}


def get_sts_orgunit(uuid):
    base = os2mo_get("{BASE}/ou/" + uuid + "/").json()
    sts_org_unit = {
        'Contact': {'ShortKey': None, 'Uuid': None, 'Value': None},
        'ContactOpenHours': {'ShortKey': None, 'Uuid': None, 'Value': None},
        'ContactPlaces': [{'OrgUnitUuid': None, 'Tasks': []}],
        'Ean': {'ShortKey': None, 'Uuid': None, 'Value': None},
        'Email': {'ShortKey': None, 'Uuid': None, 'Value': None},
        'EmailRemarks': {'ShortKey': None, 'Uuid': None, 'Value': None},
        'ItSystemUuids': [],
        'LOSShortName': {'ShortKey': None, 'Uuid': None, 'Value': None},
        'Location': {'ShortKey': None, 'Uuid': None, 'Value': None},
        'Name': base["name"],
        'ParentOrgUnitUuid': None,  # most should have
        'PayoutUnitUuid': None,
        'Phone': {'ShortKey': None, 'Uuid': None, 'Value': None},
        'PhoneOpenHours': {'ShortKey': None, 'Uuid': None, 'Value': None},
        'Post': {'ShortKey': None, 'Uuid': None, 'Value': None},
        'PostReturn': {'ShortKey': None, 'Uuid': None, 'Value': None},
        'Uuid': uuid,
    }

    if base.get("parent") and 'uuid' in base["parent"]:
        sts_org_unit["ParentOrgUnitUuid"] = base["parent"]["uuid"]

    itsystems_to_orgunit(
        sts_org_unit,
        os2mo_get("{BASE}/ou/" + uuid + "/details/it").json()
    )
    addresses_to_orgunit(
        sts_org_unit,
        os2mo_get("{BASE}/ou/" + uuid + "/details/address").json()
    )

    import pprint; pprint.pprint(sts_org_unit)
