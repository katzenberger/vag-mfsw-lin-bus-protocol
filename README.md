# VW, Skoda, Seat, Audi Multifunction Steering Wheel LIN-bus protocol

In this repository, I have collected the results of my LIN bus measurements regarding the communication between the multifunction steering wheel (MFSW) and the steering column electronics.

Car models on which the measurements were performed:

- Škoda Octavia Mk2 (1Z, pre-facelift) 2004-2007
- Seat Leon Mk2 (1P, pre-facelift) 2004-2008

## Measurement diagram

<img width="479" height="687" alt="Measurement wiring diagram" src="/measurement_wiring_diagram.png" />

## Operation
The steering column control electronics (1K0953549BP) receive a constant 12V supply. After the ignition is switched on, it periodically polls the steering wheel button control module (1P0959542) via the LIN bus, which is connected through a pass-through "clock spring" cable module (1K0959653C). The horn switch and the right/left steering wheel buttons are connected to the steering wheel button control module (1P0959542).
