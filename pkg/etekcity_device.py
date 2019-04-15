"""Etekcity adapter for Mozilla WebThings Gateway."""

from gateway_addon import Device
import threading
import time

from .etekcity_property import EtekcityProperty


_POLL_INTERVAL = 5


class EtekcityDevice(Device):
    """Etekcity device type."""

    def __init__(self, adapter, _id, vesync_dev):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        _id -- ID of this device
        vesync_dev -- the vesync device object to initialize from
        """
        Device.__init__(self, adapter, _id)
        self._type = ['OnOffSwitch', 'EnergyMonitor']
        self.type = 'onOffSwitch'

        self.vesync_dev = vesync_dev
        self.name = vesync_dev.device_name
        self.description = vesync_dev.device_type
        if not self.name:
            self.name = self.description

        if vesync_dev.device_type != 'ESWL01':
            self._type.append('SmartPlug')

        self.properties['on'] = EtekcityProperty(
            self,
            'on',
            {
                '@type': 'OnOffProperty',
                'label': 'On/Off',
                'type': 'boolean',
            },
            self.on)

        self.properties['power'] = EtekcityProperty(
            self,
            'power',
            {
                '@type': 'InstantaneousPowerProperty',
                'label': 'Power',
                'type': 'number',
                'unit': 'Watt',
                'readOnly': True,
            },
            self.power)

        self.properties['voltage'] = EtekcityProperty(
            self,
            'voltage',
            {
                '@type': 'VoltageProperty',
                'label': 'Voltage',
                'type': 'number',
                'unit': 'volt',
                'readOnly': True,
            },
            self.voltage)

        if vesync_dev.device_type in ['ESW15-USA', 'ESW01-EU']:
            self.properties['nightLightMode'] = EtekcityProperty(
                self,
                'nightLightMode',
                {
                    'label': 'Night Light Mode',
                    'type': 'string',
                    'enum': ['auto', 'manual'],
                },
                self.night_light_mode)

        t = threading.Thread(target=self.poll)
        t.daemon = True
        t.start()

    def poll(self):
        """Poll the device for changes."""
        while True:
            time.sleep(_POLL_INTERVAL)
            self.vesync_dev.update()

            for prop in self.properties.values():
                prop.update()

    @property
    def on(self):
        """Determine whether or not the device is on."""
        return self.vesync_dev.device_status == 'on'

    @property
    def power(self):
        """Determine current power usage."""
        return self.vesync_dev.power()

    @property
    def voltage(self):
        """Determine current voltage."""
        return self.vesync_dev.voltage()

    @property
    def night_light_mode(self):
        """Determine the night light mode."""
        return self.vesync_dev.details['night_light_automode']
