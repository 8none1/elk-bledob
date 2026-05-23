# ELK BLEDOB

Home Assistant custom integration for ELK BLEDOB devices controlled by the `LotusLamp X` app over Bluetooth LE.

These are really cheap Bluetooth controlled LEDs available on AliExpress.  5M of LEDs for £2.36.  The app is basic, but it works.  The IR remote is basic, but it works.  The lights connect to a USB port.

Available here: https://www.aliexpress.com/item/1005005827818737.html

![image](https://github.com/8none1/elk-bledob/assets/6552931/5d98ff5b-39af-46da-84b9-4140c34f24fd)

![image](https://github.com/8none1/elk-bledob/assets/6552931/97a1cbcc-e807-45d3-b05d-55879c4905ce)

## Understanding the protocol

This time around I'm taking a different route to finding the commands to operate the lights.  Instead of pulling btsnoop files off an Android phone I am using an NRF 52840 dongle with BLE sniffer software running on it.  The reason for this is that Android is making it harder and harder to get proper btsnoop logs off devices and on to your computer.  Despite this working in the past, after a recent Android update I am now only getting `btsnooz` files which seem to truncate the data to the first 5 bytes or so.  I haven't tried to fix this or work out why, I'm going for something which is going to work without as much messing about in to the foreseeable future.  Using these NRF 52840 devices with Wireshark is well documented.

There are some Wireshark pcap files in the `bt_snoops` folder if you want to examine them.

## Similar devices

There are a number of integrations which support the ELK BLEDOM devices (note the M at the end not a B).  The protocol for these devices is similar, but slightly different.

## Bluetooth LE commands

### Initial Connection / Time Sync

At connection time the official app sends a time-of-day packet, e.g. `7e 06 83 0f 20 0c 06 00 ef`.

```
|------| ----------------------- header
|      | ||--------------------- hour   (0-23, hex)
|      | || ||------------------ minute (0-59, hex)
|      | || || ||--------------- second (0-59, hex)
|      | || || || ||------------ day-of-week (observed as 0x06 in pcaps; Mon=1..Sun=7 seems most likely)
|      | || || || || ||--------- unknown / always 0x00
|      | || || || || || |------- footer
7e 06 83 0f 20 0c 06 00 ef
```

Hat tip to [#5](https://github.com/8none1/elk-bledob/issues/5) for pointing this out. The day-of-week encoding above is inferred — the pcaps in this repo only contain a single value, so it's a best guess. This integration sends this packet on every connection so that the device clock stays roughly in sync. The clock seems to be needed for the on-device timer feature, which this integration does not expose.

### On & Off

`7e 07 04 ff 00 01 02 01 ef`     - On

`7e 07 04 00 00 00 02 01 ef`     - Off

### Colours

```
|---------|--------------------- header
|         | ||------------------ red
|         | || ||--------------- green
|         | || || ||------------ blue
|         | || || || |---|------ footer
7e 07 05 03 ff 00 00 10 ef
7e 07 05 03 00 ff 00 10 ef
7e 07 05 03 00 00 ff 10 ef
```
### Colours Brightness

```
|------| ----------------------- header
|      | ||--------------------- Brightness 0-100
|      | || |------------|------ Footer
7e 04 01 01 01 ff 02 01 ef
7e 04 01 32 01 ff 02 01 ef
7e 04 01 64 01 ff 02 01 ef
```

### Mode / Effects

```
|------| ----------------------- header
|      | ||--------------------- Mode (135-156)
|      | || |------------|------ footer
7e 07 03 93 03 ff ff 00 ef
7e 07 03 98 03 ff ff 00 ef
```

Mode are numbered `0x87` to `0x9c`.

#### Mode Speed

```
|------| ----------------------- header
|      | ||--------------------- Speed
|      | || |------------|------ footer
7e 07 02 64 ff ff ff 00 ef
```

#### Mode Brightness

This is the same as colours brightness.

## Supported devices

This has only been tested with a single generic LED strip from Ali Express.

It reports itself as `ELK-BLEDOB` over Bluetooth LE.  The app is called `LotusLamp X`.
MAC address seem to start `BE:32:xx:xx:xx:xx`.

## Supported Features in this integration

- On/Off
- RGB colour
- Brightness
- Modes/effects
- Automatic discovery of supported devices
- Device clock is synced on every connect (see "Initial Connection / Time Sync" above)

## Not supported and not planned

- Microphone interactivity
- On-device timer / scheduling
- Discovery of current light state

The on-device timer is what tells the lights to turn themselves on/off at a particular wall-clock time without anything else being involved. It is documented in [#5](https://github.com/8none1/elk-bledob/issues/5) but exposing it from Home Assistant seems pointless — HA can already do scheduling with automations, and doing it on the device would just be a second, harder-to-discover place that affects the lights.

The discovery of the light's state requires that the device be able to tell us what state it is in.  The BT controller on the device does report that it has `notify` capabilities but I have not been able to get it to report anything at all.  Perhaps you will have more luck.  Until this is solved, we have to use these lights in `optimistic` mode and assume everything just worked.  Looking at HCI logs from the Android app it doesn't even try to enable notifications and never receives a packet from the light.

## Installation

### Requirements

You need to have the bluetooth component configured and working in Home Assistant in order to use this integration.
NB: If your lights are still connected to the App then they will not be automatically discovered until you disconnect.

### HACS

Add this repo to HACS as a custom repo.  Click through:

- HACS -> Integrations -> Top right menu -> Custom Repositories
- Paste the Github URL to this repo in to the Repository box
- Choose category `Integration`
- Click Add
- Restart Home Assistant
- ELK-BLEDOB devices should start to appear in your Integrations page

## Other projects that might be of interest

- [iDotMatrix](https://github.com/8none1/idotmatrix)
- [Zengge LEDnet WF](https://github.com/8none1/zengge_lednetwf)
- [iDealLED](https://github.com/8none1/idealLED)
- [BJ_LED](https://github.com/8none1/bj_led)
- [ELK BLEDOB](https://github.com/8none1/elk-bledob)
- [HiLighting LED](https://github.com/8none1/hilighting_homeassistant)
- [BLELED LED Lamp](https://github.com/8none1/ledble-ledlamp)

