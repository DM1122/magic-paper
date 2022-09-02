import inky


if __name__ == "__main__":
    display = inky.auto.auto()

    print(display.colour)
    print(display.resolution)
    display.set_image(image)
    display.set_border(inky.RED)

    inky_display.show()