import pytest 


from writings.sync import extract_title


@pytest.fixture(scope="module", params=[
    ('/home/dev/writings/Gallop Interfacing with a database.edited.docx', 'Gallop Interfacing with a database'),
    ('/home/dev/writings/Reaching Consensus on Consenus.edited.docx', 'Reaching Consensus on Consenus'),
    ('/home/dev/writings/TL;DR - Google Cloud Bigtable.edited.docx', 'TL;DR - Google Cloud Bigtable'),
    ('/home/dev/writings/Gallop indexing.edited.docx', 'Gallop indexing'),
    ('/home/dev/writings/Blogging by dummies.edited.docx', 'Blogging by dummies'),
    ('/home/dev/writings/Gallop An analytics database written in Rust.edited.docx', 'Gallop An analytics database written in Rust'),
    ('/home/dev/writings/TL;DR - ElasticSearch.edited.docx', 'TL;DR - ElasticSearch'),
    ('/home/dev/writings/Hello world!.edited.docx', 'Hello world!'),
    ('/home/dev/writings/How low can you go - with Search.edited.docx', 'How low can you go - with Search'),
])
def make_path_to_title(request):
    return request.param


def test_path_to_title(make_path_to_title):
    path, title = make_path_to_title
    assert extract_title(path) == title
