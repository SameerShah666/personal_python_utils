import requests
import json

class Pinata:
    def __init__(self, api_key, gateway):
        self.api_key = api_key
        self.gateway = gateway
        self.pinata_api_url = "https://api.pinata.cloud"
        self.pinata_api_pinList = self.pinata_api_url + "/data/pinList/"
        self.pinata_api_url_pinning = self.pinata_api_url + "/pinning/pinFileToIPFS"

    def pin_file_to_ipfs(self, file_path):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
        }
        files = {"file": open(file_path, "rb")}
        response = requests.post(
            self.pinata_api_url_pinning, headers=headers, files=files
        )
        return json.dumps(response.json(), indent=4)

    def request_pin_list(self):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
        }
        response = requests.get(
            self.pinata_api_pinList, headers=headers
        )
        return json.dumps(response.json(), indent=4)
    
    def get_item(self, item_hash):
        return requests.get(self.gateway + "/ipfs/" + item_hash)
