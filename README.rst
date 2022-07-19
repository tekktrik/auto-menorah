auto-menorah
============

Self-lighting menorah!

Hardware Dependencies
=====================

Electronics
-----------
This project uses the following electronics materials:

* `Raspberry Pi Pico RP2040 <https://www.adafruit.com/product/4864>`_ (x1)
* `Adafruit Airlift - ESP32 Breakout Board <https://www.adafruit.com/product/4201>`_ (x1)
* `Adafruit 1.54" Tri-Color eInk 200x200 Display <https://www.adafruit.com/product/4868>`_ (x1)
* `Super Bright Yellow 5mm LED <https://www.adafruit.com/product/2700>`_ (x9)
* 100 Ohm Resistor (x9)

Mechanical
----------
This project uses the following physical materials:

* 3D printed frames (FDM)
* Fasteners

Software Dependencies
=====================
This project depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_ (7.1.0-beta.0 or later)
* `CircuitPython Bus Device driver <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `CircuitPython datetime module <https://github.com/adafruit/Adafruit_CircuitPython_Datetime>`_
* `CircuitPython ESP32SPI driver <https://github.com/adafruit/Adafruit_CircuitPython_ESP32SPI>`_
* `CircuitPython requests module <https://github.com/adafruit/Adafruit_CircuitPython_Requests>`_
* `CircuitPython sd module <https://github.com/adafruit/Adafruit_CircuitPython_SD>`_
* `CircuitPython SSD1681 driver <https://github.com/adafruit/Adafruit_CircuitPython_SSD1681>`_
* `CircuitPython ticks module <https://github.com/adafruit/Adafruit_CircuitPython_ticks>`_

Additionally, it relies on these CircuitPython packages:

* `asyncio <https://github.com/adafruit/Adafruit_CircuitPython_asyncio>`_

Currently, to use ``asyncio``, you'll need to download the repository as a ZIP file, and extract and move the
``asyncio`` folder into the ``lib`` folder on your board as you would any other CircuitPython module or driver.

Software Installation
=====================

Installing CircuitPython
------------------------

| You can instructions for installing the latest version of CircuitPython for the Raspberry Pi Pico here:
| `<https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython>`_

Adding CircuitPython Modules & Drivers
--------------------------------------

| Please ensure all module & driver dependencies are available on the CircuitPython filesystem. This is easily achieved by downloading the Adafruit library and driver bundle:
| `<https://circuitpython.org/libraries>`_

Adding Code to Board
--------------------

Add the following files and folders from the repository to the CIRCUITPY filesystem:

* ``code.py`` file
* ``support`` folder

Additionally, you'll want to add a file named ``secrets.py`` to the filesystem that looks like this:

.. code-block:: python

    secrets = {
        "ssid": "YourWiFiName",
        "password": "YourWiFiPassword"
    }

    location = {
        "zipcode" = "Your5DigitZipcode"
    }

You'll want to update the fields with your Wi-Fi network's name and password, and zipcode accordingly.  Don't share it with anyone!

Building Hardware
=================

HW installation instructions

Usage
=====

Menorah usage instructions
