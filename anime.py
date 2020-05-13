class Anime:
    def __init__(self, name, image):
        self._name = name           # string
        self._image = image         # string

    # name
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    # image
    def get_image(self):
        return self._image

    def set_image(self, image):
        self._image = image
