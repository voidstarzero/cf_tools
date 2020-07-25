# Copyright 2020 James Arcus <jimbo@ucc.asn.au>.
# Released under the terms of the GNU GPLv3 or later.

################################################################################

import cf_driver

import os
import sys

################################################################################

def update_record_address(token, zone_id, host_id, address):
	pass

def usage():
	text = ("""dns_updater.py - Update a dynamic DNS entry

usage: python3 dns_updater.py 192.0.2.35

Required environment variables:
- CF_TOKEN: Your Cloudflare API token
- CF_ZONE_ID or CF_ZONE_NAME: The id or name of the target zone
- CF_RECORD_ID or CF_RECORD_NAME: The id or full name of the target record""")

	print(text, file=sys.stderr)

def run():
	if len(sys.argv) != 2:
		usage()
		exit(1)

	address = sys.argv[1]

	token = os.environ['CF_TOKEN']

	zone_id = os.environ.get('CF_ZONE_ID')
	if zone_id is None:
		zone_name = os.environ['CF_ZONE_NAME']
		zone_id = cf_driver.get_zone_id(token, zone_name)

	record_id = os.environ.get('CF_RECORD_ID')
	if record_id is None:
		record_name = os.environ['CF_RECORD_NAME']
		record_id = cf_driver.get_record_id(token, zone_id, record_name)

	if record_id is None: # returns None if not existant
		cf_driver.create_record(token, zone_id, 'A', record_name, address)
		print(f"Created A record for {record_name} -> {address}")
	else:
		cf_driver.change_record(token, zone_id, record_id, record_content=address)
		print(f"Updated A record for {record_name} -> {address}")

if __name__ == "__main__":
	run()