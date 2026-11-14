import pytest

from conjure_python_client import RequestsClient, Service, ServiceConfiguration


@pytest.mark.parametrize("scheme", ["http", "https"])
def test_mesh_uri_is_normalized_and_retries_are_disabled(scheme):
    uri = "{}://localhost:8080/api".format(scheme)
    config = ServiceConfiguration(uris=["mesh-" + uri], max_num_retries=5)

    service = RequestsClient.create(Service, "test", config)

    assert service._uris == [uri]
    assert service._requests_session.get_adapter(uri).max_retries.total == 0
    assert config.uris == ["mesh-" + uri]
    assert config.max_num_retries == 5


@pytest.mark.parametrize(
    "uris",
    [
        ["mesh-http://localhost:8080", "mesh-http://localhost:8081"],
        ["http://localhost:8080", "mesh-http://localhost:8081"],
        ["mesh-http://localhost:8080", "http://localhost:8081"],
    ],
)
def test_mesh_requires_exactly_one_uri(uris):
    with pytest.raises(ValueError, match="exactly one URI"):
        RequestsClient.create(Service, "test", ServiceConfiguration(uris=uris))


def test_regular_uris_preserve_configured_retries():
    uris = ["http://localhost:8080/api", "https://localhost:8081/api"]
    service = RequestsClient.create(
        Service, "test", ServiceConfiguration(uris=uris, max_num_retries=5)
    )

    assert service._uris == uris
    for uri in uris:
        assert (
            service._requests_session.get_adapter(uri).max_retries.total == 5
        )
