"""Etekcity adapter for Mozilla WebThings Gateway."""

from gateway_addon import Device
import threading
import time

from .etekcity_property import (
    EtekcityBulbProperty,
    EtekcityOutletProperty,
    EtekcitySwitchProperty,
)


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

        self.vesync_dev = vesync_dev
        self.name = vesync_dev.device_name
        self.description = vesync_dev.device_type
        if not self.name:
            self.name = self.description

        # All devices have this property
        self.properties['on'] = EtekcitySwitchProperty(
            self,
            'on',
            {
                '@type': 'OnOffProperty',
                'title': 'On/Off',
                'type': 'boolean',
            },
            self.on)

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


class EtekcityBulb(EtekcityDevice):
    """Etekcity bulb type."""

    def __init__(self, adapter, _id, vesync_dev):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        _id -- ID of this device
        vesync_dev -- the vesync device object to initialize from
        """
        EtekcityDevice.__init__(self, adapter, _id, vesync_dev)

        self._type = ['OnOffSwitch', 'Light']

        if vesync_dev.dimmable_feature:
            self.properties['brightness'] = EtekcityBulbProperty(
                self,
                'brightness',
                {
                    '@type': 'BrightnessProperty',
                    'title': 'Brightness',
                    'type': 'integer',
                    'unit': 'percent',
                    'minimum': 1,
                    'maximum': 100,
                },
                self.brightness
            )

        if vesync_dev.color_temp_feature:
            self._type.append('ColorControl')
            self.properties['colorTemperature'] = EtekcityBulbProperty(
                self,
                'colorTemperature',
                {
                    '@type': 'ColorTemperatureProperty',
                    'title': 'Color Temperature',
                    'type': 'integer',
                    'unit': 'kelvin',
                    'minimum': 2700,
                    'maximum': 6500,
                },
                self.color_temp
            )

    @property
    def brightness(self):
        """Determine current brightness."""
        return self.vesync_dev.brightness

    @property
    def color_temp(self):
        """Determine current color temperature."""
        return self.vesync_dev.color_temp_kelvin


class EtekcityOutlet(EtekcityDevice):
    """Etekcity outlet type."""

    def __init__(self, adapter, _id, vesync_dev):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        _id -- ID of this device
        vesync_dev -- the vesync device object to initialize from
        """
        EtekcityDevice.__init__(self, adapter, _id, vesync_dev)

        self._type = ['OnOffSwitch', 'EnergyMonitor', 'SmartPlug']

        self.properties['power'] = EtekcityOutletProperty(
            self,
            'power',
            {
                '@type': 'InstantaneousPowerProperty',
                'title': 'Power',
                'type': 'number',
                'unit': 'watt',
                'readOnly': True,
            },
            self.power
        )

        self.properties['voltage'] = EtekcityOutletProperty(
            self,
            'voltage',
            {
                '@type': 'VoltageProperty',
                'title': 'Voltage',
                'type': 'number',
                'unit': 'volt',
                'readOnly': True,
            },
            self.voltage
        )

        if vesync_dev.device_type in ['ESW15-USA', 'ESW01-EU']:
            self.properties['nightLightMode'] = EtekcityOutletProperty(
                self,
                'nightLightMode',
                {
                    'title': 'Night Light Mode',
                    'type': 'string',
                    'enum': ['auto', 'manual'],
                },
                self.night_light_mode
            )

    @property
    def power(self):
        """Determine current power usage."""
        return self.vesync_dev.power

    @property
    def voltage(self):
        """Determine current voltage."""
        return self.vesync_dev.voltage

    @property
    def night_light_mode(self):
        """Determine the night light mode."""
        return self.vesync_dev.details['night_light_automode']


class EtekcitySwitch(EtekcityDevice):
    """Etekcity switch type."""

    def __init__(self, adapter, _id, vesync_dev):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        _id -- ID of this device
        vesync_dev -- the vesync device object to initialize from
        """
        EtekcityDevice.__init__(self, adapter, _id, vesync_dev)

        self._type = ['OnOffSwitch']

        if vesync_dev.is_dimmable():
            self._type.append('MultiLevelSwitch')
            self.properties['level'] = EtekcitySwitchProperty(
                self,
                'level',
                {
                    '@type': 'LevelProperty',
                    'title': 'Level',
                    'type': 'integer',
                    'unit': 'percent',
                    'minimum': 1,
                    'maximum': 100,
                },
                self.level
            )

    @property
    def level(self):
        """Determine current level."""
        return self.vesync_dev.brightness
