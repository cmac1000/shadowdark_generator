Shadowdark Character Generator
---

An experimental character generator designed for use with the Shadowdark RPG.

https://www.thearcanelibrary.com/pages/shadowdark

![logo](/shadowdark.png)

# Usage

```
usage: party.py [-h] [--size [SIZE]] [--unique]

Generate characters for use with the Shadowdark RPG

optional arguments:
  -h, --help     show this help message and exit
  --size [SIZE]  number of characters to generage
  --unique       enforce character-class uniqueness
```

Called with no arguments, will generate a markdown-formatted list of six characters, generated according to the rules in the Shadowdark Player Quickstart Guide.

# Example Output

## Aran, human thief

HP: 5

```
STR: 11 +0
DEX: 19 +4
CON: 10 +0
INT: 13 +1
WIS: 10 +0
CHA: 7  -2
```

### Languages

* common
* goblin

### Talents

* backstab: on attack against unaware target, add 1+half-level damage dice
* herbalist: expert in plants, medicines, poisons
* thievery: you always have thieves' tools, no gear slots needed
* trained in climbing, sneaking, hiding, finding/disabling traps, delicate work like picking pockets and locks (advantage on relevant checks)

### Gear

* 10x iron spikes
* 13.0 gold pieces
* 2x torches
* 3x rations
* backpack
* flint and steel
* grappling hook
* leather armor
* rope, 60 feet
* shortsword

# Legal

This is an independent product published under the Shadowdark RPG Third-Party License and is not affiliated with The Arcane Library, LLC. Shadowdark RPG © The Arcane Library, LLC.

