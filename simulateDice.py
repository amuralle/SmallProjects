#Jan. 1 2019
#Alex Muralles
#simulateDice.py

#TODO:
#1. AC + Damage modifiers for more complicated systems
#2. Individual Character implementation (perhaps as a hash table linking characters' names to stats?)
#3. Generous/Greedy DM methods (min/max)

import random as rand
import statistics as stats
import sys

def run(trials, partySize, health):
    trialSet = []
    for i in range(trials):
        trialSet.append(simulate(partySize, health))
    return trialSet

def simulate(partySize, health):
    turns = 0
    while health > 0:
        turns = turns + 1
        for person in range((partySize)):
            roll = rand.randrange(1,21)
            if roll > 10:
                health = health - 1
                if roll == 20:
                    health = health - 1


    return turns


def test(trials, partySize, health):
    trialSet = run(trials,partySize, health)
    print(stats.median(trialSet))
    print(stats.mean(trialSet))
    print(stats.stdev(trialSet))

def init():
    arguments = sys.argv[1:]
    trials = int(arguments[0])
    partySize = int(arguments[1])
    health = int(arguments[2])
    test(trials,partySize, health)

init()
