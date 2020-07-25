# Copyright 2020 James Arcus <jimbo@ucc.asn.au>.
# Released under the terms of the GNU GPLv3 or later.

################################################################################

from . import methods

################################################################################

# API endpoints

def list_zones(token, query=None):
    return methods.get(token, "/zones", query)

def zone_details(token, zone_id):
    return methods.get(token, f"/zones/{zone_id}")

def list_dns_records(token, zone_id, query=None):
    return methods.get(token, f"/zones/{zone_id}/dns_records", query)

def create_dns_record(token, zone_id, data):
    return methods.post(token, f"/zones/{zone_id}/dns_records", data)

def dns_record_details(token, zone_id, record_id):
    return methods.get(token, f"/zones/{zone_id}/dns_records/{record_id}")

def update_dns_record(token, zone_id, record_id, data):
    return methods.put(token, f"/zones/{zone_id}/dns_records/{record_id}", data)

def patch_dns_record(token, zone_id, record_id, data):
    return methods.patch(token, f"/zones/{zone_id}/dns_records/{record_id}", data)

def delete_dns_record(token, zone_id, record_id):
    return methods.delete(token, f"/zones/{zone_id}/dns_records/{record_id}")