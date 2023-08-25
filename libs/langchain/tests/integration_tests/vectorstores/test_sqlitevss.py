"""Test Milvus functionality."""
from typing import List, Optional

from langchain.docstore.document import Document
from langchain.vectorstores import SQLiteVSS
from tests.integration_tests.vectorstores.fake_embeddings import (
    FakeEmbeddings,
    fake_texts,
)


def _sqlite_vss_from_texts(
    metadatas: Optional[List[dict]] = None, drop: bool = True
) -> SQLiteVSS:
    return SQLiteVSS.from_texts(
        fake_texts,
        FakeEmbeddings(),
        metadatas=metadatas,
        table="test",
        db_file=":memory:"
    )


def test_sqlvss() -> None:
    """Test end to end construction and search."""
    docsearch = _sqlite_vss_from_texts()
    output = docsearch.similarity_search("foo", k=1)
    assert output == [Document(page_content="foo", metadata=None)]


def test_sqlvss_with_score() -> None:
    """Test end to end construction and search with scores and IDs."""
    texts = ["foo", "bar", "baz"]
    metadatas = [{"page": i} for i in range(len(texts))]
    docsearch = _sqlite_vss_from_texts(metadatas=metadatas)
    output = docsearch.similarity_search_with_score("foo", k=3)
    docs = [o[0] for o in output]
    scores = [o[1] for o in output]
    assert docs == [
        Document(page_content="foo", metadata={"page": 0}),
        Document(page_content="bar", metadata={"page": 1}),
        Document(page_content="baz", metadata={"page": 2}),
    ]
    assert scores[0] < scores[1] < scores[2]

def test_sqlvss_add_extra() -> None:
    """Test end to end construction and MRR search."""
    texts = ["foo", "bar", "baz"]
    metadatas = [{"page": i} for i in range(len(texts))]
    docsearch = _sqlite_vss_from_texts(metadatas=metadatas)

    docsearch.add_texts(texts, metadatas)

    output = docsearch.similarity_search("foo", k=10)
    assert len(output) == 6


# if __name__ == "__main__":
#     test_milvus()
#     test_milvus_with_score()
#     test_milvus_max_marginal_relevance_search()
#     test_milvus_add_extra()
#     test_milvus_no_drop()
