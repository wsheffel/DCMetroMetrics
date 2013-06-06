#!/usr/bin/env python
import imp
import os
import sys
import subprocess
import argparse

PY_DIR = os.environ['OPENSHIFT_PYTHON_DIR']
REPO_DIR = os.environ['OPENSHIFT_REPO_DIR']
SCRIPT_DIR = os.path.join(REPO_DIR, 'scripts')
DATA_DIR = os.environ['OPENSHIFT_DATA_DIR']

try:
   zvirtenv = os.path.join(PY_DIR, 'virtenv', 'bin', 'activate_this.py')
   execfile(zvirtenv, dict(__file__ = zvirtenv) )
except IOError:
   pass

# Import modules
import gevent
from gevent import Greenlet
from gevent import monkey; monkey.patch_all() # Needed for bottle

# Import application modules
sys.path.append(SCRIPT_DIR)
from runTwitterApp import TwitterApp
from hotCarApp import HotCarApp

#################################################
# Run the bottle app in a greenlet 
class BottleApp(Greenlet):

    def __init__(self):
        Greenlet.__init__(self)
        # Load the bottleApp module
        self.bottleAppPath = os.path.join(REPO_DIR,'wsgi', 'bottleApp.py')
        self.bottleApp = imp.load_source('bottleApp', self.bottleAppPath)

    def _run(self):
        try:
            # Run the server. Note: This call blocks
            ip   = os.environ['OPENSHIFT_INTERNAL_IP']
            port = 8080
            bottle = self.bottleApp.application
            bottle.run(host=ip, port=port, server='gevent')
        except Exception as e:
            logName = os.path.join(DATA_DIR, 'bottle.log')
            fout = open(logName, 'a')
            fout.write('Caught Exception while running bottle! %s\n'%(str(e)))
            fout.close()

def run(LIVE=False):

   # Load the bottleApp module
   #bottleAppPath = os.path.join(REPO_DIR,'wsgi', 'bottleApp.py')
   #bottleApp = imp.load_source('bottleApp', bottleAppPath)

   # Run MetroEsclaators twitter App
   twitterApp = TwitterApp(LIVE=LIVE)
   twitterApp.start()

   # Run HotCar twitter app
   hotCarApplication = HotCarApp(LIVE=LIVE)
   hotCarApplication.start()

   # Run the server. Note: This call blocks
   #bottle = bottleApp.application
   #bottle.run(host=ip, port=port, server='gevent')
   bottleApp = BottleApp()
   bottleApp.start()

   twitterApp.join()
   hotCarApplication.join()
   bottleApp.join()

if __name__ == '__main__':
    run(LIVE=True)
