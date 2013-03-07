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
                            Comma-delimited list of tags
      --delay=DELAY         Sleep between requests. (In seconds. Can be a float.)

Example
-----------

I want to create 10 APIDs with the tags "whiskey,beer" while sleeping for a half second
between each API call.

.. sourcecode:: bash

    ./dummy-maker/dummy.py --number=10 --tags=whiskey,beer --delay=0.5

