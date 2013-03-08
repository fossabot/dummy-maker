========
dummy-maker
========

Quick script that registers a bunch of dummy Android apids.

Development
============

I'm assuming you have virtualenv and pip. If not, `brew install` those things.

.. sourcecode:: bash

    git clone git@github.com:urbanairship/dummy-maker.git
    cd dummy-maker
    . bin/activate
    pip install -r requirements.txt


Running
-------------

::

    Usage: dummy.py [options]
    
    Options:
      -h, --help            show this help message and exit
      -n NUMBER, --number=NUMBER
                            Number of devices to create
      -d, --dry-run         Just print what would happen -- no API calls
      -k API_KEY, --api-key=API_KEY
                            UA API key
      -s API_SECRET, --api-secret=API_SECRET
                            UA API secret
      -t TAG_STRING, --tags=TAG_STRING
                            Comma-delimited list of tags and probability of being
                            assigned. (Example: beer:0.1,whiskey:0.5)
      --delay=DELAY         Sleep between requests. (In seconds. Can be a float.)
      --api-host=HOSTNAME   API host, defaults to production
                               (https://go.urbanairship.com)
      --random-tags=RANDOM_TAGS 
                            Generates a random list of tags and assigns them to a
                            random number of devices. Format:
                            num_tags:max_devices_per_tag:max_num_tags_per_device


Example
-----------

I want to create 1000 APIDs with 200 of them getting tagged "whiskey", and 400 getting tagged "beer" while sleeping for a half second
between each API call.

.. sourcecode:: bash

    ./dummy-maker/dummy.py --number=1000 --tags=whiskey:0.2,beer:0.4 --delay=0.5 --api-key=YOURKEY --api-secret=YOURSECRET

