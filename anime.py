from character import Character

class Anime:
    def __init__(self, name, image="", characters=[], views=0):
        self._name = name                   # str
        self._image = image                 # str
        self._characters = characters       # [character]
        self._views = views                 # int

    # name
    def get_name(self):
        return self._name

    # image
    def get_image(self):
        return self._image

    # characters
    def get_characters(self):
        return self._characters

    def set_characters(self, character):
        self._characters.append(character)

    # view
    def get_views(self):
        return self._views
