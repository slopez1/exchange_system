

class SmartContractInterface:
    def _get_function_names_map(self) -> dict:
        return {
            'create': 'CreateAsset',
            'read': 'ReadAsset',
            'all': 'GetAllAssets',
            'update': 'UpdateAsset',
            'delete': 'DeleteAsset',
            'request': 'RequestAsset',
            'accept': 'AcceptRequestAsset',
            'deny': 'DenyRequestAsset'
        }

    def create_asset(self, id: str, endpoint: str, description: str) -> str:
        raise NotImplemented

    def read_asset(self, id: str) -> str:
        raise NotImplemented

    def get_all_assets(self) -> str:
        raise NotImplemented

    def update_asset(self, id: str, endpoint: str, description: str) -> str:
        raise NotImplemented

    def delete_asset(self, id: str) -> bool:
        raise NotImplemented

    def request_asset(self, id: str) -> bool:
        raise NotImplemented

    def accept_requests(self, id: str, requester: str) -> bool:
        raise NotImplemented

    def deny_request(self, id: str, requester: str) -> bool:
        raise NotImplemented

