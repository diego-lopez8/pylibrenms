"""
Client for LibreNMS
"""
import requests

class Librenms:

    def __init__(self, base_url, api_key):
        if not base_url.endswith('/'):
            base_url += '/'
        self.url = base_url + "api/v0/"
        self._api_key = api_key
        self._headers = {"X-Auth-Token": self._api_key}

    def _get(self, route):
        """
        'GET" call to be used by all functions. 
        """
        endpoint = self.url + route
        try:
            response = requests.get(endpoint, headers=self._headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            # TODO: fix up these exceptions
            print(f"Error occurred: {e}")

    def get_all_ports(self, ):
        ...

    def search_ports(self, ):
        ...
    
    def ports_with_associated_mac(self,):
        ...

    def get_port_info(self, port_id):
        """
        Returns port information given a specific Port ID.

        Parameters:
            - port_id : a port ID
        """

        return self._get("ports/" + str(port_id))
    
    def get_port_ip_info(self,):
        ...