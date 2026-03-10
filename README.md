# VW, Skoda, Seat, Audi Multifunction Steering Wheel LIN-bus protocol

In this repository, I have collected the results of my LIN bus measurements regarding the communication between the multifunction steering wheel (MFSW) and the steering column electronics.

Car models on which the measurements were performed:

- Škoda Octavia Mk2 (1Z, pre-facelift) 2004-2007
- Seat Leon Mk2 (1P, pre-facelift) 2004-2008

The goal of the project is to enable the steering wheel buttons to control an aftermarket head unit using a suitable data converter.

There are vehicles, for example the Škoda Fabia Mk1, that were factory-equipped with the same steering wheel, but the MFSW option was not available for them and they did not include steering column control electronics. Therefore, the LIN bus control must be implemented using an external device.
## Skoda Octavia Steering wheel buttons
### With radio operation support only
<img style="width:20%; height:auto;" alt="Octavia radio buttons" src="/assets/images/skoda_octavia_radio_buttons.png" />

### With radio and phone operation support
<img style="width:20%; height:auto;" alt="Octavia phone buttons" src="/assets/images/skoda_octavia_phone_buttons.png" />

## Seat Leon Steering wheel buttons
### With radio operation support only
<img style="width:40%; height:auto;" alt="Octavia radio buttons" src="/assets/images/seat_leon_radio_buttons.png" />

### With radio and phone operation support
<img style="width:40%; height:auto;" alt="Octavia phone buttons" src="/assets/images/seat_leon_phone_buttons.png" />

## Measurement diagram

<img width="479" height="687" alt="Measurement wiring diagram" src="/assets/images/measurement_wiring_diagram.png" />

## Operation
The steering column control electronics (1K0953549BP) receive a constant 12V supply. After the ignition is switched on, it periodically polls the steering wheel button control module (1P0959542) via the LIN bus, which is connected through a pass-through "clock spring" cable module (1K0959653C). The horn switch and the right/left steering wheel buttons are connected to the steering wheel button control module (1P0959542).

## Button Controller's common packages

### Package #1
Direction: write data to button controller

Data: ignition state???
```
PID: 		0x01
Data: 		0x50 0x03 (0x00 0x03 (checksum: 0xFC) when ignition is turned off)
Checksum: 	0xAC
```
### Package #2
Direction: write data to button controller

Data: last message before LIN communication is stopped after ignition turned off
```
PID:		0x3C
Data:		0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00
Checksum:	0xFF
```
## 1P0959542 Seat Leon steering Wheel button controller's packages

### Package #1
Direction: response from button controller

Data: sequence number, button pressed, horn pressed
```
PID:		0x30
Data:		0x02 0x20 0x00 0x00 0x00 0x00
Checksum: 	0xDD
```
### Package #2
Direction: response from button controller

Data: type of the connected button's layout layout
```
PID:		0x21
Data:		0x21 0x22 (last byte: 0x22 - Seat Leon buttons, 0x33 - Skoda octavia mk2 buttons, 0x00 - No buttons connected, 0x03 - only right buttons connected, 0x30 - only left buttons connected)
Checksum	0xBC
```
## 3C0959542 Skoda Ocatvia mk2 steering Wheel button controller's packages

## Package #1
Direction: response from button controller

Data: sequence number, button pressed, horn pressed
```
PID:		0x30
Data:		0x02 0x20 0x00 0x00 0x00 0x2A
Checksum: 	0x56
```
## Package #2
Direction: response from button controller

Data: type of the connected button's layout layout
```
PID:		0x21
Data:		0xE5 0x22 (last byte: 0x22 - Seat Leon buttons, 0x33 - Skoda octavia mk2 buttons, 0x00 - No buttons connected, 0x03 - only right buttons connected, 0x30 - only left buttons connected)
Checksum	0xF7
```

## PID 0x30 data byte0 and byte1 sequence
```
0x00 0x80
0x01 0x10
0x02 0x20
0x03 0x30
0x04 0x4A
0x05 0x5A
0x06 0x60
0x07 0x70
0x08 0x80
0x09 0x10
0x0A 0x20
0x0B 0x30
0x0C 0x4A
0x0D 0x5A
0x0E 0x60
0x0F 0x70
```
These values are repeated.

### Message start sequence on ignition on
```
PID 0x21
10ms wait
PID 0x30 (data starts with: "0x01 0x00 ...")
10ms wait
PID 0x01
10ms wait
PID 0x30 (data starts with: "0x02 0x20 ...")
...
```

### Timing
```
PID 0x01 <-- 10ms --> PID 0x30 <-- 20ms --> PID 0x30 <-- 10ms --> PID 0x01 …

PID 0x30 <-- 20ms --> PID 0x30 (50Hz)
PID 0x01 <-- 40ms --> PID 0x01 (25Hz)
PID 0x21 <-- 200ms --> PID 0x21 (between two PID 0x30) (5Hz)
```
> [!NOTE]
> Send time slots: every 10ms.


## Buttons: Sealt Leon (Red backlight)
Button map:
```
(1)    (2)    (5)    (6)

   Left         Right

(3)    (4)    (7)    (8)
```
### Left side
```
Button #1 data: x x 0x1E 0x00 0x00 x x
Button #2 data: x x 0x2A 0x00 0x00 x x
Button #3 data: x x 0x1D 0x00 0x00 x x
Button #4 data: x x 0x01 0x00 0x00 x x
                    ^
                    buttons
```
### Right side
```
Button #5 data: x x 0x02 0x00 0x00 x x
Button #6 data: x x 0x06 0x00 0x00 x x
Button #7 data: x x 0x03 0x00 0x00 x x
Button #8 data: x x 0x07 0x00 0x00 x x
                    ^
                    buttons
```
## Buttons, Skoda Octavia mk2 (Green backlight)
Button map:
```
(1)    (2)    (5)    (6)

   Left         Right

(3)    (4)    (7)    (8)
```
### Left side
```
Button #1 data: x x 0x04 0x00 0x00 x x
Button #2 data: x x 0x2B 0x00 0x00 x x
Button #3 data: x x 0x05 0x00 0x00 x x
Button #4 data: x x 0x50 0x00 0x00 x x
                    ^
                    buttons
```
### Right side
```
Button #5 data: x x 0x02 0x00 0x00 x x
Button #6 data: x x 0x06 0x00 0x00 x x
Button #7 data: x x 0x03 0x00 0x00 x x
Button #8 data: x x 0x07 0x00 0x00 x x
                    ^
                    buttons
```
> [!NOTE]
> Multiple button press is not supported! All data bytes are zero in this case!

## Horn (Same on all modells)
```
Horn btn data: x x 0x00 0x04 0x00 x x
                         ^
                         horn
```
> [!NOTE]
> Horn + any button press is supported.
