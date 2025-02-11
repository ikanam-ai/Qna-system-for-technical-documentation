# -*- coding: utf-8 -*-
"""images

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HcGEmoBy0cNOpjERMX3TMlQCsB2As7TM
"""

from rustore.extractors.base import ExtractorBase

class RuStoreImagesExtractor(ExtractorBase):
    def run(self):
        data = {}
        images_data = []
        images_selector = self.html_selector.xpath('//img/@src').extract()
        for selector in images_selector:
            images_data.append(selector)
        data[self.extractor_id] = images_data
        return data