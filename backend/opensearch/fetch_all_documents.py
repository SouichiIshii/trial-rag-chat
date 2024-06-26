from opensearchpy import OpenSearch
import pprint
from opensearch.config import INDEX_NAME


def fetch_all_documents(index_name: str):
    client = OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        use_ssl=False,
        verify_certs=False
    )

    data = {
        "size": 100,
        "query": {
            "match_all": {}
        }
    }

    response = client.search(
        index=index_name,
        body=data,
        scroll="1m"
    )

    scroll_id = response["_scroll_id"]
    all_documents = response["hits"]["hits"]

    while True:
        response = client.scroll(scroll_id=scroll_id, scroll="1m")
        scroll_id = response["_scroll_id"]
        if not response["hits"]["hits"]:
            break
        all_documents.extend(response["hits"]["hits"])
    
    client.clear_scroll(scroll_id=scroll_id)

    return all_documents


if __name__ == "__main__":
    documents = fetch_all_documents(index_name=INDEX_NAME)
    for doc in documents:
        pprint.pprint(doc)