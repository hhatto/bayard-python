import json
from urllib.parse import urljoin
from typing import Dict, Iterable

import httpx


HOST = "127.0.0.1"
PORT = 8000


class BayardHTTPClient:

    def __init__(self, host: str = HOST, port: int = PORT, method: str = "http", timeout: int = 3.0, version: str = "v1"):
        self.url = f"{method}://{host}:{port}/{version}/"
        limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
        self._client = httpx.Client(timeout=timeout, limits=limits)

    def get_document(self, document_id: str):
        res = self._client.get(urljoin(self.url, f"documents/{document_id}"))
        if res.status_code == 500:
            return {"result": "not found"}
        elif res.status_code == 404:
            return {"result": f"not found data. id={document_id}"}
        if res.status_code != 200:
            raise Exception(f"error response: statuscode={res.status_code}")
        return res.json()

    def set_document(self, document_id: str, document: Dict[str, str]):
        headers = {"Content-Type": "application/json"}
        res = self._client.put(urljoin(self.url, f"documents/{document_id}"), data=json.dumps(document), headers=headers)
        if res.status_code != 200:
            raise Exception(f"error response: statuscode={res.status_code}")
        return True

    def delete_document(self, document_id: str):
        res = self._client.delete(urljoin(self.url, f"documents/{document_id}"))
        if res.status_code != 200:
            raise Exception(f"error response: statuscode={res.status_code}")
        return True

    def bulk_set(self, documents: Iterable[Dict[str, str]]):
        datas = [json.dumps(doc) for doc in documents]
        headers = {"Content-Type": "application/json"}
        res = self._client.put(urljoin(self.url, "documents"), data="\n".join(datas), headers=headers)
        if res.status_code != 200:
            raise Exception(f"error response: statuscode={res.status_code}")
        return True

    def bulk_delete(self, ids: Iterable[str]):
        datas = [f'{{"_id": "{_id}"}}' for _id in ids]
        headers = {"Content-Type": "application/json"}
        # NOTE: request body not used with DELETE method
        res = httpx.request("DELETE", urljoin(self.url, "documents"), data="\n".join(datas), headers=headers)
        if res.status_code != 200:
            raise Exception(f"error response: statuscode={res.status_code}")
        return True

    def commit(self):
        res = self._client.get(urljoin(self.url, "commit"))
        if res.status_code != 200:
            raise Exception(f"error response: statuscode={res.status_code}")
        return res.content

    def rollback(self):
        res = self._client.get(urljoin(self.url, "rollback"))
        if res.status_code != 200:
            raise Exception(f"error response: statuscode={res.status_code}")
        return True

    def merge(self):
        res = self._client.get(urljoin(self.url, "merge"))
        if res.status_code != 200:
            raise Exception(f"error response: statuscode={res.status_code}")
        return True

    def schema(self):
        res = self._client.get(urljoin(self.url, "schema"))
        if res.status_code != 200:
            raise Exception(f"error response: statuscode={res.status_code}")
        return res.json()

    def search(self, query: str, limit=10):
        params = {"limit": limit}
        res = self._client.post(urljoin(self.url, "search"), params=params, data=query)
        if res.status_code != 200:
            raise Exception(f"error response: statuscode={res.status_code}")
        return res.json()

    def status(self):
        res = self._client.get(urljoin(self.url, "status"))
        if res.status_code != 200:
            raise Exception(f"error response: statuscode={res.status_code}")
        return res.json()
