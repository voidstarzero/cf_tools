# Copyright 2020 James Arcus <jimbo@ucc.asn.au>.
# Released under the terms of the GNU GPLv3 or later.

################################################################################

import cf_driver

import os
import sys

################################################################################

def usage():
	text = ("""zone_loder.py - Import a zone from a cleaned BIND-style zonefile

usage: python3 zone_loder.py path/to/zonefile.domain

*Compatible only with A, AAAA and CNAME records without explicit TTLs.*

Required environment variables:
- CF_TOKEN: Your Cloudflare API token
- CF_ZONE_ID or CF_ZONE_NAME: The id or name of the target zone""")

	print(text, file=sys.stderr)
	exit(1)

def run():
	if len(sys.argv) != 2:
		usage()

	with open(sys.argv[1]) as zonefile:
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

		# Now we know the zone, time to run the import
		record_name = ""

		for line in zonefile:
			fields = [s for s in line.split() if s]

			if len(fields) == 4: # hostname	IN	A	192.0.2.12
				record_name, _, record_type, record_content = fields
			elif len(fields) == 3: #	IN	A	192.0.2.13
				_, record_type, record_content = fields

			print(f"Adding '{record_type}' record for {record_name} -> {record_content}")
			cf_driver.create_record(token, zone_id, record_name, record_type, record_content)


if __name__ == "__main__":
	run()