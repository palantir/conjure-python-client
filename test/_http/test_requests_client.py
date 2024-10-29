import pickle
import sys

from conjure_python_client._http.requests_client import (
    SOCKET_KEEP_ALIVE,
    SOCKET_KEEP_INTVL,
    TransportAdapter,
)

if sys.platform != "darwin":
    from conjure_python_client._http.requests_client import SOCKET_KEEP_IDLE


def test_can_enable_keep_alives_in_transport_adapter():
    assert (
        TransportAdapter(max_retries=12, enable_keep_alive=True)._enable_keep_alive
        is True
    )
    assert TransportAdapter(max_retries=12)._enable_keep_alive is False
    assert TransportAdapter()._enable_keep_alive is False


def test_keep_alive_passes_correct_options():
    socket_options = TransportAdapter(
        max_retries=12, enable_keep_alive=True
    ).poolmanager.connection_pool_kw["socket_options"]
    assert SOCKET_KEEP_ALIVE in socket_options
    assert SOCKET_KEEP_INTVL in socket_options
    if sys.platform != "darwin":
        assert SOCKET_KEEP_IDLE in socket_options


def test_keep_alive_passed_in_state_in_transport_adapter():
    ta = TransportAdapter()
    ta.__setstate__(
        TransportAdapter(max_retries=12, enable_keep_alive=True).__getstate__()
    )
    assert ta._enable_keep_alive is True
    assert ta.max_retries.total == 12


def test_transport_adapter_pickles_correctly():
    pre_adapter = TransportAdapter(enable_keep_alive=True)
    post_adapter = pickle.loads(pickle.dumps(pre_adapter))
    assert post_adapter._enable_keep_alive is True
    assert post_adapter._pool_connections == pre_adapter._pool_connections
    assert post_adapter._pool_maxsize == pre_adapter._pool_maxsize


def test_transport_adapter_can_be_unpickled_from_old_pickle():
    # Remove "_enable_keep_alive" attr from get state so that when picked it emulates an old instance of this
    # class being pickled before this attr was added. Then verify we can pickle and unpickle to validate we
    # give it a default value if not present when unpickled.
    TransportAdapter.__getstate__ = lambda self: {
        attr: getattr(self, attr, None)
        for attr in self.__attrs__
        if attr != TransportAdapter.ENABLE_KEEP_ALIVE_ATTR
    }
    adapter = pickle.loads(pickle.dumps(TransportAdapter()))
    assert adapter._enable_keep_alive is False
