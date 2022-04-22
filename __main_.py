import requests
import base64
import re


# Class imitating Javascript functions in Python
class Js2Py:
    # Function decodes a string of data which has been encoded using Base64 encoding
    @staticmethod
    def atob(encrypted: str):
        return base64.b64decode(encrypted).decode("utf-8")

    # Function parses a string argument and returns an integer of the specified radix
    @staticmethod
    def parseInt(sin, base):
        try:
            return int(sin, base)
        except:
            return sin

    # Function returns a string created from the specified sequence of UTF-16 code units
    @staticmethod
    def fromCharCode(char_code):
        try:
            return chr(char_code)
        except:
            return f" [fail char ({char_code})] "


class CroxyProxy:
    def __init__(self, search) -> None:
        self.session = requests.Session()
        self.base_url: str = "https://www.croxyproxy.com"
        self.search: str = search

        self.endpoints: dict = {
            "topDomainsSuggest": f"{self.base_url}/topDomainsSuggest",
            "servers": f"{self.base_url}/api/config",
        }

        self.js2py = Js2Py()

    def get_top_domains_suggest(self):
        data: dict = {
            "limit": "1",
            "q": self.search,
        }

        return self.session.post(self.endpoints["topDomainsSuggest"], data=data)

    def get_servers_list(self):

        servers_encrypted = self.session.get(self.endpoints["servers"])

        if servers_encrypted.status_code == 200:

            servers_encrypted_json = servers_encrypted.json()
            if servers_encrypted_json["status"] == "success":

                for encrypted_string in servers_encrypted_json["result"]:
                    server_atob = self.js2py.atob(encrypted_string)
                    server_atob_re = re.findall(".{1,2}", server_atob)
                    print(''.join(self.js2py.fromCharCode(self.js2py.parseInt(server_atob_re[i], 16)) for i, _ in
                                  enumerate(server_atob_re)))


if __name__ == "__main__":
    croxyproxy = CroxyProxy("https://nyaa.si/")

    # Is not mandatory but allows to have queries close to what a human would do
    topDomainsSuggest = croxyproxy.get_top_domains_suggest()

    if topDomainsSuggest.status_code == 200:
        if topDomainsSuggest.json()["status"] == "success":
            servers = croxyproxy.get_servers_list()
            # print(servers.text)
        else:
            exit(topDomainsSuggest.json())
