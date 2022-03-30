# coding=utf-8
import builtins
from conjure_python_client import (
    BinaryType,
    ConjureBeanType,
    ConjureDecoder,
    ConjureEncoder,
    ConjureFieldDefinition,
    OptionalTypeWrapper,
    Service,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    Type,
)

class another_TestService(Service):
    """
    A Markdown description of the service.
    """

    def get_file_systems(self, auth_header: str) -> Dict[str, "product_datasets_BackingFileSystem"]:
        """
        Returns a mapping from file system id to backing file system configuration.
        """

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
        }

        _json: Any = None

        _path = '/catalog/fileSystems'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'GET',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        _decoder = ConjureDecoder()
        return _decoder.decode(_response.json(), Dict[str, product_datasets_BackingFileSystem])

    def create_dataset(self, auth_header: str, request: "product_CreateDatasetRequest", test_header_arg: str) -> "product_datasets_Dataset":
        """
        foo $bar
        """

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': auth_header,
            'Test-Header': test_header_arg,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
        }

        _json: Any = ConjureEncoder().default(request)

        _path = '/catalog/datasets'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'POST',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        _decoder = ConjureDecoder()
        return _decoder.decode(_response.json(), product_datasets_Dataset)

    def get_dataset(self, auth_header: str, dataset_rid: str) -> Optional["product_datasets_Dataset"]:

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
            'datasetRid': dataset_rid,
        }

        _json: Any = None

        _path = '/catalog/datasets/{datasetRid}'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'GET',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        _decoder = ConjureDecoder()
        return None if _response.status_code == 204 else _decoder.decode(_response.json(), OptionalTypeWrapper[product_datasets_Dataset])

    def get_raw_data(self, auth_header: str, dataset_rid: str) -> Any:

        _headers: Dict[str, Any] = {
            'Accept': 'application/octet-stream',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
            'datasetRid': dataset_rid,
        }

        _json: Any = None

        _path = '/catalog/datasets/{datasetRid}/raw'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'GET',
            self._uri + _path,
            params=_params,
            headers=_headers,
            stream=True,
            json=_json)

        _raw = _response.raw
        _raw.decode_content = True
        return _raw

    def get_aliased_raw_data(self, auth_header: str, dataset_rid: str) -> Any:

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
            'datasetRid': dataset_rid,
        }

        _json: Any = None

        _path = '/catalog/datasets/{datasetRid}/raw-aliased'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'GET',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        _decoder = ConjureDecoder()
        return _decoder.decode(_response.json(), product_NestedAliasedBinary)

    def maybe_get_raw_data(self, auth_header: str, dataset_rid: str) -> Optional[Any]:

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
            'datasetRid': dataset_rid,
        }

        _json: Any = None

        _path = '/catalog/datasets/{datasetRid}/raw-maybe'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'GET',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        _decoder = ConjureDecoder()
        return None if _response.status_code == 204 else _decoder.decode(_response.json(), OptionalTypeWrapper[BinaryType])

    def get_aliased_string(self, auth_header: str, dataset_rid: str) -> str:

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
            'datasetRid': dataset_rid,
        }

        _json: Any = None

        _path = '/catalog/datasets/{datasetRid}/string-aliased'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'GET',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        _decoder = ConjureDecoder()
        return _decoder.decode(_response.json(), product_AliasedString)

    def upload_raw_data(self, auth_header: str, input: Any) -> None:

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
        }

        _json: Any = ConjureEncoder().default(input)

        _path = '/catalog/datasets/upload-raw'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'POST',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        return

    def upload_aliased_raw_data(self, auth_header: str, input: Any) -> None:

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
        }

        _json: Any = ConjureEncoder().default(input)

        _path = '/catalog/datasets/upload-raw-aliased'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'POST',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        return

    def get_branches(self, auth_header: str, dataset_rid: str) -> List[str]:

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
            'datasetRid': dataset_rid,
        }

        _json: Any = None

        _path = '/catalog/datasets/{datasetRid}/branches'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'GET',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        _decoder = ConjureDecoder()
        return _decoder.decode(_response.json(), List[str])

    def get_branches_deprecated(self, auth_header: str, dataset_rid: str) -> List[str]:
        """
        Gets all branches of this dataset.
        """

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
            'datasetRid': dataset_rid,
        }

        _json: Any = None

        _path = '/catalog/datasets/{datasetRid}/branchesDeprecated'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'GET',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        _decoder = ConjureDecoder()
        return _decoder.decode(_response.json(), List[str])

    def resolve_branch(self, auth_header: str, branch: str, dataset_rid: str) -> Optional[str]:

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
            'datasetRid': dataset_rid,
            'branch': branch,
        }

        _json: Any = None

        _path = '/catalog/datasets/{datasetRid}/branches/{branch}/resolve'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'GET',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        _decoder = ConjureDecoder()
        return None if _response.status_code == 204 else _decoder.decode(_response.json(), OptionalTypeWrapper[str])

    def test_param(self, auth_header: str, dataset_rid: str) -> Optional[str]:

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
            'datasetRid': dataset_rid,
        }

        _json: Any = None

        _path = '/catalog/datasets/{datasetRid}/testParam'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'GET',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        _decoder = ConjureDecoder()
        return None if _response.status_code == 204 else _decoder.decode(_response.json(), OptionalTypeWrapper[str])

    def test_query_params(self, auth_header: str, implicit: str, query: str, set_end: List[str], something: str, optional_end: Optional[str]=None, optional_middle: Optional[str]=None) -> int:

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
            'different': something,
            'optionalMiddle': optional_middle,
            'implicit': implicit,
            'setEnd': set_end,
            'optionalEnd': optional_end,
        }

        _path_params: Dict[str, Any] = {
        }

        _json: Any = ConjureEncoder().default(query)

        _path = '/catalog/test-query-params'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'POST',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        _decoder = ConjureDecoder()
        return _decoder.decode(_response.json(), int)

    def test_no_response_query_params(self, auth_header: str, implicit: str, query: str, set_end: List[str], something: str, optional_end: Optional[str]=None, optional_middle: Optional[str]=None) -> None:

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
            'different': something,
            'optionalMiddle': optional_middle,
            'implicit': implicit,
            'setEnd': set_end,
            'optionalEnd': optional_end,
        }

        _path_params: Dict[str, Any] = {
        }

        _json: Any = ConjureEncoder().default(query)

        _path = '/catalog/test-no-response-query-params'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'POST',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        return

    def test_boolean(self, auth_header: str) -> bool:

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
        }

        _json: Any = None

        _path = '/catalog/boolean'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'GET',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        _decoder = ConjureDecoder()
        return _decoder.decode(_response.json(), bool)

    def test_double(self, auth_header: str) -> float:

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
        }

        _json: Any = None

        _path = '/catalog/double'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'GET',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        _decoder = ConjureDecoder()
        return _decoder.decode(_response.json(), float)

    def test_integer(self, auth_header: str) -> int:

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
        }

        _json: Any = None

        _path = '/catalog/integer'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'GET',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        _decoder = ConjureDecoder()
        return _decoder.decode(_response.json(), int)

    def test_post_optional(self, auth_header: str, maybe_string: Optional[str]=None) -> Optional[str]:

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
        }

        _json: Any = ConjureEncoder().default(maybe_string)

        _path = '/catalog/optional'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'POST',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        _decoder = ConjureDecoder()
        return None if _response.status_code == 204 else _decoder.decode(_response.json(), OptionalTypeWrapper[str])

    def test_optional_integer_and_double(self, auth_header: str, maybe_double: Optional[float]=None, maybe_integer: Optional[int]=None) -> None:

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
            'maybeInteger': maybe_integer,
            'maybeDouble': maybe_double,
        }

        _path_params: Dict[str, Any] = {
        }

        _json: Any = None

        _path = '/catalog/optional-integer-double'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'GET',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        return

    def get_for_strings(self, auth_header: str, dataset_rid: str, strings: List[str]) -> None:

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
            'strings': strings,
        }

        _path_params: Dict[str, Any] = {
            'datasetRid': dataset_rid,
        }

        _json: Any = None

        _path = '/catalog/datasets/{datasetRid}/strings'
        _path = _path.format(**_path_params)

        _response = self._request( # type: ignore
            'GET',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        return


another_TestService.__name__ = "TestService"
another_TestService.__qualname__ = "TestService"
another_TestService.__module__ = "another"


class product_CreateDatasetRequest(ConjureBeanType):

    @builtins.classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'file_system_id': ConjureFieldDefinition('fileSystemId', str),
            'path': ConjureFieldDefinition('path', str)
        }

    __slots__: List[str] = ['_file_system_id', '_path']

    def __init__(self, file_system_id: str, path: str) -> None:
        self._file_system_id = file_system_id
        self._path = path

    @builtins.property
    def file_system_id(self) -> str:
        return self._file_system_id

    @builtins.property
    def path(self) -> str:
        return self._path


product_CreateDatasetRequest.__name__ = "CreateDatasetRequest"
product_CreateDatasetRequest.__qualname__ = "CreateDatasetRequest"
product_CreateDatasetRequest.__module__ = "product"


class product_datasets_BackingFileSystem(ConjureBeanType):

    @builtins.classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'file_system_id': ConjureFieldDefinition('fileSystemId', str),
            'base_uri': ConjureFieldDefinition('baseUri', str),
            'configuration': ConjureFieldDefinition('configuration', Dict[str, str])
        }

    __slots__: List[str] = ['_file_system_id', '_base_uri', '_configuration']

    def __init__(self, base_uri: str, configuration: Dict[str, str], file_system_id: str) -> None:
        self._file_system_id = file_system_id
        self._base_uri = base_uri
        self._configuration = configuration

    @builtins.property
    def file_system_id(self) -> str:
        """
        The name by which this file system is identified.
        """
        return self._file_system_id

    @builtins.property
    def base_uri(self) -> str:
        return self._base_uri

    @builtins.property
    def configuration(self) -> Dict[str, str]:
        return self._configuration


product_datasets_BackingFileSystem.__name__ = "BackingFileSystem"
product_datasets_BackingFileSystem.__qualname__ = "BackingFileSystem"
product_datasets_BackingFileSystem.__module__ = "product_datasets"


class product_datasets_Dataset(ConjureBeanType):

    @builtins.classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'file_system_id': ConjureFieldDefinition('fileSystemId', str),
            'rid': ConjureFieldDefinition('rid', str)
        }

    __slots__: List[str] = ['_file_system_id', '_rid']

    def __init__(self, file_system_id: str, rid: str) -> None:
        self._file_system_id = file_system_id
        self._rid = rid

    @builtins.property
    def file_system_id(self) -> str:
        return self._file_system_id

    @builtins.property
    def rid(self) -> str:
        """
        Uniquely identifies this dataset.
        """
        return self._rid


product_datasets_Dataset.__name__ = "Dataset"
product_datasets_Dataset.__qualname__ = "Dataset"
product_datasets_Dataset.__module__ = "product_datasets"


product_AliasedString = str

product_AliasedBinary = BinaryType

product_NestedAliasedBinary = product_AliasedBinary

