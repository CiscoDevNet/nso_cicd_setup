# This PyATS test script loops over the devices in the testbed
# and executes ping tests on each device to the destination 
# IP addresses listed in the file specified by the --targets 
# command line argument. See "ping_targets.yaml" for the 
# structure. 
#
# Usage:
# python pyats_pingtest.py --testbed testbed.yaml --targets ping_targets.yaml 

import re
import logging
import yaml
import argparse
import sys
from pyats import aetest
from pyats.topology import loader

logger = logging.getLogger('AETEST')
logger.setLevel(logging.DEBUG)

class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def get_devices(self, testbed):
        self.parent.parameters.update(testbed = testbed)
        # Mark establish_connections method for looping. 
        # Loops over each device object in the testbed.
        aetest.loop.mark(self.establish_connections, device=testbed)
    
    @aetest.subsection
    def establish_connections(self, steps, device):
        with steps.start(f"Connecting to {device.name}"):
            logger.info(f"Connecting to device {device.name}")
            device.connect()

    @aetest.subsection
    def load_ping_targets(self, targets):
        # Loads a YAML file describing ping destinations and saves as a parameter
        with open(targets, 'r') as f:
            ping_targets = yaml.safe_load(f)
        self.parent.parameters.update(ping_targets = ping_targets)
    
@aetest.loop(device=('core-rtr01', 'core-rtr02', 'dist-rtr01', 'dist-rtr02'))
class PingTestCase(aetest.Testcase):
    
    @aetest.setup
    def setup(self, device):
        # Mark ping method for looping.  
        aetest.loop.mark(self.ping, destination=self.parent.parameters['ping_targets'][device])

    @aetest.test
    def ping(self, device, destination):
        current_device = self.parent.parameters['testbed'].devices[device]
        logger.info(f"Ping from {current_device.name} to {destination}")
        try:
            result = current_device.ping(destination)
        except Exception as e:
            self.failed(f"Ping {destination} from device {current_device.name} failed with error {e}", goto = ['exit'])
        else:
            match = re.search(r'Success rate is (?P<rate>\d+) percent', result)
            success_rate = match.group('rate')

            logger.info(f"Ping {destination} from device {current_device.name} with success rate of {success_rate}")

class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def setup(self, testbed):
        aetest.loop.mark(self.disconnect, device=testbed)

    @aetest.subsection
    def disconnect(self, steps, device):
        with steps.start(f"Disconnecting from {device.name}"):
            logger.info(f"Disconnecting from device {device.name}")
            device.disconnect()

            
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest = 'testbed', type = loader.load)
    parser.add_argument('--targets', dest = 'targets', required = True)
    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
