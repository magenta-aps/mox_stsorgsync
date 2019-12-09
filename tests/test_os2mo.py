# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import unittest
os.environ["STSORGSYNC_PHONE_SCOPE_CLASSES"] = " 1 2 "
from mox_stsorgsync import os2mo  # noqa
initial_settings = dict(os2mo.settings)


class Tests(unittest.TestCase):

    def test_env_vs_config(self):
        self.assertEqual(
            initial_settings["STSORGSYNC_PHONE_SCOPE_CLASSES"],
            ["1", "2"]
        )

    def test_os2mo_url(self):
        self.assertTrue(os2mo.os2mo_url("{BASE}").endswith("service"))

    def test_addresses_to_user_dar(self):
        user = {}
        os2mo.addresses_to_user(user, [
            {'address_type': {'scope': "DAR"}, 'name': 'ABC', 'uuid': "XYZ"}
        ])
        self.assertEqual(user, {'Location': {'Uuid': 'XYZ', 'Value': 'ABC'}})

    def test_secondary_address_when_first_is_secret(self):
        "only the classes given are chosen and only of PUBLIC or no visibility"
        user = {}
        os2mo.settings["STSORGSYNC_PHONE_SCOPE_CLASSES"] = [
            "42-42-42-42",
            "10-10-10-10"
        ]
        os2mo.addresses_to_user(user, [
            {'address_type': {'scope': "PHONE", "uuid": "42-42-42-42"},
             'visibility': {"scope": "SECRET"},  # OBSERVE RESULT
             'name': '1234512345', 'uuid': "XYZ"},
            {'address_type': {'scope': "PHONE", "uuid": "10-10-10-10"},
             'visibility': {"scope": "PUBLIC"},
             'name': '2234512345', 'uuid': "XYZ"}
        ])
        self.assertEqual(user, {'Phone': {'Uuid': 'XYZ',
                                          'Value': '2234512345'}})

    def test_chose_according_to_scoped_classes(self):
        user = {}
        os2mo.settings["STSORGSYNC_PHONE_SCOPE_CLASSES"] = [
            "42-42-42-42",
            "10-10-10-10"
        ]
        os2mo.addresses_to_user(user, [
            {'address_type': {'scope': "PHONE", "uuid": "10-10-10-10"},
             'visibility': {"scope": "PUBLIC"},
             'name': '2234512345', 'uuid': "XYZ"},
            {'address_type': {'scope': "PHONE", "uuid": "42-42-42-42"},
             'visibility': {"scope": "PUBLIC"},
             'name': '1234512345', 'uuid': "XYZ"}
        ])
        self.assertEqual(user, {'Phone': {'Uuid': 'XYZ',
                                          'Value': '1234512345'}})

    def test_no_phone_when_scoped_classes_are_not_found(self):
        os2mo.settings["STSORGSYNC_PHONE_SCOPE_CLASSES"] = [
            "42-42-42-42",
            "10-10-10-10"
        ]
        user = {}
        os2mo.addresses_to_user(user, [
            {'address_type': {'scope': "PHONE", "uuid": "11-10-10-10"},
             'visibility': {"scope": "PUBLIC"},
             'name': '2234512345', 'uuid': "XYZ"},
            {'address_type': {'scope': "PHONE", "uuid": "41-42-42-42"},
             'visibility': {"scope": "PUBLIC"},
             'name': '1234512345', 'uuid': "XYZ"}
        ])
        self.assertEqual(user, {})

    def test_no_phone_class_take_last(self):
        "no classes given - take last phone number"
        user = {}
        os2mo.settings["STSORGSYNC_PHONE_SCOPE_CLASSES"] = []
        os2mo.addresses_to_user(user, [
            {'address_type': {'scope': "PHONE", "uuid": "42-42-42-42"},
             'visibility': {"scope": "PUBLIC"},
             'name': '1234512345', 'uuid': "XYZ"},
            {'address_type': {'scope': "PHONE", "uuid": "10-10-10-10"},
             'visibility': {"scope": "PUBLIC"},
             'name': '2234512345', 'uuid': "XYZ"}
        ])
        self.assertEqual(user, {'Phone': {'Uuid': 'XYZ',
                                          'Value': '2234512345'}})

        user = {}
        os2mo.addresses_to_user(user, [
            {'address_type': {'scope': "PHONE", "uuid": "10-10-10-10"},
             'visibility': {"scope": "PUBLIC"},
             'name': '2234512345', 'uuid': "XYZ"},
            {'address_type': {'scope': "PHONE", "uuid": "42-42-42-42"},
             'visibility': {"scope": "PUBLIC"},
             'name': '1234512345', 'uuid': "XYZ"}
        ])
        self.assertEqual(user, {'Phone': {'Uuid': 'XYZ',
                                          'Value': '1234512345'}})

    def test_no_phone_class_all_secret(self):
        "no classes given - take last phone number"
        user = {}
        os2mo.settings["STSORGSYNC_PHONE_SCOPE_CLASSES"] = []
        os2mo.addresses_to_user(user, [
            {'address_type': {'scope': "PHONE", "uuid": "42-42-42-42"},
             'visibility': {"scope": "SECRET"},  # OBSERVE RESULT
             'name': '1234512345', 'uuid': "XYZ"},
            {'address_type': {'scope': "PHONE", "uuid": "10-10-10-10"},
             'visibility': {"scope": "SECRET"},  # OBSERVE RESULT
             'name': '2234512345', 'uuid': "XYZ"}
        ])
        self.assertEqual(user, {})

    def test_engagements_to_user(self):
        user = {"Positions": []}
        os2mo.engagements_to_user(user, [{
            'org_unit': {'uuid': "UUID"},
            'job_function': {'name': 'CLERK'},
            'uuid': "XYZ"
        }], ["UUID"])
        self.assertEqual(user, {
            'Positions': [{
                'OrgUnitUuid': "UUID",
                'Name': 'CLERK',
                'Uuid': 'XYZ'
            }]
        })

    def test_addresses_to_orgunit(self):
        orgunit = {}
        os2mo.addresses_to_orgunit(orgunit, [
            {'address_type': {'scope': "TEXT"}, 'name': 'ABC', 'uuid': "XYZ"}
        ])
        self.assertEqual(
            orgunit,
            {'Location': {'Uuid': 'XYZ', 'Value': 'ABC'}}
        )

    def test_itsystems_to_orgunit(self):
        orgunit = {"ItSystemUuids": []}
        os2mo.itsystems_to_orgunit(orgunit, [{'itsystem': {'uuid': 'ABCD'}}])
        self.assertEqual(orgunit, {'ItSystemUuids': ['ABCD']})
