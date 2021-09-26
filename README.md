# Flag

This is an sbot-based motorised flag that prints student IDs and moves when you scan a Southampton University ID card.

## Setup

Build a standard SRO-style robot with the following components:

- Raspberry Pi running SourceOS
- SR Power board v4
- 1x SR Motor board v4
- 1x 12V motor connected to motor board output 0
- Arduino running the firmware from the `arduino-fw` submodule in this repository
- PN532 breakout board connected to the arduino like this:
  - 5V -> VCC
  - GND -> GND
  - A4 -> SDA
  - A5 -> SCL
  - D2 -> IRQ
  - D3 -> RSTO

Make sure that the Arduino is flashed with the firmware on the `rfid` branch of the submodule.

Put `main.py` on a USB stick, insert it in the robot and start.
