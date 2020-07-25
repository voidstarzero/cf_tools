# Copyright 2020 James Arcus <jimbo@ucc.asn.au>.
# Released under the terms of the GNU GPLv3 or later.

################################################################################

import cf_driver

import os
import sys

################################################################################

def usage():
	text = ("""gateway_repoint.py - Point a set of records at a single gateway

usage: python3 gateway_repoint.py cf-gateway.example.com < fqdns.list

Required environment variables:
- CF_TOKEN: Your Cloudflare API token
- CF_ZONE_ID or CF_ZONE_NAME: The id or name of the target zone""")

	print(text, file=sys.stderr)
	exit(1)

def run():
	if len(sys.argv) != 2:
		usage()

	gateway = sys.argv[1]

	try:
		token = os.environ['CF_TOKEN']
	except KeyError:
		usage()

	zone_id = os.environ.get('CF_ZONE_ID')
	if zone_id is None:
		try:
			zone_name = os.environ['CF_ZONE_NAME']
		except KeyError:
			usage()

		zone_id = cf_driver.get_zone_id(token, zone_name)

	if zone_id is None: # Doesn't match anything existing
		print(f"No matching zone for {zone_name}, does it exist?", file=sys.stderr)
		exit(1)

	for line in sys.stdin:
		record_name = line.strip()

		# Is there a single CNAME for this record name already?
		try:
			record_id = cf_driver.get_record_id(token, zone_id, record_name, 'CNAME')
		except ValueError: # Multiple exist
			record_id = None

		if record_id is None:
			# Need to clear out excess records (e.g. A, AAAA)
			record_ids = cf_driver.query_record_ids(token, zone_id, record_name)

			print(f"Found existing records for {record_name}, clearing...", record_ids)
			for record_id in record_ids:
				cf_driver.delete_record(token, zone_id, record_id)

			cf_driver.create_record(token, zone_id, record_name, 'CNAME',
				record_content=gateway, record_proxied=True)
			print(f"Created new proxy CNAME for {record_name} -> {gateway}")
		
		else:
			cf_driver.change_record(token, zone_id, record_id,
				record_content=gateway, record_proxied=True)
			print(f"Proxying CNAME for {record_name} -> {gateway}")

if __name__ == "__main__":
	run()