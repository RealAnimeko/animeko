class Quote:
    def __init__(self, anime, character, quote, tags):
        self._anime = anime                  # Class Anime
        self._character = character          # Class Character
        self._quote = quote                  # string
        self._tags = tags                    # List of strings store as tag;tag;tag;...

    # anime
    def get_anime(self):
        return self._anime

    def set_anime(self, anime):
        self._anime = anime

    # character
    def get_character(self):
        return self._character

    def set_character(self, character):
        self._character = character

    # quote
    def get_quote(self):
        return self._quote

    def set_quote(self, quote):
        self._quote = quote

    # character
    def get_tags(self):
        return [float(x) for x in self._tags.split(';')]

    def set_tags(self, tags):
        self._tags += ';%s' % value
