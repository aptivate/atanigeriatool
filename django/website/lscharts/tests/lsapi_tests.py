from __future__ import unicode_literals, absolute_import

from django.test.testcases import TestCase

from lscharts.lsapi import LiveStoriesAPI


class LiveStoriesAPITests(TestCase):

    def setUp(self):
        self.api = LiveStoriesAPI("http://ata.livestories.com")

    def patch_get_json(self, fake_result):
        def fake_get_json(api_path):
            return fake_result
        self.api.get_json = fake_get_json

    def test_get_most_recent_dataset_returns_none_if_no_datasets(self):
        self.patch_get_json([])
        self.assertIsNone(self.api.get_most_recent_dataset('mydataset'))

    def test_get_most_recent_dataset_returns_none_if_no_datasets_match(self):
        self.patch_get_json([{"name": "otherdataset"}])
        self.assertIsNone(self.api.get_most_recent_dataset('mydataset'))

    def test_get_most_recent_dataset_returns_latest_matching_dataset(self):
        self.patch_get_json([
            {"name": "otherdataset", 'modified': "2015-01-07T15:56:21.653000"},
            {"name": "mydataset", 'modified': "2015-01-06T15:56:21.653000"},
            {"name": "mydataset", 'modified': "2015-01-05T15:56:21.653000"},
        ])
        most_recent = self.api.get_most_recent_dataset('mydataset')
        self.assertEqual("2015-01-06T15:56:21.653000", most_recent['modified'])
