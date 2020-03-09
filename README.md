# etekcity-adapter

Etekcity smart device adapter for Mozilla WebThings Gateway.

# Supported Devices

## Tested and Working

* Smart plugs
    * Etekcity Voltson Smart WiFi Outlet (15A model ESW15-USA)
    * Etekcity Voltson Smart WiFi Outlet (10A model ESW03-USA)

## Untested but _Should Work_

* Smart bulbs
    * Etekcity Soft White Dimmable Smart Bulb (ESL100)
    * Etekcity Cool to Soft White Tunable Dimmable Bulb (ESL100CW)
* Smart plugs
    * Etekcity Voltson Smart WiFi Outlet (7A model ESW01-USA)
    * Etekcity Voltson Smart WiFi Outlet (10A model ESW01-EU)
    * Etekcity Two Plug Outdoor Outlet (ESO15-TB)
* Smart switches
    * Etekcity Smart WiFi Light Switch (model ESWL01)
    * Etekcity Wifi Dimmer Switch (ESD16)

# Requirements

If you're running this add-on outside of the official gateway image for the Raspberry Pi, i.e. you're running on a development machine, you'll need to do the following (adapt as necessary for non-Ubuntu/Debian):

```
sudo apt install python3-dev libnanomsg-dev
sudo pip3 install nnpy
sudo pip3 install git+https://github.com/mozilla-iot/gateway-addon-python.git
```
