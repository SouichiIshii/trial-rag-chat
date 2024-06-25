from opensearchpy import OpenSearch


def create_index(opensearch_client: OpenSearch, index_name: str, settings=None, mappings=None):
    if settings is None:
        settings = {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            }
        }

    if mappings is None:
        mappings = {
            "properties": {
                "document_id": {"type": "keyword"},
                "page_number": {"type": "integer"},
                "title": {"type": "text"},
                "registration_date": {"type": "date"},
                "content": {"type": "text"}
            }
        }

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