class Quote:
    def __init__(self, anime, character, quote, tags):
        self._anime = anime                  # Class Anime
        self._character = character          # Class Character
        self._quote = quote                  # string
        self._tag = tags                    # List of strings store as tag;tag;tag;...

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
    def get_tag(self):
        return self._tag

    def get_tag_list(self):
        return [x for x in self._tag.split(';')]

    def set_tag(self, tag):
        self._tag += ';%s' % value
