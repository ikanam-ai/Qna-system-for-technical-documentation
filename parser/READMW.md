## How to use

### HTMLParser

```
from rustore_parsers import RuStoreHTMLParser
from rustore_manifest import RuStoreWebParserManifest
import urllib.request
import yaml

# Загрузка HTML контента
string_data = urllib.request.urlopen("https://www.rustore.ru/help/").read().decode("utf-8")

# Манифест экстракторов в формате YAML
extraction_manifest_yaml = """
- extractor_type: RuStoreMetaTagExtractor
  extractor_id: meta_tags
- extractor_type: RuStoreCustomDataExtractor
  extractor_id: content
  extractor_fields:
  - field_id: title
    element_query:
      type: css
      value: title
    data_attribute: text
    data_type: RuStoreStringField
"""

# Парсинг YAML в Python объект
extractor_manifest = yaml.load(extraction_manifest_yaml, yaml.Loader)

# Создание манифеста для парсера
manifest = RuStoreWebParserManifest(
    title="rustore.ru help",
    domain="rustore.ru",
    version="alpha",
    test_urls="https://www.rustore.ru/help/",
    owner={
        "title": "VK",
        "ownership_type": "Company",
        "email": "support@rustore.ru",
        "website_url": "https://www.rustore.ru"
    },
    extractors=extractor_manifest
)

# Создание экземпляра парсера и выполнение экстракторов
engine = RuStoreHTMLParser(string_data=string_data, url="https://www.rustore.ru/help/", extractor_manifest=manifest)
data = engine.run_extractors()
print(data)

# Выполнение экстракторов с флагом flatten_extractors=True
data_flat = engine.run_extractors(flatten_extractors=True)
print(data_flat)
```