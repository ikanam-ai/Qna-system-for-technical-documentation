import logging

logger = logging.getLogger(__name__)


class ExtractorBase:
    """

    """

    def __init__(self, url=None, html_selector=None, extractor_id=None, **kwargs):
        """
        :param html_selector: html html_selector of the request
        :param extractor_id: the field with which data is stored in database.
        """
        # if url is None:
        #     logger.warning(
        #         "url cannot be blank, as it is used to generate absolute urls in most of the cases, you can "
        #         "give http://dummy-url.com as url, if you want to give a dummy url"
        #     )
        if None in [html_selector, extractor_id]:
            raise Exception(
                "Invalid input to the extractor class, html_selector, extractor and extractor_id are mandatory")

        self.url = url
        self.html_selector = html_selector
        self.extractor_id = extractor_id

    def run(self):
        raise NotImplementedError()


class ContentExtractorBase(ExtractorBase):
    """

    """

    def __init__(self, url=None, html_selector=None, extractor_id=None, extractor=None):
        super(ContentExtractorBase, self).__init__(url=url, html_selector=html_selector, extractor_id=extractor_id)
        self.extractor = extractor
