from opensearchpy import OpenSearch
import json


def load_settings():
    with open('./backend/opensearch/settings.json', 'r') as f:
        settings = json.load(f)
    return settings

def load_mappings():
    with open('./backend/opensearch/mappings.json', 'r') as f:
        mappings = json.load(f)
    return mappings

def create_index(opensearch_client: OpenSearch, index_name: str):
    settings = load_settings()
    mappings = load_mappings()

    body = {
        "settings": settings,
        "mappings": mappings
    }

    if not opensearch_client.indices.exists(index=index_name):
        response = opensearch_client.indices.create(index=index_name, body=body)
        print(f"Index {index_name} created:", response)
    else:
        print(f"Index {index_name} already exists.")


if __name__ == "__main__":
    client = OpenSearch(
            hosts=[{"host": "localhost", "port": 9200}],
            use_ssl=False,
            verify_certs=False
    )

    create_index(opensearch_client=client, index_name="upload_test_index")