# -*- coding: utf-8 -*-


import logging

logger = logging.getLogger(__name__)


class RuStoreParserBase:
    selector_key = None

    def __init__(self, string_data, url=None, extractor_manifest=None):
        self.string_data = string_data
        self.url = url
        self.extractor_manifest = extractor_manifest

    def parse_data(self, string_data):
        """
        This function will be used to convert string to html/xml tree.
        :return:
        """
        raise NotImplementedError()

    def get_selector_key(self):
        if self.selector_key is None:
            raise Exception("selector_key should be assigned to Parser classes")
        return self.selector_key

    def run_extractor(self, xml_tree=None, extractor=None):
        extractor_id = extractor.extractor_id
        logger.info("Running extractor:'{}' on url:{}".format(extractor_id, self.url))
        try:
            extractor_object = extractor.extractor_cls(
                **{
                    'url': self.url,
                    self.get_selector_key(): xml_tree,
                    'extractor': extractor,
                    'extractor_id': extractor_id
                }
            )
            return extractor_object.run()
        except Exception as error:
            logger.error(
                "Failed to extract data from the extractor '{extractor_id}:{extractor_type}' on url "
                "'{url}' with error: '{error}'".format(
                    extractor_id=extractor_id,
                    extractor_type=extractor.extractor_type,
                    url=self.url,
                    error=error)
            )
            return {extractor_id: None}

    @staticmethod
    def flatten_extracted_data(all_extracted_data):
        all_extracted_data_new = {}
        for k, v in all_extracted_data.items():
            all_extracted_data_new.update(v)
        return all_extracted_data_new

    def run_extractors(self, flatten_extractors=False):
        xml_tree = self.parse_data(self.string_data)
        all_extracted_data = {}
        for extractor in self.extractor_manifest.extractors:
            extracted_data = self.run_extractor(extractor=extractor, xml_tree=xml_tree)
            all_extracted_data.update(extracted_data)
        if flatten_extractors is True:
            return self.flatten_extracted_data(all_extracted_data)
        return all_extracted_data