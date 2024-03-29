"""
Client for LibreNMS
"""
import requests
import json
import logging

class Librenms:

    def __init__(self, base_url, api_key, verify_ssl):
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
        self._verify = verify_ssl

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
            response = requests.get(endpoint, headers=self._headers, params=params,verify=self._verify)
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
            response = requests.patch(endpoint, headers=self._headers, json=data, verify=self._verify)
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
            response = requests.post(endpoint, headers=self._headers, json=data, verify=self._verify)
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
            response = requests.delete(endpoint, headers=self._headers, json=data, verify=self._verify)
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
    
    def get_devicegroups(self):
        """
        List all device groups.

        Not to be confused with get_device_groups(), which gets the groups belonging only to a single device.
        """

        return self._get("devicegroups/")
    
    def add_devicegroup(self, group_name, group_type, description=None, rules=None, devices=None):
        """
        Add a new device group. Upon success, the ID of the new device group is returned and the HTTP response code is 201.

        Parameters:
            - group_name: (all, required) The name of the device group
            - group_type: (all, required) should be static or dynamic. Setting this to static requires that the devices input be provided
            - description(all, optional) Description of the device group
            - rules: (dynamic, required)  required if type == dynamic - A set of rules to determine which devices should be included in this device group
            - devices: (static, required) required if type == static - A list of devices that should be included in this group. This is a static list of devices
        """

        data = {
            "name": group_name, 
            "description": description,
            "type": group_type
        }
        if group_type == "static":
            if devices is None or rules is not None:
                raise Exception("Devices must be set, rules cannot be set for STATIC group type.")
            data["devices"] = devices
        elif group_type == "dynamic":
            if rules is None or devices is not None:
                raise Exception("rules must be set, Devices cannot be set for DYNAMCI group type.")
            data["rules"] = rules
        else:
            raise Exception(f"Unknown group type {group_type}")
        return self._post("devicegroups", data=data)
    
    def get_devices_by_group(self, group_name, full=None):
        """
        List all devices matching the group provided.

        Parameters:
            - group_name: The name of the device group which can be obtained using get_devicegroups
            - full: Set to True to enable full return of device information
        """
        params = {}
        if full:
            params["full"] = full
        return self._get("devicegroups/" + str(group_name), params=params)

    def maintenance_devicegroup(self, group_name, duration, title=None, notes=None, start=None):
        """
        Set a device group into maintenance mode.

        Parameters:
            - group_name: The name of the device group which can be obtained using get_devicegroups
            - title: (Optional) Some title for the Maintenance
            - notes: (Optional) Some description for the Maintenance
            - start: (Optional) start time of Maintenance in full format Y-m-d H:i:00 eg: 2022-08-01 22:45:00
            - duration (Required) Duration of Maintenance in format H:i / Hrs:Mins eg: 02:00
        """

        data = {
            "title": title,
            "notes": notes,
            "start": start,
            "duration": duration
        }
        return self._post("devicegroups/" + str(group_name) + "/maintenance", data=data)

    def list_bgp(self, hostname=None, asn=None, remote_asn=None, remote_address=None, local_address=None, 
                 bgp_descr=None, bgp_state=None, bgp_adminstate=None, bgp_family=None):
        """
        List current BGP sessions.
        All parameters are optional.

        Parameters:
            - hostname: Either the devices hostname or ID
            - asn: The local ASN you would like to filter by
            - remote_asn: Filter by remote peer ASN
            - remote_address: Filter by remote peer address
            - local_address: Filter by local address
            - bgp_descr: Filter by BGP neighbor description
            - bgp_state: Filter by BGP session state (like established,idle...)
            - bgp_adminstate: Filter by BGP admin state (start,stop,running...)
            - bgp_family: Filter by BGP address Family (4,6)        
        """

        params = {
            "hostname": hostname,
            "asn": asn,
            "remote_asn": remote_asn,
            "remote_address": remote_address,
            "local_address": local_address,
            "bgp_descr": bgp_descr,
            "bgp_state": bgp_state,
            "bgp_adminstate": bgp_adminstate,
            "bgp_family": bgp_family
        }
        return self._get("bgp", params=params)
    
    def get_bgp(self, bgp_id):
        """
        Retrieves a BGP session by ID

        Parameters:
            - bgp_id: bgp ID
        """

        return self._get("bgp/" + str(bgp_id))
    
    def list_devices(self, device_type, query=None):
        """
        Returns a list of devices.

        Parameters:
            type: can be one of the following to filter or search by:
                filters:
                    all: All devices
                    active: Only not ignored and not disabled devices
                    ignored: Only ignored devices
                    up: Only devices that are up
                    down: Only devices that are down
                Searchable:
                    os: search by os type
                    mac: search by mac address
                    ipv4: search by IPv4 address
                    ipv6: search by IPv6 address (compressed or uncompressed)
                    location: search by location
                    location_id: serach by locaiton_id
                    hostname: search by hostname
                    sysName: search by sysName
                    display: search by display name
                    device_id: exact match by device-id
                    type: search by device type
        """

        if device_type in ["all", "active", "ignored", "up", "down"] and query is not None:
            raise Exception(f"Device type {device_type} cannot have a query string.")
        elif device_type in ["os", "mac", "ipv4", "ipv6", "location", 
                             "location_id", "hostname", "sysName", "display", "device_id", "type"] and query is None:
            raise Exception(f"Device type {device_type} needs a query string.")
        params = {
            "type": device_type,
            "query": query
        }
        return self._get("devices", params=params)