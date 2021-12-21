import sys
from collections import namedtuple


class DeterministicDice:
    def __init__(self) -> None:
        self.num = 1
        self.count = 0
    
    def roll(self) -> int:
        v = self.num
        self.count += 1
        self.num += 1
        if self.num > 100: self.num = 1
        return v


# Part 1: Finding winning player of deterministic game
with open(sys.argv[1]) as infile:
    pos = [int(line.strip()[-1]) for line in infile]

scores = [0 for _ in range(len(pos))]

turn = 0
dice = DeterministicDice()

while(all([s < 1000 for s in scores])):
    roll = sum([dice.roll() for _ in range(3)])
    pos[turn] = (pos[turn] + roll - 1) % 10 + 1
    scores[turn] += pos[turn]
    turn = -turn + 1

print(f"Part 1: Losing Score * Dice Count: {min(scores) * dice.count}")


# Part 2: Consider all possible outcomes
Universe = namedtuple("Universe", "count scores pos turn")

# Reset pos
with open(sys.argv[1]) as infile:
    pos = [int(line.strip()[-1]) for line in infile]

# "Open List"
universes = [Universe(1, [0, 0], pos, 0)]

# Dice combination frequencies, for universe counts
expansions = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
wins = [0, 0]


def expand(u: Universe):
    for value, freq in expansions.items():
        new_pos = [(p + value - 1) % 10 + 1 if i == u.turn else p for i, p in enumerate(u.pos)]
        new_score = [(s + new_pos[i]) if i == u.turn else s for i, s in enumerate(u.scores)]
        yield Universe(u.count * freq, new_score, new_pos, -u.turn+1)


while len(universes) > 0:
    cur = universes.pop()
    if max(cur.scores) >= 21:
        wins[-cur.turn+1] += cur.count
    else:
        universes.extend(expand(cur))

print(f"Part 2: Max Wins: {max(wins)}")
