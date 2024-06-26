from opensearchpy import OpenSearch
from config import INDEX_NAME

def search_index(index_name: str, keywords: list[str]) -> list[dict]:
    client = OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        use_ssl=False,
        verify_certs=False
    )

    query = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"content": " ".join(keywords)}}
                ],
                "minumum_should_match": 1
            }
        }
    }

    response = client.search(
        index=INDEX_NAME,
        body=query
    )
    return response["hits"]["hits"]