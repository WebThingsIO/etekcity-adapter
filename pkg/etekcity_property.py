"""Etekcity adapter for Mozilla WebThings Gateway."""

from gateway_addon import Property


class EtekcityProperty(Property):
    """Etekcity property type."""

    def __init__(self, device, name, description, value):
        """
        Initialize the object.

        device -- the Device this property belongs to
        name -- name of the property
        description -- description of the property, as a dictionary
        value -- current value of this property
        """
        Property.__init__(self, device, name, description)
        self.set_cached_value(value)


class EtekcityBulbProperty(EtekcityProperty):
    """Etekcity bulb property type."""

    def set_value(self, value):
        """
        Set the current value of the property.

        value -- the value to set
        """
        if self.name == 'brightness':
            success = self.device.vesync_dev.set_brightness(value)

            if success:
                self.set_cached_value(value)
                self.device.notify_property_changed(self)

    def update(self):
        """Update the current value, if necessary."""
        value = None
        if self.name == 'brightness':
            value = self.device.brightness
        else:
            return

        if value != self.value:
            self.set_cached_value(value)
            self.device.notify_property_changed(self)


class EtekcityOutletProperty(EtekcityProperty):
    """Etekcity outlet property type."""

    def set_value(self, value):
        """
        Set the current value of the property.

        value -- the value to set
        """
        if self.name == 'nightLightMode':
            success = False
            if value == 'auto':
                success = self.device.vesync_dev.turn_on_nightlight()
            else:
                success = self.device.vesync_dev.turn_off_nightlight()

            if success:
                self.set_cached_value(value)
                self.device.notify_property_changed(self)

    def update(self):
        """Update the current value, if necessary."""
        value = None
        if self.name == 'power':
            value = self.device.power
        elif self.name == 'voltage':
            value = self.device.voltage
        elif self.name == 'nightLightMode':
            value = self.device.night_light_mode
        else:
            return

        if value != self.value:
            self.set_cached_value(value)
            self.device.notify_property_changed(self)


class EtekcitySwitchProperty(EtekcityProperty):
    """Etekcity switch property type."""

    def set_value(self, value):
        """
        Set the current value of the property.

        value -- the value to set
        """
        if self.name == 'on':
            success = False
            if value:
                success = self.device.vesync_dev.turn_on()
            else:
                success = self.device.vesync_dev.turn_off()

            if success:
                self.set_cached_value(value)
                self.device.notify_property_changed(self)

    def update(self):
        """Update the current value, if necessary."""
        value = None
        if self.name == 'on':
            value = self.device.on
        else:
            return

        if value != self.value:
            self.set_cached_value(value)
            self.device.notify_property_changed(self)
