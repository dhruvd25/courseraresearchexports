#!/usr/bin/env python

# Copyright 2016 Coursera
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from courseraresearchexports.commands import jobs
from courseraresearchexports.models.ExportRequest import ExportRequest
from courseraresearchexports.models.ExportRequestWithMetadata import \
    ExportRequestWithMetadata
from mock import MagicMock
from mock import patch
import argparse


fake_course_id = 'fake_course_id'
fake_course_slug = 'fake_course_slug'


@patch('courseraresearchexports.commands.jobs.api.get_all')
def test_get_all(api_get_all):
    api_get_all.return_value = []

    jobs.get_all(argparse.Namespace())

    api_get_all.assert_any_call()


@patch('courseraresearchexports.models.utils.lookup_course_slug_by_id')
@patch('courseraresearchexports.commands.jobs.api.get')
def test_get(api_get, lookup_course_slug_by_id):
    lookup_course_slug_by_id.return_value = fake_course_slug
    api_get.return_value = [
        ExportRequestWithMetadata(course_id=fake_course_id)
    ]
    args = argparse.Namespace()
    args.id = fake_course_id

    jobs.get(args)

    api_get.assert_called_with(fake_course_id)


@patch('courseraresearchexports.commands.jobs.api.post')
def test_request(api_post):
    api_post.return_value = [
        ExportRequestWithMetadata(course_id=fake_course_id)
    ]
    args = argparse.Namespace()
    args.course_id = fake_course_id
    args.course_slug = None
    args.partner_id = None
    args.partner_short_name = None
    args.group_id = None
    args.export_type = None
    args.user_id_hashing = None
    args.purpose = None
    args.schemas = None

    jobs.request_tables(args)

    export_request, = api_post.call_args[0]
    assert export_request.course_id == fake_course_id
