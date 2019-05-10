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

def print_im(f, ser, rotate=True, black=1):
    im = Image.open(f)
    if rotate:
        im = im.rotate(-90, expand=True)

    dots = 20
    heatTime = 127
    heatInterval = 100
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
                blk = px == black
                b |= blk
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
    print_break(s, 4)
    sleep(0.6)

if __name__ == '__main__':
    import sys
    s = Serial(sys.argv[1], 19200)
    sleep(0.3)
    while True:
        title('throwie kit/zine v0.2\nby @uniphil', s, 3)
        print_break(s, 3)
        page('cover.png', s)
        text("""\
"LED Throwies are an inexpensive
way to add color to any ferro-
magnetic surface in your neigh-
bourhood. A Throwie consists of
a lithium battery, an LED, and a
strong magnet taped together.
Throw it up high and in quantity
to impress your friends and city
officials.
        -- Graffiti Research Lab
""", s)
        print_im('throwies-smol.png', s, False, black=0)
        text("""\
   "Make Throwies Not Bombs"
""", s)

        print_break(s, 3)
        page('0-contents.png', s)
        page('1-led.png', s)
        page('2-battery.png', s)
        page('3-circuit.png', s)
        page('4-tape.png', s)
        page('5-magnet.png', s)
        page('6-more-tape.png', s)
        page('7-throw.png', s)
        title('Appendix', s, 1)

        title('Light Emitting Diodes', s)
        text("""\
Any little glowing indicator
light made since the 1980s is
probably an LED!

Diodes only conduct electricity
in one direction - they block it
if they are connected backwards
(this is why they are called
semiconductors). When electrical
current flows forwards through
an LED, it lights up!

The chemistry of the semicon-
ductor material determines the
colour. White LEDs cheat: they
are really a blue LED with phos-
phors that absorb and re-emit
some of the blue light as yellow
to make white!

Materials:

- Case / lens: plastic
- Semiconductor: Silicon,
  Gallium, Arsenic, Nitrogen, or
  other chemicals (depending on
  the colour).
- Recycling: reusable! The LED
  can be reused many many times!
""", s)

        title('Coin-cell batteries', s)
        text("""\
Our battery is a CR2032 lithium
button cell. "2032" is two
numbers--20 and 32--which refer
to the size of the battery:
    -> 20mm wide
    -> 3.2mm thick.
Other button cell batteries will
also work for throwies, but
smaller ones don't last as long.

CR2032 batteries are rated "3V"
(3 Volts), which is perfect for
our LEDs: typical blue, green,
pink, white and UV LEDs usually
have a "forward voltage", the
amount needed to light up, of
around 3V.

Materials:

- Casing and electrods: aluminum
  and copper, as well as cobalt
  or nickel.
- An electrolyte with lithium.
- May be partially recycled if
  returned as e-waste.
  Extracting lithium from
  batteries currently costs more
  than mining new lithium.

CR2032 batteries do not contain
acid or or heavy metals, but
they should still be disposed of
properly.
""", s)

        title('Neodymium magnet', s)
        text("""\
Also known as rare earth magnets
because neodymium is a so-called
Rare Earth Element (REE). REEs
are a set of 15 elements called
the lanthanide series.

China accounts for almost 90% of
global REE production, estimated
at 135,000 tonnes.

Materials:

- Magnet: NdFeB (neodymium, iron
  and boron)
- Plating: Nickel
- Recycling: Reusable!
""", s)

        title('An odd circuit', s)
        text("""\
Throwies only use two electronic
parts, but almost every other
circuit with an LED will have
one more: a resistor!
""", s)
        print_im('resistor.png', s, False)
        text("""\

Resistors limit the amount of
electrical current that can flow
in a circuit, making it safe for
LEDs to be used with higher
voltages.

A common resistor size used with
LEDs is 330 Ohms. LEDs like ours
can be used with up to 9 Volts
if a 330 Ohm resistor is connec-
ted in series with the LED like
this:

""", s)
        print_im('resistor-circuit.png', s, False)

        print_break(s, 3)
        title('Ones and Zeros', s, 1)
        title("""\
Artist-run workshops on
compu ters and electronics,
taught gently, with a focus on
creativity!

Find more stuff and our next
events at OnesAndZeros.ca
@onesandzerosca
""", s, 3)
        print_break(s, 2)

        break
        sleep(3)

    sleep(0.5)
    s.close()
