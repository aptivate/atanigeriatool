from __future__ import unicode_literals, absolute_import

import logging
import requests

logger = logging.getLogger(__name__)


class LiveStoriesAPI(object):

    def __init__(self, root_url):
        """ root_url should be just the protocol and domain, eg:
            http://ata.livestories.com """
        self.root_url = root_url

    def get_url(self, url):
        """ wrapper around requests we can override in tests """
        return requests.get(url)

    def get_json(self, api_path):
        api_url = self.root_url + api_path
        try:
            response = requests.get(api_url)
        except requests.exceptions.RequestException as e:
            logger.error("Error getting API %s: %s" % (api_url, e))
            raise
        if response.status_code != 200:
            error_msg = "Error getting API %s - status code %d" % \
                (api_url, response.status_code)
            logger.error(error_msg)
            raise StandardError(error_msg)
        return response.json()

    def dataset_list(self):
        return self.get_json('/api/dataset')

    def get_most_recent_dataset(self, dataset_name):
        matching_datasets = [d for d in self.dataset_list()
                             if d['name'] == dataset_name]
        if len(matching_datasets) == 0:
            return None
        matching_datasets.sort(key=lambda d: d['modified'], reverse=True)
        return matching_datasets[0]
