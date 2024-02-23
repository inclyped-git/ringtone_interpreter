__author__ = 'inclyped et al.'

### IMPORT STATEMENTS ###
import re as Re # import regex pattern recognition.
import unittest # import unittesting library.

### TASK 1 ###
def check_valid_note( substring : str ) -> bool:
    
    """
    
    Description:
    Checks whether a substring meets the given criteria set for being a valid musical note.
    
    Parameters:
    @param substring: The string that will be checked if it is a valid music note.
    
    Returns:
    @return bool: True if the substring is a valid music note or otherwise it's False.
    
    """
    
    # creating a regex pattern that contains all the rules that make a musical note valid.
    notePattern : re.Pattern = Re.compile(r"(^\d{1,2})?([a-g]{1}(#)?|p{1})([1-8]{1})?(\.)?$")
    
    # stores a match object if the substring matches the regex pattern. Otherwise, stores a None.
    substringMatch : re.Match = notePattern.match( substring )
    
    # if there is a match,
    if substringMatch:
        
        # we need to check the note length specifically is correct or not.
        noteLength : str = substringMatch.group(1)
        
        # since note length is optional, we can check if it exists.
        if noteLength:
            
            # if it exists, we need to check if the note length meets the criteria set.
            # the valid lengths are 1,2,4,8,16,32.
            if not int(noteLength) in [1,2,4,8,16,32]:
                return False
        
        # since the other attributes of the substring is checked within the regex pattern, we can just return True.
        return True
    
    # if the match fails,
    return False

### TASK 2 ###
def generate_valid_ringtone( ringtoneDetails : str ) -> list:
    
    """
    
    Description:
    Returns a list of title, default values, and notes data of a valid ringtone. If the ringtone
    is not valid, it returns an empty list.
    
    Parameters:
    @param ringtoneDetails: The details that contain information about a specific ringtone.
    
    Returns:
    @return list: An empty list or list with corresponding ringtone's title, default values and note data.
    
    """
    
    # if there is no string, return empty list.
    if not any ( ringtoneDetails ):
        return []
    
    # splitting the string into three distinctive fields.
    optionalData : tuple
    noteData : str
    
    # creates an packed iterable if default values or default values and title were given. noteData is compulsory.
    *optionalData, noteData = Re.split( ':', ringtoneDetails )
    
    # converting all characters to lowercase in noteData and stripping any whitespace.
    noteData = Re.sub( r'\s', '', noteData ).lower()
    
    ###TECHNIQUE: LIST COMPREHENSION###
    # checking if all of the note data is correct.
    # Split the note data in separate substrings, and checks each substring is valid or not. all() checks if all the data in the list is truthy.
    if all ( [ check_valid_note( substring ) for substring in Re.split( ',' , noteData ) ] ):
        
        # we need to check if the default values pattern is correctly written or not.
        defaultValuesPattern: re.Pattern = Re.compile( r"^(\s*|(d=[1-9]\d*,o=[1-9]\d*,b=[1-9]\d*))$" )
        
        # if there is any optional data written,
        if optionalData:
            
            # stripping off whitespace and converting default values to lower case.
            optionalData[-1] : str = Re.sub( r'\s','',optionalData[-1] ).lower()
            
            # if the default values are written correctly,
            if defaultValuesPattern.match( optionalData[-1] ):
                
                # if the length of the optionalData iterable is 1, only default values and note data were given.
                # otherwise, all of the three fields were given in the ringtone details.
                tempListToAppend : list = [ optionalData[-1], noteData ]
                return [''] + tempListToAppend if len(optionalData) == 1 else [ optionalData[0].lstrip().rstrip() ] + tempListToAppend
        
        # otherwise return empty title and default values, with the note data.
        else:
            return [''] * 2 + [ noteData ]
    
    # if the ringtone details given fail to meet at least one of the criteria, return empty list.
    return []
    
### TASK 4 ###            
def get_ringtone_notes( defaultValues : str, noteData : str ) -> list:
    
    """
    
    Description:
    Returns a list of notes to play with specific note durations and playback note numbers
    from a given default values and note data.
    
    Parameters:
    @param defaultValues: The default values set for the note length, scale and beats.
    
    Returns:
    @return list: Returns a nested list of musical notes from the given parameters.
     
    """
    # similar to task 1, storing the regex pattern for a specific substring.
    notePattern : re.Pattern = Re.compile(r"(^\d{1,2})?([a-g]{1}(#)?|p{1})([1-8]{1})?(\.)?$")
    
    # default values for the music note data.
    d : int = 4; o : int = 5; b : int = 60;
    
    # dictionary to store the note pitch and its corresponding scale value.
    dictionaryOfPitchScales : dict = {
        'C' : 0, 'D' : 2, 'E' : 4,
        'F' : 5, 'G' : 7, 'A' : 9,
        'B' : 11, 'P' : -400
    }
    
    # final list to store the list of playable notes.
    listOfNotes : list = []
    
    ###TECHNIQUE: TUPLE COMPREHENSION###
    # if the default values are given, override the defaults given above.
    # findall() returns a list of numbers found inside the default values string, and puts each number into respective variables.
    if defaultValues:
        d,o,b = ( int(number) for number in Re.findall(r'\b\d+\b', defaultValues) )
        
    
    # iterating through each substring of the note data string.
    for note in Re.split(',', noteData):
        
        hasFullStop : bool = False
        playBackNote : int = 0
        
        noteMatch : re.Match = notePattern.match(note)
        
        # getting the values of the length, scale, pitch, and fullstop.
        noteLength : str = noteMatch.group(1)
        noteScale : str = noteMatch.group(4)
        noteFullStop : str = noteMatch.group(5)
        notePitch : str = noteMatch.group(2)
        
        # overriding variables accordingly.
        noteLength : int = int ( noteLength ) if noteLength else d
        noteScale : int = int( noteScale ) if noteScale else o
        hasFullStop : bool = True if noteFullStop else False
        
        # calculating the noteDuration
        noteDuration : float =  ( ( 4 / noteLength ) * ( 60 / b ) ) 
        noteDuration = noteDuration if not hasFullStop else noteDuration * 1.5
        noteDuration = round( noteDuration, 2 )
        
        # grabbing the note pitch and extracting its letter.
        pitchLetter : chr = notePitch[0]
        playBackNote : int = dictionaryOfPitchScales[ pitchLetter.upper() ]
        
        # if there is a '#' we need to add one to the value.
        if 'p' in pitchLetter:
            pass # if there is a p, return the playBackNote value stored inside the dictionary.
        elif not noteMatch.group(3):
            playBackNote = playBackNote + ( (noteScale - 1) * 12 )
        else:
            playBackNote = playBackNote + 1 + ( (noteScale -1) * 12 )
        
        listOfNotes.append( [ noteDuration, playBackNote ] )
    
    return listOfNotes # returns the list of notes to be played.
        
### TASK 5 ###
def generate_commands( ringtonesLists : list, songTitlesLists : list ) -> tuple:
    
    """
    
    Description:
    The function will return a string of JavaScript commands from the given lists of ringtone
    data and song titles.
    
    Parameters:
    @param ringtonesLists: A list of ringtone details.
    @param songTitlesLists: A list of ringtone titles.
    
    Returns:
    @return tuple: A tuple of JavaScript commands and anchor HTML statements.
    
    """
    
    # variables to store the end results
    validRingtones : str = ""
    titleRingtones : str = ""
    
    # iterating through each nested list of ringtones lists.
    position : int = 0
    for ringtoneList in ringtonesLists:
        
        validRingtones += "function play" + str(position) + "() {\n"
        validRingtones += concatenateJavaScriptCommands(ringtoneList)
        validRingtones += "}"
        
        position += 1
        if position < len(ringtonesLists):
            validRingtones += "\n"
    
    position : int = 0 # Overriding
    for title in songTitlesLists:
        
        # if a title exists,
        finalTitle : str = title if title else "UNTITLED SONG"
        titleRingtones += f"<p><a href='javascript:play{position}();'>PLAY {finalTitle.upper()}</a></p>"
        
        position += 1
        if position < len(songTitlesLists):
            titleRingtones += "\n"
        
    return ( validRingtones, titleRingtones )
        
### TASK 6 ###
def convert_song_file( fileName: str ) -> list:
    
    """
    
    Description:
    The function returns a set of ringotne titles and ringtone notes to play for each title given.
    
    Parameters:
    @param file: The name of the file where the data will be extracted.
    
    Returns:
    @return list: A list of titles list and ringtone notes list.
        
    """
    
    # variables to store the results
    listOfRingtones : list = []
    numberOfLines : int = 0
    
    ###TECHNIQUE: EXCEPTION HANDLING###
    try:
        songFile : _io.TextIOWrapper = open(fileName, 'r')
        currentFile : list = songFile.readlines()
        numberOfLines = len(currentFile)
        
        ###TECHNIQUE: LIST COMPREHENSION###
        listOfRingtones = [ line for line in currentFile if Re.sub(r'\s','',line) ] # removing empty lines from the file.
        
        songFile.close()
        
    except FileNotFoundError: # in case the file was not found.
        raise FileNotFoundError(f'FILE {fileName} NOT FOUND') 
        
    except IOError: # in case of any errors in working with the file.
        raise IOError(f"COULD NOT READ FILE {fileName}")
    
    ###TECHNIQUE: LIST COMPREHENSION###
    # further filtering out the invalid ringtones from the listOfRingtones.
    listOfRingtones = [ generate_valid_ringtone( ringtoneDetail ) for ringtoneDetail in listOfRingtones if any(generate_valid_ringtone(ringtoneDetail)) ]
    
    print(f"Read {numberOfLines} lines from \"{fileName}\".\nGenerated {len(listOfRingtones)} valid songs.")
    
    # variables to store the final titles, and ringtone notes.
    titles : list = []
    ringtoneNotes : list = []
    
    # appending each title and ringtone notes to corresponding variables.
    for ringtoneDetail in listOfRingtones:
        
        titles.append( ringtoneDetail[0] )
        ringtoneNotes.append( get_ringtone_notes(ringtoneDetail[1], ringtoneDetail[2]) )
    
    generateHTMLFile( ringtoneNotes, titles)
        
    return [titles, ringtoneNotes]
    
### HELPER FUNCTIONS ###
###TECHNIQUE: RECURSION###
def concatenateJavaScriptCommands(  ringtoneList : list, index : int = 0, endTime : float = 0.0, stringToReturn : str = "" ) -> str:
    """
    
    Description:
    Recursively appends JavaScript commands into a string variable, and returns the string.
    
    Parameters:
    @param ringtoneList: The list that contains ringtone information.
    @param index: Keeps track of how many notes are there inside the ringtoneList
    @param endTime: The time that each note ends.
    @param stringToReturn: The string that is to be returned
    
    Returns:
    @return str: The string of JavaScript commands.
    
    """
    
    if index >= len( ringtoneList ):
        return stringToReturn # BASE CASE: if the function reaches the end of the list, return the string.
    
    ringtoneDetail = ringtoneList[index]
    stringToReturn += f"var audioBufferSourceNode = player.queueWaveTable(AC, AC.destination, preset, AC.currentTime+{round(endTime, 2)}, {ringtoneDetail[1]}, {ringtoneDetail[0]});\n"
    
    return concatenateJavaScriptCommands(ringtoneList, index + 1, endTime + ringtoneDetail[0], stringToReturn) # RECURSIVE CASE: calling the function with updated parameters.

def generateHTMLFile( ringtoneDetails: list, titles: list ) -> None:
    """
    
    Description:
    This function generates a HTML file from given ringtone details and titles.

    Parameters:
    @param ringtoneDetails: A list containing all the ringtone details to play the ringtone.
    @param titles: A list containing the titles for each song.
    """
    # creating a new HTML file if it does not exist, and appending the commands needed to play music.
    with open('play_ringtones.html', 'w') as ringtoneFile:
        ringtoneFile.write("<html>\n<head>\n<script src='WebAudioFontPlayer.js'></script>\n<script src='Soundfile_sf2.js'></script>\n<script>\nvar preset=soundfile_sf2;\nvar AudioContextFunc = window.AudioContext || window.webkitAudioContext;\nvar AC = new AudioContextFunc();\nvar player=new WebAudioFontPlayer();\nplayer.adjustPreset(AC,preset);\n")
        ringtoneFile.write( generate_commands(ringtoneDetails, titles)[0] )
        ringtoneFile.write("\n</script>\n</head>\n<body>\n<h1>\"Mamba Number Py\" Ringtone Interpreter</h1>\n")
        ringtoneFile.write( generate_commands(ringtoneDetails, titles)[1] )
        ringtoneFile.write("\n</body>\n</html>")      

### TASK 3 ###
class RingtoneTestCase(unittest.TestCase):
    """
    
    RingtoneTestCase class contains behaviours that test the check_valid_note() and generate_valid_ringtone()
    functions individually, checking if the function behaves as intended when given different types of cases.
    
    """
    
    def test1_check_valid_note( self ):
        """
        
        Description: 
        Checks the boundary conditions of the substring's note length.
        It should pass for the values 1,32 and fail for values 0,33
        
        """
        noteLengthCases : list = [0,1,32,33] # boundary conditions for the function.
        
        for lengthCase in noteLengthCases:
            
            # if the length is not within the given criteria range, it should return False.
            if lengthCase == 0 or lengthCase == 33:
                assert check_valid_note( str(lengthCase) + 'a1' ) == False, "The test cases doesn't work for boundary condition lengths 0 or 33."
            
            else: # if it is within the range, return True.
                assert check_valid_note( str(lengthCase) + 'a1' ), "The test cases doesn't work for boundary condition lengths 1 or 32."
    
    def test2_check_valid_note( self ):
        # length negative numbers within range [1-32]
        """
        
        Description: 
        Checks if the function returns False for negative length numbers.
        
        """
        noteLengthCases : list = [-32,-16,-8,-4,-2,-1]
        
        for lengthCase in noteLengthCases:
            
            # if the length is a negative, it should return False.
            assert check_valid_note( str(lengthCase) + 'a1' ) == False, "The function does not return False for negative numbers!"
        
    def test3_check_valid_note( self ):
        """
        
        Description: 
        Checks whether the note pitch is within the range. Returns true if the character
        is between [a-g] with optional '#' or a p with no '#'. Returns false if the 
        condition is not met.
        
        """
        notePitchCases : list = ['h','h#','i','i#','y','y#','z','z#','p#'] # invalid pitches
        
        for pitchCase in notePitchCases:
            
            # throws AssertionError if the pitchCase evaluates to True.
            assert check_valid_note( pitchCase ) == False, "The function considers outside the range of [a-g] or accepts p with '#'"
    
    def test4_check_valid_note( self ):
        """
        
        Description: 
        Checks if the pitch is not a special character. 
        If it is, the function should return False.  
        
        """
        # special characters
        notePitchCases : str = ".,:;!?()<>*{}()&^$#@+-_=/%"
        
        for pitchCase in notePitchCases:
            # AssertionError is thrown if the special character is allowed to evaluate the function to true.
            assert check_valid_note( pitchCase ) == False, "The function accepts special characters as well!"

    def test5_check_valid_note( self ):
        """
        
        Description: 
        The function should return False if there is a negative number in the note scale.
        
        """
        # list of negative numbers
        noteScaleCases : list = [-1,-2,-3,-4,-5,-6,-7,-8]
        
        for scaleCase in noteScaleCases:
            # Passes the test case if the negative number evaluates the function to false.
            assert check_valid_note('1a' + str(scaleCase)) == False, "The function also accepts negative number!"
    
    def test6_check_valid_note( self ):
        """
        
        Description: 
        Returns False for false boundary conditions, returns True for boundary conditions
        within the range [1-8].
        
        """
        
        # note scale test cases.
        noteScaleCases : list = [0,1,8,9]
        
        for scaleCase in noteScaleCases:
            
            # should return false if the scales are outside the range.
            if scaleCase == 0 or scaleCase == 9:
                assert check_valid_note( '1a' + str(scaleCase) ) == False, "The function accepts boundary conditions 0 or 9, but it should not!"
            
            else: # otherwise it should return true.
                assert check_valid_note('1a' + str(scaleCase) ), "The function does not behave as intended for boundary conditions 1 or 8."
    
    def test1_generate_valid_ringtone( self ):
        """
        
        Description: 
        Checks if the function accepts negative default values and zero. It should return empty list if 
        negative values or zero are given. 
        
        """
        
        # test cases
        defaultValuesCases : list = [-1,0,-20,-69, -400]
        
        for valueCase in defaultValuesCases:
                
                # should return empty list if the default values are not non-zero positive integers.
                assert generate_valid_ringtone(f'd={valueCase},o={valueCase},b={valueCase}:4c3') == [], "The function does not check the default values for negative numbers or zero correctly!"

    def test2_generate_valid_ringtone( self ):
        """
        
        Description: 
        Checks if the order of the ringtone string is correct or not. Returns an empty list
        if the order is incorrect. 
        
        """
        
        # test cases of different orders.
        ringtoneCases : list = ['d=4,o=5,b=60:Scale:4c5,4d5,4e5,4f5,4g5,4a5,4b5,4c6', '4c5, 4d5,4 e5, 4f 5,4g5, 4a5,  4B5, 4C 6:D= 8 , O  =  4,B =100', ' 32p,8 c, 8 c,    8g,   8G,8 A ,8A,    G: Twinkle Twinkle'] 
        
        for ringtoneCase in ringtoneCases:
            # Gets an AssertionError if the function does not carefully consider the order of the ringtone details entered.
            assert generate_valid_ringtone(ringtoneCase) == [], "The function does not work as intended. The order of the ringtone was not considered carefully!"

### RUN METHOD ###
def run() -> None:
    """
    
    Description:
    This method contains all the behaviours that will simulate the ringtone interpreter.
    
    """
    
    # printing the introduction to the interpreter.
    print("\nTITLE")
    print("-"*10 + "\n\"Mamba Number Py\" Ringtone Interpreter\n" + "-"*10)
    print()
    
    print("SETUP")
    print("-" * 10)
    fileToRead : str = input("Please enter the file you want to read: ") # getting the file to read.
    songTitles, songRingtoneNotes = convert_song_file( fileToRead ) # returns the valid titles and ringtone notes within the file.    
    print("-" * 10)
    print()
    
    print("SONG TITLES")
    print("-"*10)
    titleIndex : int = 0
    for title in songTitles:
        print(f"{titleIndex} {title}")
        titleIndex += 1
    print("-"* 10)
    print()
    
    print("DISCARDING")
    print("-"* 10)
    choiceOfSongs : str = input("Select songs to discard (e.g. 1,2,4 or None): ")
    songsToDiscard : list = []
    
    if choiceOfSongs != "None":
        songsToDiscard = list( map (int, choiceOfSongs.split(",")))
        
    print("-" * 10)
    print()
    
    newTitles : list = [] # storing the titles that were not removed.
    newRingtoneDetails : list = [] # storing the ringtone details that were not removed.
    
    # looping through each valid ringtone and only keeping the ones the user did not remove.
    for i in range(len(songTitles)):
        
        if i not in songsToDiscard:
            newTitles.append(songTitles[i])
            newRingtoneDetails.append(songRingtoneNotes[i])
    
    print("UPDATED SONG TITLES")
    print("-"*10)
    titleIndex = 0 # Overriding
    for title in newTitles:
        print(f"{titleIndex} {title}")
        titleIndex += 1
    print("-" * 10)
    print()
    
    print("MODIFICATION OF SONGS")
    print("-"*10)
    
    titleIndex = 0
    for title in newTitles:
        print(f"{titleIndex} {title}")
        titleIndex += 1
    print()
    
    toModify : bool = input("Do you wish to modify any songs (Y/N)? ") == "Y" or False # asking the user if they want to modify songs.
    print()
    
    
    
    while toModify:
        
        selectedSong : int = int(input("Select song to modify: ")) # asking the user which song to select.
        print()
        
        # printing out the options.
        print("1 - Double length of each note (slower)")
        print("2 - Half length of each note (faster)")
        print("3 - Increase octave of each note ")
        print("4 - Decrease octave of each note ")
        
        print()
        
        # getting the option, and the title and ringtone details to be edited accordingly.
        selectedOption: int = int(input("Select option: "))
        selectedTitle : str = newTitles[selectedSong]
        selectedRingtoneDetails : list = newRingtoneDetails[selectedSong]
        
        # if the octave has to be changed, ask the user how much they want to change it by.
        if selectedOption in range(3,5):
            selectedOctave : int = int(input("How many octaves do you wish to increase? ")) 
        
        stringReplace : str = "" # string replacement
        
        # edits the ringtone details accordingly.
        for i in range(len(selectedRingtoneDetails)):
            
            if selectedOption is 1:
                selectedRingtoneDetails[i][0] *= 2 # doubling the note length to slow down.
                stringReplace = "2 times slower"
            elif selectedOption is 2:
                selectedRingtoneDetails[i][0] /= 2
                stringReplace = "2 times faster" # halving the note length to speed up.
            
            elif selectedOption is 3:
                selectedRingtoneDetails[i][1] += 12 * selectedOctave
                stringReplace = f"{selectedOctave} octaves higher" # increasing the playback no. depending on how many octaves entered.
                
            elif selectedOption is 4:
                selectedRingtoneDetails[i][1] -= 12 * selectedOctave        
                stringReplace = f"{selectedOctave} octaves lower" # decreasing the playback no. depening on the octaves entered.
        
        print(f"{selectedTitle} is now {stringReplace}")
        print()
        toModify = input("Do you wish to modify any songs (Y/N)? ") == "Y" or False # asks the user if they want to modify again.
    
    generateHTMLFile( newRingtoneDetails, newTitles ) # creating a HTML file after the new changes.
    print()
    print("\"play_ringtone.html\" file is generated and ready to play!")
    print()
    toUnitTest : bool = input("Do you wish to run unittest on Task 3 before exiting (Y/N)? ") == "Y" or False
    
    # runs the unit test if they want to test.
    if toUnitTest:
        unittest.main()
    
if __name__ == '__main__':
    run()
