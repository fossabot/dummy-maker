#!/usr/bin/env python

from uuid import uuid4
from optparse import OptionParser
import sys
import requests
import json
from time import sleep
import random
import string

parser = OptionParser()
parser.add_option("-n", "--number", dest="number", help="Number of devices to create", type="int")
parser.add_option("-d", "--dry-run", dest="dry_run", action="store_true", help="Just print what would happen -- no API calls", default=False)
parser.add_option("-k", "--api-key", dest="api_key", help="UA API key")
parser.add_option("-s", "--api-secret", dest="api_secret", help="UA API secret")
parser.add_option("-t", "--tags", dest="tag_string", help="Comma-delimited list of tags and probability of being assigned. (Example: beer:0.1,whiskey:0.5)", type="string")
parser.add_option("", "--delay", dest="delay", help="Sleep between requests. (In seconds. Can be a float.)", type="float")
parser.add_option("", "--api-host", dest="hostname", help="API host, defaults to production (https://go.urbanairship.com)", default="https://go.urbanairship.com")
parser.add_option("", "--random-tags", dest="random_tags", help="Generates a random list of tags and assigns them to a random number of devices. Format: num_tags:max_devices_per_tag:max_num_tags_per_device")
(options, args) = parser.parse_args()

if not options.number:
    print "Number is 0 or not set at all. Nothing to do!"
    parser.print_help()
    sys.exit(1)

random_tags = {}
if options.random_tags:
    (num_tags, max_devices_per_tag, max_num_tags_per_device) = options.random_tags.split(':')
    num_tags = int(num_tags)
    max_devices_per_tag = int(max_devices_per_tag)
    max_num_tags_per_device = int(max_num_tags_per_device)
    for i in xrange(num_tags):
        tag = ''.join(random.choice(string.ascii_uppercase) for x in range(10))
        random_tags[i] = {'tag': tag, 'count': 0}

has_tags = options.tag_string is not None

tag_dict = {}
if has_tags:
    tag_pairs = options.tag_string.split(',')
    for pair in tag_pairs:
        (tag, chance) = pair.split(':')
        tag_dict[tag] = float(chance)

def register_device(uuid, tag_string):
    if options.dry_run:
        print "--- Dry run, no registration made"
    else:
        r = requests.put(
                "%s/api/apids/%s" % (options.hostname, uuid),
                headers={'Content-type': 'application/json'},
                auth=(options.api_key, options.api_secret),
                data=tag_string)
        print r

for i in xrange(1, options.number + 1):
    uuid = uuid4()
    progress_info = '%s of %s: %s' % (i, options.number, uuid)
    data = {}

    tags = []
    rand = random.random()
    # Pre-defined tags
    for tag, chance in tag_dict.iteritems():
        if rand < chance:
            tags.append(tag)
    
    if options.random_tags:
        # Between 0 - n number of tags
        for j in xrange(random.randrange(max_num_tags_per_device)):
            tries = 0
            while tries < 10:
                random_tag_dict = random_tags[random.randrange(num_tags)]
                if random_tag_dict['count'] < max_devices_per_tag:
                    tags.append(random_tag_dict['tag'])
                    random_tag_dict['count'] = random_tag_dict['count'] + 1
                    break
                tries += 1

    if tags:
        data['tags'] = tags
        print '%s with tags "%s"' % (progress_info, tags)
    else:
        print '%s with no tags' % (progress_info)

    register_device(uuid, json.dumps(data))

    if options.delay:
        print "Sleeping %s seconds..." % options.delay
        sleep(options.delay)
