from opensearchpy import OpenSearch
from config import INDEX_NAME


def delete_index(index_name):
    client = OpenSearch(
        hosts=[{'host': 'localhost', 'port': 9200}],
        use_ssl=False,
        verify_certs=False
    )

    # インデックスが存在するか確認
    if client.indices.exists(index=index_name):
        client.indices.delete(index=index_name)
        print(f"Index {index_name} deleted.")


if __name__ == "__main__":
    delete_index(index_name=INDEX_NAME)
