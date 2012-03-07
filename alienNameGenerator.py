# -*- coding:Utf-8 -*-
VERSION = '0.1'
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


# STEP 1
# transform umlaut characters to their non-umlaut version
def umlautTransform(string):
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

    return nonUmlaut

    
# STEP 2    
# remove a random character from the name
def removeRandomChar(string):
    delChar = choice(range(0, len(string)))
    return string[:delChar] + string[delChar + 1:]


# STEP 3    
# transform name to alien-name    
def insertApostropheAndH(string):

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
            return string[:vowelPos[0]].capitalize() + '\' h' + string[vowelPos[0]:]
            
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
            return string[:modPos].capitalize() + '\' h' + string[modPos:]
    

# START PROCESS
# make your name looks like an Alien's name    
def Alienize(string):
    names = umlautTransform(string.decode('utf-8').lower()).encode('ascii').split(' ')
    alienName = []
    
    for name in names:
        alienName.append(insertApostropheAndH(removeRandomChar(name)))
        alienName.append(' ')        
        
    return ''.join(alienName)



# main function
if __name__ == '__main__':
    print 'Welcome in Alien Name Generator ver ', VERSION, '!'
    inName = raw_input('Please enter your name! > ')
    if len(inName) == 0:
        print 'Next time try to write an actual name...'
    else:   
        name = Alienize(inName)
        print 'Your alien name is > ', name
