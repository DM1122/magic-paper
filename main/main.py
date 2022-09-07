import inky
import configparser
import libs


class MagicPaper():
    """Controller for the e-ink display."""

    def __init__():
        display = inky.auto.auto()
        config = configparser.ConfigParser()
        config.read("config.conf")
        self.config = config

        self.active_image = None

    def shuffle_image(self):
        img_paths = libs.get_image_paths()
        img_path = random.choice(files)
        
        self.active_image = Image.open(img_path)
        self.refresh_image()

    def rotate_image(img, angle):
        img.rotate(angle, resample=0, expand=0, center=None, translate=None, fillcolor=None)
        
        config.set("main", "display_rotation", angle)

        with open("config.conf", "w") as configfile:
            config.write(configfile)

        self.refresh_image()

    def reboot(self):
        """Reboot the Pi."""
        pass

    def toggle_display_mode(self):
        """Change the display mode between fit and no fit image."""
        fit_image = config.getboolean('main', 'fit_image')
        fit_image = not fit_image
        
        config.set("main", "fit_image", fit_image)

        with open("config.conf", "w") as configfile:
            config.write(configfile)
        
        self.refresh_image()


    def get_image_paths(search_dir: Path):
        p = search_dir.rglob()
        files = [x for x in p if x.is_file()]
        
        return files

    def refresh_image(self):
        inky_display.set_image(self.active_image)
        inky_display.show()

    def clean_display(self):
        """Displays solid blocks of red, black, and white to clean the Inky pHAT
        display of any ghosting."""
        colours = (inky_display.RED, inky_display.BLACK, inky_display.WHITE)
        colour_names = (inky_display.colour, "black", "white")

        # Create a new canvas to draw on

        img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))

        # Loop through the specified number of cycles and completely
        # fill the display with each colour in turn.

        for i in range(cycles):
            print("Cleaning cycle %i\n" % (i + 1))
            for j, c in enumerate(colours):
                print("- updating with %s" % colour_names[j])
                inky_display.set_border(c)
                for x in range(inky_display.WIDTH):
                    for y in range(inky_display.HEIGHT):
                        img.putpixel((x, y), c)
                inky_display.set_image(img)
                inky_display.show()
                time.sleep(1)
            print("\n")

        print("Cleaning complete!")        


def main():
    """Main program thread."""
    magic_paper = MagicPaper()

    while True:

        if timer or button_A:
            img = libs.shuffle_image()
            display.set_image(img)
            timer.restart()
            inky_display.show()

        if button_B:
            libs.rotate_image()
        
        if button_C:
            libs.toggle_display_mode()

        if button_D:
            libs.reboot()


if __name__ == "__main__":
    main()
    

    