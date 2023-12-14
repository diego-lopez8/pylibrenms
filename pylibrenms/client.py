"""
Client for LibreNMS
"""
import requests
import json

class Librenms:

    def __init__(self, base_url, api_key):
        """
        Creates a LibreNMS client. 

        Parameters:
            - base_url: URL of the LibreNMS instance to query
            - api_key: API token used for authentication. 
        """
        if not base_url.endswith('/'):
            base_url += '/'
        self.url = base_url + "api/v0/"
        self._api_key = api_key
        self._headers = {"X-Auth-Token": self._api_key}

    def _get(self, route, columns=None):
        """
        'GET" call to be used by all functions. 
        """
        endpoint = self.url + route
        params = {}
        # TODO: figure out if supporting strings or lists as columns is a good idea, just testing with lists now
        if columns:
            params['columns'] = ','.join(columns) if isinstance(columns, list) else columns
        try:
            response = requests.get(endpoint, headers=self._headers, params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            # TODO: implement an exception here
            raise Exception(f"Error occurred, {e}")

    def get_all_ports(self, columns=None):
        """
        Get all ports on all devices.

        Parameters:
            - columns: columns to filter on. None means return all columns.  
        """
        return self._get("ports", columns=columns)

    def search_ports(self, field, search_string, columns=None):
        """
        Search for ports matching a specific query. 

        Parameters:
            - field: a list of fields to search. Can be ifAlias, ifDescr, ifName, or all.
            - search_string: the string to search. 
            - columns: columns to filter on. None means return all columns.  
        """

        if field not in ["ifAlias", "ifDescr", "ifName", "all"]:
            # TODO: implement exception
            raise Exception(f"Error occurred!")
        if field == "all":
            return self._get("ports/search/" + str(search_string), columns=columns)
        else:
            # fields is any of the remaining ifAlias, ifDescr, ifName
            return self._get("ports/search/" + str(field) + "/" + str(search_string), columns=columns)

    def ports_with_associated_mac(self,):
        ...

    def get_port_info(self, port_id):
        """
        Returns port information given a specific Port ID.

        Parameters:
            - port_id : a port ID.
        """

        return self._get("ports/" + str(port_id), columns=None)
    
    def get_port_ip_info(self, port_id):
        """
        Returns all Ipv4 and Ipv6 information for a given port ID.

        Parameters:
            - port_id: a port ID.
        """

        return self._get("ports/" + str(port_id) + "/ip")