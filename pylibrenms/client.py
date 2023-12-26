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
        if params is None: params = {}
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
        
    def _patch(self, route, data=None):
        """
        PATCH call to be used by endpoints.
        """
        endpoint = self.url + route
        if data is None: data = {}
        try:
            response = requests.patch(endpoint, headers=self._headers, json=data)
            return response.json()
        except requests.exceptions.RequestException as e:
            # TODO: implement exception here
            raise Exception(f"Error occurred, {e}")              
        
    def _post(self, route, data=None):
        """
        POST call to be used by endpoints.
        """
        endpoint = self.url + route
        if data is None: data = {}
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
        if data is None: data = {}
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

    def ports_with_associated_mac(self, mac, search_filter=None):
        """
        Search for ports matching the search mac.

        Parameters:
            mac: MAC Address to search for
            search_filter: Add filter to the search. Optional.
        """
        params = {
            "filter": search_filter
        }

        return self._get("ports/mac/" + str(mac), params=params)

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
            - hostname: (all, required) device hostname or IP
            - display: (all, optional) A string to display as the name of the device, defaults to hostname
            - port: (snmpv1, snmpv2c, snmpv3, optional) SNMP port, defaults to port defined in config
            - transport: (snmpv1, snmpv2c, snmpv3, optional) SNMP protocol, defaults to transport defined in config
            - community: (snmpv1, snmpv2c, required) Community string to use.
            - authlevel: (snmpv3, required) SNMP Authlevel, can be `noAuthNoPriv`, `authNoPriv`, `authPriv`
            - authname: (snmpv3, required) Auth username
            - authpass: (snmpv3, required) Auth password
            - authalgo: (snmpv3, required) Auth algorithm, can be `MD5`, `SHA`, `SHA-224`, `SHA-256`, `SHA-384`, `SHA-512`
            - cryptopass: (snmpv3, required) SNMP crypto password
            - cryptoalgo: (snmpv3, required) SNMP crypto algorithm, can be `AES`, `DES`
            - os: (icmp, optional) OS short name for the device
            - sysName: (icmp, optional) sysName for the device
            - hardware: (icmp, optional) device hardware
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
        # handle snmpver
        if device_type == "icmp": 
            data["snmp_disable"] = "true"
        elif device_type == "snmpv1":
            data['snmpver'] = "v1"
        elif device_type == "snmpv2c":
            data["snmpver"] = "v2c"
        else: 
            data['snmpver'] = "v3"
        return self._post("devices", data=data)
    
    def list_oxidized(self, hostname=None):
        """
        List devices for used with Oxidized

        Parameters:
            - hostname: Hostname or device IP. Optional.
        """

        if not hostname: hostname = ""
        return self._get("oxidized/" + str(hostname))
    
    def rename_device(self, hostname, new_hostname):
        """
        Rename a device. 
        
        WARNING: This changes the actual hostname, not the display name. Be sure you actually want this. 
        Parameters:
            - hostname: device hostname or ID
            - new_hostname: new device hostname
        """
        
        return self._patch("devices/" + str(hostname) + "/rename/" + str(new_hostname))
    

    def get_port_stack(self, hostname, valid_mappings=False):
        """
        Get a list of port mappings for a device. This is useful for 
        showing physical ports that are in a virtual port-channel.

        Parameters:
            - hostname: can be either the device hostname or id
            - valid_mappings (Optional): Filter the result by only showing valid mappings ("0" values not shown).
        """

        if valid_mappings:
            return self._get("devices/" + str(hostname) + "/port_stack", params={"valid_mappings": ""})
        return self._get("devices/" + str(hostname) + "/port_stack")
    
    def get_device_groups(self, hostname):
        """
        List the device groups that a device is matched on.

        Parameters:
            - hostname: either the device hostname or id
        """

        return self._get("devices/" + str(hostname) + "/groups")
    
    def add_parents_to_host(self, hostname, parent_ids):
        """
        Add one or more parents to a host.

        Parameters
            - hostname: either the device hostname or id
            - parent_ids: a list of parent ids or hostnames, or a single string for a single parent.
        """

        # TODO: Implement check for parent to be either a list or some sort of iterable?
        if isinstance(parent_ids, list):
            parent_ids = ','.join(map(str, parent_ids))
        data = {"parent_ids": parent_ids}
        return self._post("devices/" + str(hostname) + "/parents", data=data)

    def delete_parents_from_host(self,):
        ...

    def get_inventory(self, hostname, ent_physical_class=None, ent_physical_contained_in=None):
        """
        Retrieve the inventory for a device. 
        
        Parameters:
            - hostname: either the device hostname or the device id
            - entPhysicalClass (Optional) restrict the class of the inventory
            - entPhysicalContainedIn (Optional) retrieve items within the inventory assigned to a previous component
        """

        params = {
            "entPhysicalClass": ent_physical_class,
            "entPhysicalContainedIn" : ent_physical_contained_in
        }
        return self._get("inventory/" + str(hostname), params=params)    

    def get_inventory_for_device(self, hostname):
        """
        Retrieve the flattened inventory for a device
        
        Parameters:
            - hostname: either the device hostname or the device id
        """

        return self._get("inventory/" + str(hostname) + "/all")    
    
    def get_graphs(self, hostname):
        """
        Get a list of available graphs for a device, this does not include ports.

        Parameters:
            - hostname: either the device hostname or id
        """

        return self._get("devices/" + str(hostname) + "/graphs")
    
    def system(self):
        """
        Display Librenms instance information.        
        """

        return self._get("system")
    
    def list_available_health_graphs(self, hostname, health_type=None, sensor_id=None):
        """
        Get a list of overall health graphs available, or get a list of health graphs based on provided class, or get the health sensors information based on ID.

        Parameters:
            - hostname: either the device hostname or id
            - health_type: Optional. Health type / sensor class
            - sensor_id: Optional. Sensor id to retrieve specific information
        """

        route = "devices/" + str(hostname) + "/health/"
        if health_type:
            route += str(health_type) + "/"
        if sensor_id:
            route += str(sensor_id)
        return self._get(route)

    def list_locations(self):
        """
        Return a list of locations.
        """

        return self._get("resources/locations")
    
    def add_location(self, location_name, latitude=None, longitude=None, fixed_coordinates=None):
        """
        Add a new location.

        Parameters:
            - location_name: Name of the location
            - latitude: latitude
            - longitude: longitude
            - fixed_coordinates: 0 if updated from the device or 1 if the coordinate is fixed
        """

        data = {
            "location": location_name,
            "lat": latitude if latitude else "None",
            "lng": longitude if longitude else "None",
            "fixed_coordinates": fixed_coordinates
        }
        return self._post("locations", data=data)
    

    def delete_location(self, location_name):
        """
        Deletes an existing location. 

        Parameters:
            - location_name: name or ID of the location to delete. 
        """

        return self._delete("locations/" + str(location_name))
    

    def edit_location(self, location_name, latitude=None, longitude=None): 
        """
        Edit a location.

        Parameters:
            - location_name: name or ID of the location to edit
            - latitude: latitude
            - longitude: longitude
        """
        
        data = {}
        if latitude is not None:
            data['lat'] = latitude
        if longitude is not None:
            data['lng'] = longitude
        return self._patch("locations/" + str(location_name), data=data)

    def get_location(self, location_name):
        """
        Gets a specific location

        Parameters:
            - location_name: name or id of the location to get
        """

        return self._get("location/" + str(location_name))