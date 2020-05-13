from anime import Anime
from character import Character
from quote import Quote

import pickle

QUOTES = []

lelouch = Character("Lelouch Vi Brittana", "n4px85w6nppbsq7/code_geass_lelouch.png")
code_geass = Anime("Code Geass", "")
q1 = Quote(code_geass, lelouch, "Time flows constantly, it doesn't care about the people who are struggling.", "inspiration;psychological")
q2 = Quote(code_geass, lelouch, "If the king doesn’t move, then his subjects won’t follow.", "inspiration")
q3 = Quote(code_geass, lelouch, "Why do people lie? It isn’t only because they struggle against each other, it’s also because there is something that they’re seeking.", "inspiration;deep")

QUOTES.append(q1)
QUOTES.append(q2)
QUOTES.append(q3)

with open('db.pickle', 'wb') as db:
    pickle.dump(QUOTES, db)
