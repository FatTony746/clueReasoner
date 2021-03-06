'''
Tony Tran and Miles Douglas





ClueReasoner.py - project skeleton for a propositional reasoner
for the game of Clue.  Unimplemented portions have the comment "TO
BE IMPLEMENTED AS AN EXERCISE".  The reasoner does not include
knowledge of how many cards each player holds.
Originally by Todd Neller
Ported to Python by Dave Musicant

Copyright (C) 2008 Dave Musicant

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Information about the GNU General Public License is available online at:
  http://www.gnu.org/licenses/
To receive a copy of the GNU General Public License, write to the Free
Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
02111-1307, USA.'''

import SATSolver

# Initialize important variables
caseFile = "cf"
players = ["sc", "mu", "wh", "gr", "pe", "pl"]
extendedPlayers = players + [caseFile]
suspects = ["mu", "pl", "gr", "pe", "sc", "wh"]
weapons = ["kn", "ca", "re", "ro", "pi", "wr"]
rooms = ["ha", "lo", "di", "ki", "ba", "co", "bi", "li", "st"]
cards = suspects + weapons + rooms

def getPairNumFromNames(player,card):
    return getPairNumFromPositions(extendedPlayers.index(player),
                                   cards.index(card))

def getPairNumFromPositions(player,card):
    return player*len(cards) + card + 1

# TO BE IMPLEMENTED AS AN EXERCISE
def initialClauses():
    clauses = []

    # Each card is in at least one place (including case file).
    for c in cards:
        clauses.append([getPairNumFromNames(p,c) for p in extendedPlayers])

    # A card cannot be in two places.
    # For every card, created a set of clauses: 
    # [c_ip_1, ~c_ip_2, ~c_ip_3]
    # [~c_ip_1, c_ip_2, ~c_ip_3]
    # [~c_ip_1, ~c_ip_2, c_ip_3]
    for c in cards:
        for p in extendedPlayers:
            num = getPairNumFromNames(p, c)
            p = getPairNumFromNames(p, c)
            clauses.append([-num, -p])
    
        # for p in extendedPlayers:
        #     moreClauses = []
        #     clauses.append([getPairNumFromNames(p,c),-getPairNumFromNames(p,c)])
        #     for others in extendedPlayers:
        #         if p == others:
        #             pass
        #         else:
        #             clauses.append([-getPairNumFromNames(others,c),-getPairNumFromNames(p,c)])
        #             moreClauses.append(getPairNumFromNames(others,c))
        #     moreClauses.append(getPairNumFromNames(p,c))
        #     clauses.append(moreClauses)

    # At least one card of each category is in the case file.
    clauses.append([getPairNumFromNames("cf",s) for s in suspects])
    clauses.append([getPairNumFromNames("cf",w) for w in suspects])
    clauses.append([getPairNumFromNames("cf",r) for r in suspects])

    # No two cards in each category can both be in the case file.
    f = extendedPlayers[len(extendedPlayers)-1]
    for c in range(len(cards)):
        num = getPairNumFromNames(f, cards[c])

        #Add suspect clauses
        if c<6:
            for i in range(6):
                if i != c:
                    p = getPairNumFromNames(f, cards[i])
                    clauses.append([-num, -p])
        #Add weapon clauses 
        elif c<12:
            for i in range(6,12):
                if i!=c:
                    p = getPairNumFromNames(f, cards[i])
                    clauses.append([-num, -p])
        #Add room clauses
        elif c<21:
            for i in range(12,21):
                if i!=c:
                    p = getPairNumFromNames(f, cards[i])
                    clauses.append([-num, -p])

    # # No two cards in each category can both be in the case file.
    # for s in suspects:
    #     moreClauses = []
    #     clauses.append([getPairNumFromNames("cf",s),-getPairNumFromNames("cf",s)])
    #     for otherS in suspects:
    #         if s == otherS:
    #             pass
    #         else:
    #             clauses.append([-getPairNumFromNames("cf",otherS),-getPairNumFromNames("cf",s)])
    #             moreClauses.append(getPairNumFromNames("cf",otherS))
    #     moreClauses.append(getPairNumFromNames("cf",s))
    #     clauses.append(moreClauses)

    # for w in weapons:
    #     moreClauses = []
    #     clauses.append([getPairNumFromNames("cf",w),-getPairNumFromNames("cf",w)])
    #     for otherW in weapons:
    #         if w == otherW:
    #             pass
    #         else:
    #             clauses.append([-getPairNumFromNames("cf",otherW),-getPairNumFromNames("cf",w)])
    #             moreClauses.append(getPairNumFromNames("cf",otherW))
    #     moreClauses.append(getPairNumFromNames("cf",w))
    #     clauses.append(moreClauses)

    # for r in rooms:
    #     moreClauses = []
    #     clauses.append([getPairNumFromNames("cf",r),-getPairNumFromNames("cf",r)])
    #     for otherR in rooms:
    #         if r == otherR:
    #             pass
    #         else:
    #             clauses.append([-getPairNumFromNames("cf",otherR),-getPairNumFromNames("cf",r)])
    #             moreClauses.append(getPairNumFromNames("cf",otherR))
    #     moreClauses.append(getPairNumFromNames("cf",r))
    #     clauses.append(moreClauses)

    return clauses

# TO BE IMPLEMENTED AS AN EXERCISE
def hand(player,cards):
    return [[getPairNumFromNames(player,c)] for c in cards]

# TO BE IMPLEMENTED AS AN EXERCISE
def suggest(suggester,card1,card2,card3,refuter,cardShown):
    toAddClauses = []
    if refuter == None:
        for p in players:
            if p == suggester:
                pass
            else:
                toAddClauses.append([-getPairNumFromNames(p,card1)])
                toAddClauses.append([-getPairNumFromNames(p,card2)])
                toAddClauses.append([-getPairNumFromNames(p,card3)])
        return toAddClauses        

    index = players.index(suggester)
    while(index != players.index(refuter)):
        index += 1
        index = index%len(players)
        toAddClauses.append([-getPairNumFromNames(players[index],card1)])
        toAddClauses.append([-getPairNumFromNames(players[index],card2)])
        toAddClauses.append([-getPairNumFromNames(players[index],card3)])
        
    if cardShown == None:
        toAddClauses.append([getPairNumFromNames(refuter,card1), 
                             getPairNumFromNames(refuter,card2), 
                             getPairNumFromNames(refuter,card3)])
        
    else:
        toAddClauses.append([getPairNumFromNames(refuter,cardShown)])
        
    return toAddClauses

# TO BE IMPLEMENTED AS AN EXERCISE
def accuse(accuser,card1,card2,card3,isCorrect):
    toAddClauses = []
    
    if isCorrect:
        toAddClauses.append([getPairNumFromNames("cf",card1)])
        toAddClauses.append([getPairNumFromNames("cf",card2)])
        toAddClauses.append([getPairNumFromNames("cf",card3)])

    else:
        toAddClauses.append([-getPairNumFromNames("cf", card1),
                             -getPairNumFromNames("cf", card2),
                             -getPairNumFromNames("cf", card3)])

    toAddClauses.append([-getPairNumFromNames(accuser,card1)])
    toAddClauses.append([-getPairNumFromNames(accuser,card2)])
    toAddClauses.append([-getPairNumFromNames(accuser,card3)])

    return toAddClauses

def query(player,card,clauses):
    return SATSolver.testLiteral(getPairNumFromNames(player,card),clauses)

def queryString(returnCode):
    if returnCode == True:
        return 'Y'
    elif returnCode == False:
        return 'N'
    else:
        return '-'

def printNotepad(clauses):
    for player in players:
        print '\t', player,
    print '\t', caseFile
    for card in cards:
        print card,'\t',
        for player in players:
            print queryString(query(player,card,clauses)),'\t',
        print queryString(query(caseFile,card,clauses))

def playClue():
    clauses = initialClauses()
    clauses.extend(hand("sc",["wh", "li", "st"]))
    clauses.extend(suggest("sc", "sc", "ro", "lo", "mu", "sc"))
    clauses.extend(suggest("mu", "pe", "pi", "di", "pe", None))
    clauses.extend(suggest("wh", "mu", "re", "ba", "pe", None))
    clauses.extend(suggest("gr", "wh", "kn", "ba", "pl", None))
    clauses.extend(suggest("pe", "gr", "ca", "di", "wh", None))
    clauses.extend(suggest("pl", "wh", "wr", "st", "sc", "wh"))
    clauses.extend(suggest("sc", "pl", "ro", "co", "mu", "pl"))
    clauses.extend(suggest("mu", "pe", "ro", "ba", "wh", None))
    clauses.extend(suggest("wh", "mu", "ca", "st", "gr", None))
    clauses.extend(suggest("gr", "pe", "kn", "di", "pe", None))
    clauses.extend(suggest("pe", "mu", "pi", "di", "pl", None))
    clauses.extend(suggest("pl", "gr", "kn", "co", "wh", None))
    clauses.extend(suggest("sc", "pe", "kn", "lo", "mu", "lo"))
    clauses.extend(suggest("mu", "pe", "kn", "di", "wh", None))
    clauses.extend(suggest("wh", "pe", "wr", "ha", "gr", None))
    clauses.extend(suggest("gr", "wh", "pi", "co", "pl", None))
    clauses.extend(suggest("pe", "sc", "pi", "ha", "mu", None))
    clauses.extend(suggest("pl", "pe", "pi", "ba", None, None))
    clauses.extend(suggest("sc", "wh", "pi", "ha", "pe", "ha"))
    clauses.extend(suggest("wh", "pe", "pi", "ha", "pe", None))
    clauses.extend(suggest("pe", "pe", "pi", "ha", None, None))
    clauses.extend(suggest("sc", "gr", "pi", "st", "wh", "gr"))
    clauses.extend(suggest("mu", "pe", "pi", "ba", "pl", None))
    clauses.extend(suggest("wh", "pe", "pi", "st", "sc", "st"))
    clauses.extend(suggest("gr", "wh", "pi", "st", "sc", "wh"))
    clauses.extend(suggest("pe", "wh", "pi", "st", "sc", "wh"))
    clauses.extend(suggest("pl", "pe", "pi", "ki", "gr", None))
    print 'Before accusation: should show a single solution.'
    printNotepad(clauses)
    print
    clauses.extend(accuse("sc", "pe", "pi", "bi", True))
    print 'After accusation: if consistent, output should remain unchanged.'
    printNotepad(clauses)

if __name__ == '__main__':
    playClue()
