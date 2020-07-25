# Copyright 2020 James Arcus <jimbo@ucc.asn.au>.
# Released under the terms of the GNU GPLv3 or later.

################################################################################

from . import endpoints

################################################################################

# Query helpers

def LOOKUP_ONCE(seq, key):
    if len(seq) == 0:
        return None
    elif len(seq) == 1:
        return seq[0][key]
    else:
        raise ValueError("Multiple results: " + repr(seq))

def SET_UNLESS_NONE(map, key, value):
    if value is not None:
        map[key] = value

################################################################################

# API actions

def get_zone_id(token, zone_name):
    result = endpoints.list_zones(token, {"name": zone_name})
    return LOOKUP_ONCE(result, "id")

def list_all_records(token, zone_id):
    return endpoints.list_dns_records(token, zone_id)

def create_record(token, zone_id,
    record_name, record_type, record_content,
    record_ttl=1, record_priority=None, record_proxied=None):
    
    details = {
        "name": record_name,
        "type": record_type,
        "content": record_content,
        "ttl": record_ttl,
    }

    SET_UNLESS_NONE(details, "priority", record_priority)
    SET_UNLESS_NONE(details, "proxied", record_proxied)

    return endpoints.create_dns_record(token, zone_id, details)

def get_record_id(token, zone_id, record_name, record_type='A'):
    query = {
        "name": record_name,
        "type": record_type,
    }

    result = endpoints.list_dns_records(token, zone_id, query)
    return LOOKUP_ONCE(result, "id")

def change_record(token, zone_id, record_id,
    record_name=None, record_type=None, record_content=None,
    record_ttl=None, record_proxied=None):
    
    changes = {}

    SET_UNLESS_NONE(changes, "name", record_name)
    SET_UNLESS_NONE(changes, "type", record_type)
    SET_UNLESS_NONE(changes, "content", record_content)
    SET_UNLESS_NONE(changes, "ttl", record_ttl)
    SET_UNLESS_NONE(changes, "proxied", record_proxied)

    return endpoints.patch_dns_record(token, zone_id, record_id, changes)

def delete_record(token, zone_id, record_id):
    return endpoints.delete_dns_record(token, zone_id, record_id)