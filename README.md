# ELK BLEDOB

Home Assistant custom integration for ELK BLEDOB devices controlled by the `LotusLamp X` app over Bluetooth LE.

These are really cheap Bluetooth controlled LEDs available on AliExpress.  5M of LEDs for £2.36.  The app is basic, but it works.  The IR remote is basic, but it works.  The lights connect to a USB port.

Available here: https://www.aliexpress.com/item/1005005827818737.html

![image](https://github.com/8none1/elk-bledob/assets/6552931/5d98ff5b-39af-46da-84b9-4140c34f24fd)

## Understanding the protocol

This time around I'm taking a different route to finding the commands to operate the lights.  Instead of pulling btsnoop files off an Android phone I am using an NRF 52840 dongle with BLE sniffer software running on it.  The reason for this is that Android is making it harder and harder to get proper btsnoop logs off devices and on to your computer.  Despite this working in the past, after a recent Android update I am now only getting `btsnooz` files which seem to truncate the data to the first 5 bytes or so.  I haven't tried to fix this or work out why, I'm going for something which is going to work without as much messing about in to the foreseeable future.  Using these NRF 52840 devices with Wireshark is well documented.

There are some Wireshark pcap files in the `bt_snoops` folder if you want to examine them.

## Similar devices

There are a number of integrations which support the ELK BLEDOM devices (note the M at the end not a B).  The protocol for these devices is similar, but slightly different.

## Bluetooth LE commands

### Initial Connection

The bytes `7e 06 83 0f 20 0c 06 00 ef` are sent at connection time.  It is unknown what this does at the moment.

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

## Not supported and not planned

- Microphone interactivity
- Timer / Clock functions
- Discovery of current light state

The timer/clock functions are understandable from the HCI Bluetooth logs but adding that functionality seems pointless and I don't think Home Assistant would support it any way.

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
