#!/usr/bin/env python

from uuid import uuid4
from optparse import OptionParser
import sys
import requests
import json
from time import sleep

APIHOST = "http://s0247:8003"

parser = OptionParser()
parser.add_option("-n", "--number", dest="number", help="Number of devices to create", type="int")
parser.add_option("-d", "--dry-run", dest="dry_run", action="store_true", help="Just print what would happen -- no API calls", default=False)
parser.add_option("-k", "--api-key", dest="api_key", help="UA API key")
parser.add_option("-s", "--api-secret", dest="api_secret", help="UA API secret")
parser.add_option("-t", "--tags", dest="tag_string", help="Comma-delimited list of tags", type="string")
parser.add_option("", "--delay", dest="delay", help="Sleep between requests. (In seconds. Can be a float.)", type="float")
(options, args) = parser.parse_args()

if not options.number:
    print "Number is 0 or not set at all. Nothing to do!"
    parser.print_help()
    sys.exit(1)

has_tags = options.tag_string is not None

def register_device(uuid, tag_string):
    if options.dry_run:
        print "--- Dry run, no registration made"
    else:
        r = requests.put(
                "%s/api/apids/%s" % (APIHOST, uuid),
                headers={'Content-type': 'application/json'},
                auth=(options.api_key, options.api_secret),
                data=tag_string)
        print r

    if options.delay:
        print "Sleeping %s seconds..." % options.delay
        sleep(options.delay)

for i in range(1, options.number + 1):
    uuid = uuid4()
    progress_info = '%s of %s: %s' % (i, options.number, uuid)
    data = {}
    if has_tags:
        data['tags'] = options.tag_string.split(',')
        print '%s with tags "%s"' % (progress_info, options.tag_string)
    else:
        print '%s with no tags' % (progress_info)

    register_device(uuid, json.dumps(data))
