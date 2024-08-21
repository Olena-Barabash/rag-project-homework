from typing import Dict, List, Union

import numpy as np
from elasticsearch import Elasticsearch

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

QUERY = "When is the next cohort?"


@data_loader
def search(*args, **kwargs) -> List[Dict]:
    connection_string = kwargs.get('connection_string', 'http://localhost:9200')
    index_name = kwargs.get('index_name', 'documents')
    top_k = kwargs.get('top_k', 5)
    chunk_column = kwargs.get('chunk_column', 'content')

    script_query = {
        "bool": {
            "must": {
                "multi_match": {
                    "query": QUERY,
                    "fields": ["question", "text", "section"],
                    "type": "cross_fields"
                }
            }
        }
    }

    es_client = Elasticsearch(connection_string)

    response = es_client.search(
        index=index_name,
        body=dict(
            size=top_k,
            query=script_query,
        ),
    )

    return [hit['_source'] for hit in response['hits']['hits']]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'