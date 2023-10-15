from elasticsearch_dsl import Document, Keyword, MetaField, analyzer, token_filter


class Mappings(Document):
    """Class representing the basic document structure for Elasticsearch."""

    id = Keyword()

    class Meta:
        dynamic = MetaField('strict')

    def to_dict(self) -> dict:
        """
        Serialize the document into a dictionary for correct data loading via a bulk request.

        Returns:
            dict: Document data in a convenient format for loading.
        """
        doc = super().to_dict(include_meta=True)
        doc['_id'] = self.id
        return doc


class Settings(object):
    """Class for index settings in Elasticsearch."""

    settings = {'refresh_interval': '1s'}
    analyzers = [analyzer('ru_en', tokenizer='standard', filter=[
        'lowercase',
        token_filter('english_stop', 'stop', stopwords='_english_'),
        token_filter('english_stemmer', 'stemmer', language='english'),
        token_filter('english_possessive_stemmer', 'stemmer', language='possessive_english'),
        token_filter('russian_stop', 'stop', stopwords='_russian_'),
        token_filter('russian_stemmer', 'stemmer', language='russian'),
    ])]
