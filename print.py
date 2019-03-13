#!/usr/bin/env python
from serial import Serial
from PIL import Image
from time import sleep

EMPH = 0b00001000
TALL = 0b00010000
WIDE = 0b00100000

ROW = (
    0x12,  # [DC2]
    '*',
    1, # height
    48,  # width
)

def print_im(f, ser, rotate=True):
    im = Image.open(f)
    if rotate:
        im = im.rotate(-90, expand=True)

    dots = 20
    heatTime = 150
    heatInterval = 110
    ser.write([
        27,
        55,
        dots,
        heatTime,
        heatInterval,
    ])

    printDensity = 0b001
    printBreakTime = 0b00001
    ser.write([
        18,
        35,
        (printDensity << 5) | printBreakTime,
    ])

    for y in range(im.size[1]):
        out = list(ROW)
        for xi in range(0, im.size[0], 8):
            b = 0
            for i in range(8):
                b <<= 1
                px = im.getpixel((xi + i, y))
                black = px == 1
                b |= black
            out.append(b)
        ser.write(out)
        sleep(0.05)


def print_break(ser, n=2):
    ser.write('\n' * n);

def text(t, s):
    s.write(t)
    sleep(0.005 * len(t))

def title(t, s, n=2):
    print_break(s, 1)
    if n == 1:
        s.write([27, '!', EMPH | TALL | WIDE])
    elif n == 2:
        s.write([27, 'a', 1])  # center
        s.write([27, '!', EMPH])  # bold
        s.write([29, 'B', 1])  # invert
    else:
        s.write([27, 'a', 1])  # center
 
    s.write(' {} \n'.format(t))

    s.write([27, '!', 0])  # unformat    
    s.write([29, 'B', 0])  # uninvert
    s.write([27, 'a', 0])  # left

    print_break(s, 1)

def page(f, s):
    print_im(f, s)
    print_break(s, 6)
    sleep(0.6)

if __name__ == '__main__':
    import sys
    s = Serial(sys.argv[1], 19200)
    sleep(0.3)
    while True:
        title('a OnesAndZeros.ca kitzine\nby @uniphil', s, 3)
        print_break(s, 3)
        page('cover.png', s)
        page('0-contents.png', s)
        page('1-led.png', s)
        page('2-battery.png', s)
        page('3-circuit.png', s)
        page('4-tape.png', s)
        page('5-magnet.png', s)
        page('6-more-tape.png', s)
        page('7-throw.png', s)
        title('Appendix', s, 1)

        title('Throwie kitzine v0.1', s, 3)

        title('Light Emitting Diodes', s)
        text("""\
LEDs have become cheap and
universal in electronic devices.
Any little glowing indicator
light made since the 1980s is
likely to be an LED. Backlights
on all kinds of device screens
are LEDs! With big efficiency
gains in modern LED tech, many
new household light bulbs are
even LEDs.

Diodes conduct electricity only
in one direction - they almost
completely block it if they are
connected backwards (this is why
they are called semiconductors).
That's why nothing happens if
you connect an LED the wrong way
around.

When current flows (forwards)
through an LED, it lights up!
The frequency of the light,
which we perceive as colour, is
determined by the chemistry
of the semiconductor materials.

White LEDs are usually really
blue LEDs with phosphors added
that absorb and re-emit some of
the blue light as yellow light!

Materials:

- Epoxy case / lens.
- Wire leads.
- Tiny amounts of Silicon,
  Gallium, Arsenic, Nitrogen, or
  other chemicals depending on
  the colour.
- Recyclable: not sure, but
  probably not :(
""", s)

        title('Coin-cell batteries', s)
        text("""\
The battery in this kit is a
type CR2032 lithium battery. The
2032 part is actually two
numbers, 20 and 32, which refer
to the diameter and thickness of
the battery: 20mm wide, 3.2mm
thick. You can swap it out for
most other CRXXXX batteries!
Smaller sizes typically don't
store as much energy, so your
throwie won't last as long.

These batteries are rated "3V"
or 3 Volts, which is perfect for
our LEDs! Small blue, green,
pink, white, and UV LEDs
typically have a "forward
voltage" of around 3 Volts,
which is what they need to start
conducting electricity and
lighting up.

Materials:

- Aluminum, and likely copper as
  well as cobalt or nickel.
- An electrolyte containing
  Lithium.
- May be partially recycled if
  returned as e-waste. As of
  2017, extracting Lithium from
  batteries cost 5x more than
  mining it.
""", s)

        title('An odd circuit', s)
        text("""\
We only used two components in
our throwie, but almost every
other circuit you make with an
LED will have at least one more:
a resistor!
""", s)
        print_im('resistor.png', s, False)
        text("""\

Resistors limit the amount of
current that can flow into an
LED, making it safe for them to
work with higher voltages.

A common resistor size used with
LEDs is 330 Ohms.Most LEDs can
be used with up to 9 Volts if a
330 Ohm resistor is connected in
series with the LED like this:

""", s)
        print_im('resistor-circuit.png', s, False)

        print_break(s, 3)
        title('Ones and Zeros', s, 1)
        title("""\
Artist-run workshops on
computers and electronics,
taught gently, with a focus on
creativity!

Find more stuff and our next
events at OnesAndZeros.ca
<3
""", s, 3)
        print_break(s, 4)

        break

    sleep(0.5)
    s.close()
