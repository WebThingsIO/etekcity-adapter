"""Etekcity adapter for Mozilla WebThings Gateway."""

from gateway_addon import Adapter, Database
from pyvesync.vesync import VeSync

from .etekcity_device import EtekcityDevice


_TIMEOUT = 3


class EtekcityAdapter(Adapter):
    """Adapter for Etekcity smart home devices."""

    def __init__(self, verbose=False):
        """
        Initialize the object.

        verbose -- whether or not to enable verbose logging
        """
        self.name = self.__class__.__name__
        Adapter.__init__(self,
                         'etekcity-adapter',
                         'etekcity-adapter',
                         verbose=verbose)

        self.manager = None

        database = Database(self.package_name)
        if database.open():
            config = database.load_config()

            if 'username' in config and len(config['username']) > 0 and \
                    'password' in config and len(config['password']) > 0:
                self.manager = VeSync(config['username'], config['password'])
                self.manager.login()

            database.close()

        self.pairing = False
        self.start_pairing(_TIMEOUT)

    def start_pairing(self, timeout):
        """
        Start the pairing process.

        timeout -- Timeout in seconds at which to quit pairing
        """
        if self.manager is None or self.pairing:
            return

        self.pairing = True

        self.manager.update()
        for dev in self.manager.devices:
            if not self.pairing:
                break

            _id = 'etekcity-' + dev.uuid
            if _id not in self.devices:
                device = EtekcityDevice(self, _id, dev)
                self.handle_device_added(device)

        self.pairing = False

    def cancel_pairing(self):
        """Cancel the pairing process."""
        self.pairing = False
