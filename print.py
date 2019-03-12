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

def print_im(f, ser):
    im = Image.open(f).rotate(-90, expand=True)

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

LEDs are "semiconductors", which
means that it's a little hard to
explain how they work because
there is so much -magic- i mean
*physics* going on. They're too
small to see what's going on if
you try to take them apart, and
tricky to DIY.

[todo: not be such a downer!
still read about them!]

Materials:

- Epoxy case / lens
- Wire leads
- Semiconductor chemistry
- Not recyclable?
""", s)

        title('Coin-cell batteries', s)
        text("""\
The battery in this kit is a
type CR2032 lithium battery. The
2032 part is actually two
numbers, 20, and 32, referring
to the diameter and thickness of
the packaging: 20mm wide, and
3.2mm thick. You can swap it out
for most other batteries that
look similar. Smaller sizes
typically don't hold as much
charge, so your throwie won't
last as long.

These batteries are rated "3V"
or 3 Volts, which is perfect for
our LEDs! Small blue, green,
pink, white, and UV LEDs
typically have a "forward
voltage" of 3.2 to 3.6 Volts,
and you don't want to give them
more than their forward voltage
rating! More on this in the next
section.

Materials:

- Lithium
- Metal casing
- Other chemical stuff...
- Recyclable as e-waste?
""", s)

        title('An odd circuit', s)
        text("""\
Usually you need to use a
resistor!

blah blah
""", s)

        print_break(s, 2)
        title('Ones and Zeros', s, 1)
        text("""\
Artist-run workshops on
computers and electronics,
taught gently, with a focus on
creativity!

Find more stuff and our next
workshop at OnesAndZeros.ca
<3
""", s)
        print_break(s, 4)

        break

    sleep(0.5)
    s.close()
