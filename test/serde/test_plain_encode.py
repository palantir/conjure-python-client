import pytest
from conjure_python_client import ConjureEncoder

from test.generated.conjure_verification_types import EnumExample


@pytest.mark.parametrize("value,expected_encoded", [
    (float('inf'), 'Infinity'),
    (-float('inf'), '-Infinity'),
    (EnumExample.ONE_HUNDRED, 'ONE_HUNDRED'),
    (True, 'true'),
    (False, 'false'),
    ([1, "test", EnumExample.ONE], ["1", "test", "ONE"])
])
def test_plain_encodes(value, expected_encoded):
    encoded = ConjureEncoder.plain(value)
    assert(encoded == expected_encoded)
