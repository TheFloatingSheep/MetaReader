import requests
from PIL import Image
from PIL.ExifTags import TAGS
import os
import curses
import time

class MetaReader:

    def __init__(self):
        self.url = ""
        self.name_image = ""

    def safe_addstr(self, stdscr, y, x, text):
        max_width = curses.COLS - 1
        if len(text) > max_width:
                text = text[:max_width - 3] + "..."
        stdscr.addstr(y, x, text)

    def download_image(self, stdscr):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                with open(self.name_image, 'wb') as f:
                    f.write(response.content)
                self.safe_addstr(stdscr, 8,0,f" ヽ(o＾▽＾o)ノ Picture downloaded successfully : {self.name_image}")
            else:
                self.addstr(stdscr, 8, 0, f"(╥_╥) Downloading failed. HTTP code : {response.status_code}")
        except Exception as e:
            self.safe_addstr(stdscr, 8, 0, f"ヽ( `д´*)ノ An error occurred while downloading : {e}")

    def get_exif(self, stdscr):
        try:
            if not os.path.exists(self.name_image):
                self.safe_addstr(stdscr, 10, 0,"(╥_╥) Picture's file does not exist.")
                return
            
            absolute_path = os.path.abspath(self.name_image)
            self.safe_addstr(stdscr, 10, 0,f"	(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ Path to the picture : {absolute_path}")
            
            image = Image.open(self.name_image)

            exif_data = image._getexif() #get exif data

            if exif_data is not None:
                ligne = 12
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)  # get tag EXIF name
                    text = f"{tag_name} : {value}"
                    self.safe_addstr(stdscr, ligne, 0, text)
                    ligne += 1 
                    if ligne >= curses.LINES - 1:
                        self.safe_addstr(stdscr, ligne, 0, "-- Press any key to continue --")
                        stdscr.refresh()
                        stdscr.getch()
                        stdscr.clear()
                        self.safe_addstr(stdscr, 10, 0, f"	(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ Path to the picture is : {absolute_path}")
                        ligne = 14
                stdscr.refresh()
            else:
                self.safe_addstr(stdscr, 14, 0, ".｡･ﾟﾟ･(＞_＜)･ﾟﾟ･｡. No EXIF data found.")
                stdscr.refresh()
        except Exception as e:
            erreur = f'	ヽ( `д´*)ノ An error occurred while extracting EXIF data : {e}'
            
            
            self.safe_addstr(stdscr, 14, 0, erreur)
            stdscr.refresh()



def interface(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    options = [
        "1. Download a picture	°˖✧◝(⁰▿⁰)◜✧˖°",
        "2. Read EXIF metadata ( ͠° ͟ʖ ͡°)",
        "3. Quit ᕕ(⌐■_■)ᕗ"
    ]
    selection = 0
    titre = "=== Welcome to MetaReader ! ✨ ==="
    reader = MetaReader()
    while True:
        stdscr.clear()
        stdscr.addstr(0, (curses.COLS - len(titre)) // 2, titre)
        for i, opt in enumerate(options):
            if i == selection:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr( i + 2, 2, opt)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(i + 2, 2, opt)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            selection = (selection - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selection = (selection + 1) % len(options)
        if key == 10:
            stdscr.clear()

            if selection == 0:
                curses.echo()
                stdscr.addstr(2, 0, "૮ ˶ᵔ ᵕ ᵔ˶ ა Please enter image's URL : ")
                reader.url = stdscr.getstr().decode()
                stdscr.addstr(3, 0, "Please enter the name of your image (ex : image.jpg) : ")
                reader.name_image = stdscr.getstr().decode()
                curses.noecho()
                reader.download_image(stdscr)

                stdscr.addstr(curses.LINES - 2, 0, "(∩ᄑ_ᄑ)⊃━☆ﾟ*･｡*･:≡( ε:) Press any ley to go back to the menu...")
                stdscr.refresh()
                stdscr.getch()

            if selection == 1:
                reader.get_exif(stdscr)
                stdscr.addstr(curses.LINES - 2, 0, "(∩ᄑ_ᄑ)⊃━☆ﾟ*･｡*･:≡( ε:) Press any ley to go back to the menu...")
                stdscr.getch()
            
            if selection == 2:
                stdscr.addstr(0, 0, "Closing...(ﾉ>ω<)ﾉ :｡･:*:･ﾟ’★,｡･:*:･ﾟ’☆")
                stdscr.refresh()
                time.sleep(1)
                curses.napms(1000)
                break



def main():
    curses.wrapper(interface)

if __name__ == "__main__":
    main()
