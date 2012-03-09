# -*- coding:Utf-8 -*-
VERSION = '0.3'
## ----- alienNameGenerator.py -----
##
##      Alien name transformator
##
##  Transforms your name into an alien name. Use with caution!
## 
## Copyright (C) 2012, Fülöp, András, fulibacsi@gmail.com
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##


from random import choice
import data.pyplanets
import collections as col


class Alienize():
    """ Create and stores the user's alien name. """
    
    
    def __init__(self, name = None):
        """ Init the name. """
        self.name = name
        self.planet = None
        
    
    def getName(self):
        """ Set the alien name, and a matching planet, then returns it to the user. """
        # create the name
        self.alienize()
        # create the planet
        self.getPlanet()
        
        # return the result
        return self.name + ' from the planet ' + self.planet
    

# ---------------------------------- Name -----------------------------------

    
    # STEP 1
    # transform umlaut characters to their non-umlaut version
    def umlautTransform(self, string):
        """ Turn every character with umlaut to it's non-umlaut version. """
        
        UmlautNonUmlautDict = {u'á':'a', u'é':'e', u'í':'i', u'ó':'o', u'ö':'o', u'ő':'o', u'ú':'u', u'ü':'u', u'ű':'u'}
        nonUmlaut = ''
        
        # for every character,
        for s in string:
            # if umlaut character, switch it
            if s in UmlautNonUmlautDict:
                nonUmlaut += UmlautNonUmlautDict[s]
            # don't change in other cases
            else:
                nonUmlaut += s

        # return the result.
        return nonUmlaut

        
        
    # STEP 2    
    # remove a random character from the name
    def removeRandomChar(self, string):
        """ Remove a randomly selected char from the string. """

        modifiedString = string

        # remove characters in proportion to the length of the string
        for i in range(len(modifiedString) / 5):
            # select the char,
            delChar = choice(range(0, len(modifiedString)))
            # and then remove the selected one, and return the result
            modifiedString = modifiedString[:delChar] + modifiedString[delChar + 1:]

        # return the modified string
        return modifiedString


    # STEP 3    
    # transform name to alien-name    
    def insertApostropheAndH(self, string):

        vowel = 'aeiou'
        numOfVowels = 0
        vowelPos = []
        
        # count the vowels
        for i, s in enumerate(string):
            if s in vowel:
                numOfVowels += 1
                vowelPos.append(i)    
                
        # if there are no vowels in the name:
        if numOfVowels == 0:
            # he/she already have a special name...
            return string.capitalize()
            
        # if there are only one vowel:        
        elif numOfVowels == 1:
            # if it's in the beginning, or in the end, remove it!
            if vowelPos[0] == 0:            
                return string[vowelPos[0] + 1:].capitalize()
            elif vowelPos == len(string) - 1:
                return string[:vowelPos[0] - 1].capitalize()
            # if it's somewhere in the middle:
            else:
                return string[:vowelPos[0]].capitalize() + '\'h' + string[vowelPos[0]:]
                
        # if there are more than one vowel in the name:
        elif numOfVowels > 1:
            # pick one randomly
            modPos = choice(vowelPos)
            # if it's in the beginning, or in the end, remove it!
            if modPos == 0:
                return string[modPos + 1:].capitalize()
            elif modPos == len(string) - 1:
                return string[:modPos - 1].capitalize()
            # if it's somewhere in the middle:
            else:
                return string[:modPos].capitalize() + '\'h' + string[modPos:]
        


    # START PROCESS
    # make your name looks like an Alien's name    
    def alienize(self):
        """ Create the name. """
        
        # replace umlaut characters, handles utf-8 encoding, and split the name
        names = self.umlautTransform(self.name.decode('utf-8').lower()).encode('ascii').split(' ')
        alienName = []
        
        # for every part of the name,
        for i, name in enumerate(names):
            # remove a random char, and try to add a 'h to it
            alienName.append(self.insertApostropheAndH(self.removeRandomChar(name)))
            # if it's not the last part, add a whitespace
            if len(names) != 1 and i < len(names):
                alienName.append(' ')
        
        # join the parts
        self.name = ''.join(alienName)



# ---------------------------------- Planet -----------------------------------



    # STEP 1
    # get a list of planet names.
    def getAllPlanet(self):
        # init the Elite based random planet name generator
        # originally it's part of Ian Bell's txtelite.c 1.2 (and parts of 1.4)
        # but later implemented in python. I found the solution in
        # http://automaticromantic.com/static/misc/pytxtelite.txt
        # but I use Laszló Szathmáry's (jabba.laci@gmail.com) cleaned version
        # of it.
        galaxy = data.pyplanets.Galaxy()
        # go to galaxy #1
        galaxy.goto_galaxy(1)
        
        # return the planets of the selected galaxy
        return galaxy.planets
    
    
    # compute the similarity
    def matchingElementsOfMultiSets(self, multi1, multi2):
        """ Compute the number of matching elements of two multisets. """
        # parameter
        num = 0
        
        # for every element in the first multiset,
        for elem in multi1:
            # if we find a matching element in the second,
            if elem in multi2:
                # increase the parameter by the smaller number of occurences
                num += min(multi1[elem], multi2[elem])
        
        # return the number of matches
        return num
    
    
    
    
    # START PROCESS
    # select the best planet name from the existing planet names
    def getPlanet(self):
        """ Select the best matching planet for the name. """
        
        # get the planets
        planets = self.getAllPlanet()
        # select the first planet
        selectedPlanet = planets[0]
        
        # get all the characters from the name
        selectedName = col.Counter(self.name.lower())
        
        # get the actual number of matching characters
        maxima = self.matchingElementsOfMultiSets(selectedName, col.Counter(selectedPlanet.lower())) 
        # previous solution:
        # maxima = len(selectedName.intersection(set(selectedPlanet.lower())))
        
        # for every planet,
        for planet in planets:
            # computes similarity
            similarity = self.matchingElementsOfMultiSets(selectedName, col.Counter(planet.lower()))
            
            # if it's more similar then
            if similarity >= maxima:
                # select the planet name, and update the maximum value
                maxima = similarity
                selectedPlanet = planet

        # set the selected planet name
        self.planet = selectedPlanet



# main function
if __name__ == '__main__':
    print '\n\tWelcome in Alien Name Generator ver ', VERSION, '!\n'
    inName = raw_input('Please enter your name! > ')
    if len(inName) == 0:
        print 'Next time try to write an actual name...'
    else:   
        alienNameGenerator = Alienize(inName)
        print 'Your alien name is > ', alienNameGenerator.getName()
