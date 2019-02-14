# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import unittest
from mox_stsorgsync import os2mo


class Tests(unittest.TestCase):

    def test_os2mo_url(self):
        self.assertTrue(os2mo.os2mo_url("{BASE}").endswith("service"))

    def test_addresses_to_user(self):
        user = {}
        os2mo.addresses_to_user(user, [
            {'address_type': {'scope': "DAR"}, 'name': 'ABC', 'uuid': "XYZ"}
        ])
        self.assertEqual(user, {'Location': {'Uuid': 'XYZ', 'Value': 'ABC'}})

    def test_engagements_to_user(self):
        user = {"Positions": []}
        os2mo.engagements_to_user(user, [{
            'org_unit': {'uuid': "UUID"},
            'job_function': {'name': 'CLERK'},
            'uuid': "XYZ"
        }])
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
