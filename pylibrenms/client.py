"""
Client for LibreNMS
"""
import requests
import json
import logging

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

    def _get(self, route, params=None):
        """
        'GET" call to be used by endpoints. 
        """
        endpoint = self.url + route
        if params is None:
            params = {}
        else:
            for key, value in params.items():
                if isinstance(value, list):
                    params[key] = ','.join(value)            
        # TODO: figure out if supporting strings or lists as columns is a good idea, just testing with lists now
        try:
            response = requests.get(endpoint, headers=self._headers, params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            # TODO: implement exception here
            raise Exception(f"Error occurred, {e}")
        
    def _post(self, route, data=None):
        """
        POST call to be used by endpoints.
        """
        endpoint = self.url + route
        if data is None:
            data = {}
        try:
            response = requests.post(endpoint, headers=self._headers, json=data)
            return response.json()
        except requests.exceptions.RequestException as e:
            # TODO: implement exception here
            raise Exception(f"Error occurred, {e}")        

    def _delete(self, route, data=None):
        """
        POST call to be used by endpoints.
        """
        endpoint = self.url + route
        if data is None:
            data = {}
        try:
            response = requests.delete(endpoint, headers=self._headers, json=data)
            return response.json()
        except requests.exceptions.RequestException as e:
            # TODO: implement exception here
            raise Exception(f"Error occurred, {e}")     

    def get_all_ports(self, columns=None):
        """
        Get all ports on all devices.

        Parameters:
            - columns: columns to filter on. None means return all columns.  
        """
        return self._get("ports", params={"columns": columns})

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
            return self._get("ports/search/" + str(field) + "/" + str(search_string), params={"columns": columns})

    def ports_with_associated_mac(self,):
        ...

    def get_port_info(self, port_id):
        """
        Returns port information given a specific Port ID.

        Parameters:
            - port_id : a port ID.
        """

        return self._get("ports/" + str(port_id))
    
    def get_port_ip_info(self, port_id):
        """
        Returns all Ipv4 and Ipv6 information for a given port ID.

        Parameters:
            - port_id: a port ID.
        """

        return self._get("ports/" + str(port_id) + "/ip")
    
    def del_device(self, hostname):
        """
        Delete a given device.

        Parameters:
            - hostname: either the device hostname or ID
        """

        return self._delete("devices/" + str(hostname))
    
    def get_device(self, hostname):
        """
        Get details of a given device.

        Parameters:
            - hostname: either the device hostname or ID

        NOTE: hostname is the IP Address or DNS name of the device, libreNMS stores the actual hostname in sysName.
        """

        return self._get("devices/" + str(hostname))

    def discover_device(self, hostname):
        """
        Trigger a discovery of given device.

        Parameters:
            - hostname: either the device hostname or ID

        NOTE: hostname is the IP Address or DNS name of the device, libreNMS stores the actual hostname in sysName.
        """

        return self._get("devices/" + str(hostname) + "/discover")
    
    def availability(self, hostname):
        """
        Get calculated availabilities of given device.

        Parameters:
            - hostname: either the device hostname or ID

        NOTE: hostname is the IP Address or DNS name of the device, libreNMS stores the actual hostname in sysName.        
        """

        return self._get("devices/" + str(hostname) + "/availability")
    
    def outages(self, hostname):
        """
        Get detected outages of given device.

        Parameters:
            - hostname: either the device hostname or ID

        NOTE: hostname is the IP Address or DNS name of the device, libreNMS stores the actual hostname in sysName.        
        """

        return self._get("devices/" + str(hostname) + "/outages")
    
    def get_components(self, hostname, component_type=None, component_id=None, component_label=None, component_status=None, component_disabled=None, component_ignore=None):
        """
        Get a list of components for a particular device.

        Parameters:
            - hostname: either the device hostname or ID
            - component_type: Filter the result by type (Equals).
            - component_id: Filter the result by id (Equals).
            - component_label: Filter the result by label (Contains).
            - component_status: Filter the result by status (Equals).
            - component_disabled: Filter the result by disabled (Equals).
            - component_ignore: Filter the result by ignore (Equals).
        """

        params = {
            "type": component_type, 
            "id": component_id,
            "label": component_label,
            "status": component_status,
            "disabled": component_disabled,
            "ignore": component_ignore
        }
        return self._get("devices/" + str(hostname) + "/components", params=params)
    
    def add_components(self, hostname, component_type):
        """
        Create a new component of a type on a particular device.

        Parameters: 
            - hostname: either the device hostname or ID
            - component_type: type of component to add. 
        
        """

        return self._post("devices/" + str(hostname) + "/components/" + str(component_type))
    
    def edit_components(self, ):
        ...

    def delete_components(self, ):
        ...

    def add_device(self, hostname, device_type="snmpv2c", **kwargs):
        """
        Add a device. 
        
        Parameters:
            - device_type: Monitoring method for a device. Can be icmp, snmpv1, snmpv2c, snmpv3
            - hostname: device hostname or IP
            - community: Required for snmpv2c. Community string to use.
        """

        # define parameter dictionaries
        required_params = {
            "icmp" : [],
            "snmpv1": ["community"],
            "snmpv2c": ["community"],
            "snmpv3": ["authlevel", "authname", "authpass", "authalgo", "cryptopass", "cryptoalgo"]
        }
        optional_params = {
            "icmp": ["os", "sys_name", "hardware", "force_add", "location", "poller_group", "display"],
            "snmpv1": ["port", "transport", "port_association_mode", "location", "force_add", "display"],
            "snmpv2c": ["port", "transport", "port_association_mode", "location", "force_add", "display"],
            "snmpv3": ["port", "transport", "port_association_mode", "location", "force_add", "display"],
        }
        data = {'hostname': hostname}
        # validation
        if device_type not in required_params.keys():
            raise Exception(f"Unknown device type {device_type}.")
        for param in required_params[device_type]:
            if param not in kwargs.keys():
                raise Exception(f"Missing parameter {param} for device type {device_type}.")
            else:
                data[param] = kwargs[param]
        for param in optional_params[device_type]:
            # ignore other parameters
            if param in kwargs.keys():
                data[param] = kwargs[param]
        if device_type == "icmp": 
            data["snmp_disable"] = "true"
        elif device_type == "snmpv1":
            data['snmpver'] = "v1"
        elif device_type == "snmpv2c":
            data["snmpver"] = "v2c"
        else: 
            data['snmpver'] = "v3"
        return self._post("devices", data=data)