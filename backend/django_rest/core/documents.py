"""Create Elasticsearch document"""

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from core.models import ProductItem

# Info: 'django-elasticsearch-dsl' automatically created the appropriate
#       database signals so that your Elasticsearch storage gets updated every
#       time an instance of a model is created, deleted, or edited.

# Note: To create and populate the Elasticsearch index and mapping, use the
#       search_index command in django server environment:
#
#       python manage.py search_index --rebuild --no-parallel
#
#       OR
#
#       sleep 15 && echo 'y' | python manage.py search_index --rebuild
#
#       * You need to run this command every time you change your index
#         settings or attribute that any field in Django class depends on.
#       * The alternative way in case you want to pass value 'y' when std ask
#         you BUT you always have to wait 15 seconds at least before enter 'y'
#         otherwise will face issue of (Connection timed out).
#
#       Options:
#       1) -f option is for force operation without asking (y/N?) But this
#             option will cause error (Connection timed out), see the
#             alternative way.
#       2) --no-parallel is for run populate/rebuild update single threaded.

# Important:
# I have created script that can use to do the process for you by running:
#
# >> docker-compose run --rm app sh -c "/usr/src/compose/es-index-rebuild.sh"


@registry.register_document
class ProductItemDocument(Document):
    """Document class of model ProductItem"""

    # Info: Document in Elasticsearch is representing row of fields those
    #       indexed from SQL database table.

    # Info: Each document needs to have an Index and Django class:
    #       1- In the Index class, we need to provide the index (table) name
    #          and Elasticsearch index settings.
    #       2- In the Django class, we tell the document which Django model to
    #          associate it to and provide the fields we want to be indexed.

    # Define relationships/customized fields to be indexed.
    # Note: Take care of relationships fields like Foreign, Many To Many and
    #       one To Many by using 'ObjectField'.
    # product = fields.ObjectField(properties={
    #     # 'id': fields.IntegerField(),
    #     'title': fields.TextField()
    # })

    # Here we are using TextField and pass to it an attribute that is model
    # method instead of using ObjectField.
    # Note: The primary difference between the text datatype and the keyword
    #       datatype is that text fields are analyzed at the time of indexing,
    #       and keyword fields are not. What that means is, text fields are
    #       broken down into their individual terms at indexing to allow for
    #       partial matching, while keyword fields are indexed as is. So any
    #       special characters in text fields will be ignored in query time and
    #       word like 'tea-time' will lead to ignore 'time'. In fact, the
    #       hyphen appears to be a special case, because it is a reserved
    #       character in Elasticsearch, used for ensuring that a term
    #       immediately following a hyphen does not appear in the results.
    product_item_info = fields.TextField(attr='product_item_info')

    class Index:
        # Name of the Elasticsearch index (use hyphen for multi words).
        name = 'product-items'
        # Define settings for current Elasticsearch document
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        # Set the model associated with this Document
        model = ProductItem
        # The fields of the model you want to be indexed in Elasticsearch
        fields = ['slug', 'sku']

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True

        # Configure how the index should be refreshed after an update.
        # See Elasticsearch documentation for supported options:
        # https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-refresh.html
        # This per-Document setting overrides:
        # settings.ELASTICSEARCH_DSL_AUTO_REFRESH.
        # auto_refresh = False

        # Paginate the django queryset used to populate the index with the
        # specified size (by default it uses the database driver's default
        # setting)
        # queryset_pagination = 5000
