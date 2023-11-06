# Modified from the WS2812 LED example
import array, time
from machine import Pin
import rp2

# Configure the number of LEDs.
NUM_LEDS = 160
PIN_NUM = 6

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()
        
class NeoPixel(object):
    def __init__(self,pin=PIN_NUM,num=NUM_LEDS,brightness=0.8):
        self.pin=pin
        self.num=num
        self.brightness = brightness
        
        # Create the StateMachine with the ws2812 program, outputting on pin
        self.sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))

        # Start the StateMachine, it will wait for data on its FIFO.
        self.sm.active(1)

        # Display a pattern on the LEDs via an array of LED RGB values.
        self.ar = array.array("I", [0 for _ in range(self.num)])
        
        self.BLACK = (0, 0, 0)
        self.RED = (0, 15, 0)
        self.YELLOW = (15, 15, 0)
        self.GREEN = (15, 0, 0)
        self.CYAN = (0, 15, 15)
        self.BLUE = (0, 0, 15)
        self.PURPLE = (15, 0, 15)
        self.WHITE = (15, 15, 15)
        self.COLORS = [self.RED, self.YELLOW, self.GREEN, self.CYAN, self.BLUE, self.PURPLE, self.WHITE,self.BLACK ]
        
    ##########################################################################
    def pixels_show(self):
        dimmer_ar = array.array("I", [0 for _ in range(self.num)])
        for i,c in enumerate(self.ar):
            r = int(((c >> 8) & 0xFF) * self.brightness)
            g = int(((c >> 16) & 0xFF) * self.brightness)
            b = int((c & 0xFF) * self.brightness)
            dimmer_ar[i] = (g<<16) + (r<<8) + b
        self.sm.put(dimmer_ar, 8)

    def pixels_set(self, i, color):
        self.ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

    def pixels_fill(self, color):
        for i in range(len(self.ar)):
            self.pixels_set(i, color)

def strToBin(inString):
    array = []
    out = []
    for i in inString:
        val = bin(ord(i))[2:]
        array.append(val)
    
    for i in list(''.join(array)):
        out.append(int(i))
            
    return out

if __name__=='__main__':
    grid = NeoPixel()
    count = 0
    colArray = []
    binArray = []
    length = 12   # this must be the length of the longest array
    data = (
        ['Torbjørnskjær','Hvaler'],
        ['Homlungen','Hvaler'],
        ['Strømtangen','Fredrikstad'],
        ['Struten','Fredrikstad'],
        ['Guldholmen','Moss'],
        ['Digerudgrunnen','Frogn'],
        ['Steilene','Nesodden'],
        ['Heggholmen','Oslo'],
        ['Dyna','Oslo'],
        ['Kavringen','Oslo'],
        ['Filtvet','Hurum'],
        ['Bastøy','Horten'],
        ['Medfjordbåen','Tønsberg'],
        ['Torgersøy','Tønsberg'],
        ['Fulehuk','Nøtterøy'],
        ['StoreFærder','Tjøme'],
        ['LilleFærder','Tjøme'],
        ['Svenner','Larvik'],
        ['Stavernsodden','Larvik'],
        ['Tvistein','Larvik'],
        ['Langøytangen','Bamble'],
        ['Jomfruland','Kragerø'],
        ['Strømtangen','Kragerø'],
        ['Stavseng','Kragerø'],
        ['Stangholmen','Risør'],
        ['Lyngør','Tvedestrand'],
        ['YtreMøkkalasset','Arendal'],
        ['StoreTorungen','Arendal'],
        ['LilleTorungen','Arendal'],
        ['Sandvigodden','Arendal'],
        ['Rivingen','Grimstad'],
        ['Homborsund','Grimstad'],
        ['Saltholmen','Lillesand'],
        ['Grønningen','Kristiansand'],
        ['Oksøy','Kristiansand'],
        ['Odderøya','Kristiansand'],
        ['Songvår','Søgne'],
        ['Ryvingen','Mandal'],
        ['Hatholmen','Mandal'],
        ['Lindesnes','Lindesnes'],
        ['Markøy','Lyngdal'],
        ['SøndreKatland','Farsund'],
        ['Lista','Farsund'],
        ['LillePresteskjær','Sokndal'],
        ['Vibberodden','Eigersund'],
        ['Eigerøy','Eigersund'],
        ['Kvassheim','Hå'],
        ['Obrestad','Hå'],
        ['Feistein','Klepp'],
        ['Flatholmen','Sola'],
        ['Tungenes','Randaberg'],
        ['Kvitsøy','Kvitsøy'],
        ['Fjøløy','Rennesøy'],
        ['Vikeholmen','Karmøy'],
        ['Høgevarde','Karmøy'],
        ['Sørhaugøy','Haugesund'],
        ['Skudenes','Karmøy'],
        ['Geitungen','Karmøy'],
        ['Utsira','Utsira'],
        ['Røværsholmen','Haugesund'],
        ['Ryvarden','Sveio'],
        ['Leirvik','Stord'],
        ['Slåtterøy','Bømlo'],
        ['Øksehamaren','Austevoll'],
        ['Marstein','Austevoll'],
        ['Hellisøy','Fedje'],
        ['Holmengrå','Fedje'],
        ['Utvær','Solund'],
        ['Geita','Askvoll'],
        ['Ytterøyane','Flora'],
        ['Stabben','Flora'],
        ['Kvanhovden','Flora'],
        ['Hendanes','Vågsøy'],
        ['Ulvesund','Vågsøy'],
        ['Skongenes','Vågsøy'],
        ['Kråkenes','Vågsøy'],
        ['Svinøy','Sande'],
        ['Haugsholmen','Sande'],
        ['Flåvær','Herøy'],
        ['Runde','Herøy'],
        ['Grasøyane','Ulstein'],
        ['Hogsteinen','Giske'],
        ['Alnes','Giske'],
        ['Erkna','Giske'],
        ['Storholmen','Giske'],
        ['Lepsøyrev','Haram'],
        ['Hellevik','Haram'],
        ['Ulla','Haram'],
        ['Ona','Sandøy'],
        ['Flatflesa','Sandøy'],
        ['Bjørnsund','Fræna'],
        ['Kvitholmen','Eide'],
        ['Hestskjær','Averøy'],
        ['Stavnes','Averøy'],
        ['Grip','Kristiansund'],
        ['Tyrhaug','Smøla'],
        ['Skalmen','Smøla'],
        ['Haugjegla','Smøla'],
        ['Sletringen','Frøya'],
        ['Sula','Frøya'],
        ['Vingleia','Frøya'],
        ['Finnvær','Frøya'],
        ['Halten','Frøya'],
        ['Terningen','Hitra'],
        ['Børøyholmen','Hitra'],
        ['Agdenes','Agdenes'],
        ['Asenvågøy','Bjugn'],
        ['Kjeungskjær','Ørland'],
        ['Kaura','Roan'],
        ['Buholmråsa','Osen'],
        ['Kya','Osen'],
        ['Villa','Flatanger'],
        ['Ellingråsa','Flatanger'],
        ['Gjeslingene','Vikna'],
        ['Grinna','Vikna'],
        ['Nordøyan','Vikna'],
        ['Prestøy','Nærøy'],
        ['Nærøysund','Vikna'],
        ['Sklinna','Leka'],
        ['Bremstein','Vega'],
        ['Ytterholmen','Herøy'],
        ['Åsvær','Dønna'],
        ['Træna','Træna'],
        ['Myken','Rødøy'],
        ['Kalsholmen','Meløy'],
        ['Tennholmen','Gildeskål'],
        ['Bodø','Bodø'],
        ['Landegode','Bodø'],
        ['Bjørnøy','Bodø'],
        ['Måløy–Skarholmen','Steigen'],
        ['Flatøy','Steigen'],
        ['Tranøy','Hamarøy'],
        ['Barøy','Ballangen'],
        ['Skrova','Vågan'],
        ['Moholmen','Vågan'],
        ['Rotvær','Lødingen'],
        ['Skomvær','Røst'],
        ['Glåpen','Moskenes'],
        ['Litløy','Bø'],
        ['Anda','Øksnes'],
        ['Andenes','Andøy'],
        ['Hekkingen','Lenvik'],
        ['Torsvåg','Karlsøy'],
        ['Fugløykalven','Karlsøy'],
        ['Fuglenes','Hammerfest'],
        ['Fruholmen','Måsøy'],
        ['Helnes','Nordkapp'],
        ['Slettnes','Gamvik'],
        ['Kjølnes','Berlevåg'],
        ['Makkaur','Båtsfjord'],
        ['Vardø','Vardø'],
        ['Bøkfjord','Sør-Varanger'],
        ['Lyngdal','Markøy'], # *
        ['Haram','Hellevik'], # * 
        )

    # fill the grid with some, ya know, totally random colors
    for y in range(10):
        for x in range(16):
            modX = x % 16
            modY = y % 10
            
            colArray.insert(16 * y + x, (0,15,0))
            if modX == 5 or modY == 4 or modY == 5:
                colArray.insert(16 * y + x, (0,0,15))
            elif modX == 4 or x % 16 == 6:
                if modY != 4 or modY != 4:
                    colArray.insert(16 * y + x, (15,15,15))
            elif modY == 3 or modY == 6:
                if modX < 5 or modX > 6:
                    colArray.insert(16 * y + x, (15,15,15))

    # make the array of names and places into binArray (binary, hehe)
    for string in data:
        binArray.append(strToBin(''.join( string)))
    
    # these are to make the gap at the bottom
    binArray.insert(47,[0])
    binArray.insert(63,[0])
    binArray.insert(79,[0])
    binArray.insert(95,[0])
    binArray.insert(111,[0])
    binArray.insert(127,[0])
        
    while(1):
        for i in range(len(binArray)):
            string = binArray[i]
            grid.pixels_set(i, colArray[i])
                
            if string[count % len(string)] == 0:                
                grid.pixels_set(i, grid.BLACK)

        grid.pixels_show()
        count += 1
        sleep = 2 #Hz
        time.sleep(1/sleep)