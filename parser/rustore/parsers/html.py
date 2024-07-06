# -*- coding: utf-8 -*-

import logging
from rustore.utils import convert_html_to_selector
from .base import RuStoreParserBase

logger = logging.getLogger(__name__)


class RuStoreHTMLParser(RuStoreParserBase):
    """
    extractor_manifest should be a list of extractors i.e., `rustore_extractors`.
    """
    selector_key = "html_selector"

    def __init__(self, url=None, string_data=None, extractor_manifest=None):
        super().__init__(url=url, string_data=string_data, extractor_manifest=extractor_manifest)
        if self.url is None:
            raise Exception(
                "url cannot be blank, as it is used to generate absolute urls in most of the cases. You can "
                "use http://dummy-url.com as a dummy url if needed."
            )

    def parse_data(self, string_data):
        """
        This function will be used to convert string to html tree.
        :return:
        """
        return convert_html_to_selector(string_data)