import re as Re # importing for regex pattern.


def check_valid_note( substring: str ) -> bool:
    """
    Description:
    Checks whether a substring meets the criteria set for being a valid musical note.

    Parameters:
    @param substring: The string that will be checked if it is a valid music note.

    Returns:
    @return bool: True if the substring is a valid music note or otherwise it's False.
    """
    
    
    """
    Compiling the regex pattern that will check if it matches the criteria for being a valid music note.
    
    >> Note length must have 1-2 digits only. Optional input.
    >> Note pitch must be either any one letter from [a-g] with '#' as an option, or only p. Compulsory input.
    >> Note scale must be a digit from [1-8] only. Optional input.
    
    Fullstop in the end is optional.
    """
    pattern : object = Re.compile(r"(^\d{1,2})?([a-g]{1}(#)?|p{1})([1-8]{1})?(\.)?$")
    
    # stores True if the substring matches, otherwise stores None.
    substringMatch: object = pattern.match(substring)
    
    
    # if the substring matches with the criteria,
    if substringMatch:
        
        # we will get the note length from the substring
        noteLength: str = substringMatch.group(1)
        
        # if noteLength exists,
        if noteLength:
            
            # we need to check if the note length is either numbers 1,2,4,8,16 or 32.
            if not int(noteLength) in [1,2,4,8,16,32]:
                return False
            
        # return True if everything does meet the criteria, given that note length is entered correctly or is not entered at all.
        return True
    
    # otherwise, return false.
    return False

def generate_valid_ringtone( ringtone: str ) -> list:
    """
    Description: Returns a list of title, default values and notes data from a given
                 ringtone. Returns an empty list if the given ringtone string does not meet
                 the criteria.

    Parameters:
    @param ringtone: Ringtone string that contains all of the data.

    Returns:
    @return list: A list containing the details of the ringtone.
    """
    
    # if there is no string, return empty list.
    if not any( ringtone ):
        return []
    
    # splitting the string into respective fields: title, default values, and note data.
    optionalData : tuple
    noteData: str
    
    *optionalData, noteData = Re.split( ':', ringtone )
    
    # converting all characters to lowercase in notedata and stripping any whitespace.
    noteData : str = Re.sub(r'\s','',noteData).lower()
    
    ###TECHNIQUE: LIST COMPREHENSION###
    # checking if all of the substrings in the note data is a valid note.
    if all( [ check_valid_note( substring ) for substring in Re.split( ',', noteData )] ):
        
        # now we will check if the default values syntax is correct or not.
        
        # default values section must be either empty or must have d=x,o=x,b=x for some number x.
        defaultValuesPattern : object = Re.compile( r"^(\s*|(d=[1-9]\d*,o=[1-9]\d*,b=[1-9]\d*))$" )
        
        # if there is any optional data written,
        if any (optionalData):
            
            # if the default values are matching the criteria.
            if defaultValuesPattern.match( Re.sub( r'\s','',optionalData[-1] ).lower() ):
                
                # return only empty title, default values and notedata if only default values are given, else print all three criterias.
                listToAppend : list = [ Re.sub(r'\s','',optionalData[-1]).lower() ] + [ noteData ]
                return [''] + listToAppend if len(optionalData) == 1 else [ optionalData[0].lstrip().rstrip() ] + listToAppend
        
        else:
            # if there is no title or default values given, print only the note data with empty title and default values.
            return [''] * 2 + [ noteData ]

        
    return [] # if the ringtone fails to meet all of the criteria.

def get_ringtone_notes( defaultValues: str, noteData: str ) -> list:
    """
    Description: Returns a list of notes to play with specific note durations and playback note numbers
                 from a given default values and note data.

    Parameters:
    @param defaultValues: The default values set for the note length, note scale, and the beat.
    @param noteData: The note data that the ringtone consists of.

    Returns:
    @return list: Returns a nested list of musical notes from the given parameters.
    """
    # Using a regex pattern to compile each note data in the noteData string.
    pattern : object = Re.compile(r"(^\d{1,2})?([a-g]{1}(#)?|p{1})([1-8]{1})?(\.)?$")
    
    # default values for the music note data.
    d : int = 4 # note length default value
    o : int = 5 # note scale default value
    b : int = 60 # beats default value
    
    # dictionary to store the note pitch and its corresponding scale value.
    dictionaryOfPitchScale : dict = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11, 'P': -400}
    
    # final list that stores musical notes to be played. 
    listOfNotes : list = []
    
    # if the user defines their own default values, it will override the pre-defined program defaults above.
    if defaultValues:    
        d, o, b = ( int(number) for number in Re.findall(r'\b\d+\b', defaultValues) )
        
    
    # iterating through each note data separated by the delimter ','
    for note in Re.split(',', noteData):
        
        hasFullStop : bool = False
        playBackNote : int = 0
        
        noteMatch : object = pattern.match(note) # regex pattern match object
        
        # getting the values of the length, scale, pitch, and whether a fullstop is there or not.
        noteLength : str = noteMatch.group(1)
        noteScale : str = noteMatch.group(4)
        noteFullStop : str = noteMatch.group(5)
        notePitch: str = noteMatch.group(2)
        
        noteLength : int = int(noteLength) if noteLength else d # Overriding noteLength if there is any given.
        noteScale : int = int(noteScale) if noteScale else o # Overriding noteScale if there is any given.
        hasFullStop : bool = True if noteFullStop else False
        
        quarterDuration : float = 60 / b # 60 / note beats
        noteDuration : float = ( ( 4 / noteLength ) * quarterDuration ) if not hasFullStop else ( ( 4 / noteLength ) * quarterDuration ) * 1.5
        
        noteDuration = round(noteDuration, 2)
        # if there is a character given from [a-g] or p, and if its not p,
        pitchLetter: str = notePitch[0]
        if notePitch and 'p' not in notePitch:
            
            # if there is a #, we need to add one to the value
            if not noteMatch.group(3):
                playBackNote = ( dictionaryOfPitchScale[pitchLetter.upper()] + ((noteScale - 1) * 12))
            else:
                playBackNote = ( dictionaryOfPitchScale[pitchLetter.upper()] + 1 + ((noteScale - 1) * 12))

        elif 'p' in notePitch:
            # if it is a p,
            playBackNote = dictionaryOfPitchScale[pitchLetter.upper()]
            
        listOfNotes.append( [noteDuration, playBackNote] )
    
    return listOfNotes

def generate_commands( ringtonesLists: list, songTitlesLists: list ) -> tuple:
    """
    Description: The function will return a string of javascript commands from the given lists
                 of ringtone data and song titles.

    Parameters:
    @param ringtonesLists : A list of ringtone details.
    @param songTitlesLists: A list of ringtont titles.
    
    Returns:
    @return tuple: A tuple of javascript commands for playing the ringtone and displaying the titles.
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
        
    position : int = 0 # Overriding to reuse the variable again.
    for title in songTitlesLists:
        
        # if a title exists
        if title:
            titleRingtones += f"<p><a href='javascript:play{position}();'>PLAY {title.upper()}</a></p>"
        # if the title does not exist
        else:
            titleRingtones += f"<p><a href='javascript:play{position}();'>PLAY UNTITLED SONG</a></p>"
        
        position += 1
        if position < len(songTitlesLists):
            titleRingtones += "\n"       
    
    return (validRingtones, titleRingtones)
    
def convert_song_file( fileName: str ) -> tuple:
    """
    Description: The function returns a set of ringtone titles and ringtoneNotes to play for
                 each title given.

    Parameters:
    @param fileName: The file that the algorithm will read and extract ringtone data from.

    Returns:
    @return tuple: A tuple of titles list and ringtone notes list.
    """
    
    # variables to store the results
    listOfRingtones: list = []
    numberOfFileLines : int = 0
    
    # using try-except
    try:
        songFile : object = open(fileName, 'r')
        currentFile : list = songFile.readlines()
        numberOfFileLines = len(currentFile)
        
        listOfRingtones = [ line for line in currentFile if Re.sub(r'\s','',line) ]
        
        songFile.close()
        
    except FileNotFoundError:
        raise FileNotFoundError("File does not exist!")
    
    listOfRingtones = [ generate_valid_ringtone( ringtone ) for ringtone in listOfRingtones if any(generate_valid_ringtone(ringtone)) ]
    print(f"Read {numberOfFileLines} lines from \"{fileName}\".\nGenerated {len(listOfRingtones)} valid songs.")

    titles : list = []
    ringtoneNotes : list = []
    
    for ringtoneDetail in listOfRingtones:
        titles.append(ringtoneDetail[0])
        ringtoneNotes.append( get_ringtone_notes(ringtoneDetail[1], ringtoneDetail[2]) )
        
    with open('play_ringtones.html', 'w') as ringtoneFile:

        ringtoneFile.write("<html>\n<head>\n<script src='WebAudioFontPlayer.js'></script>\n<script src='Soundfile_sf2.js'></script>\n<script>\nvar preset=soundfile_sf2;\nvar AudioContextFunc = window.AudioContext || window.webkitAudioContext;\nvar AC = new AudioContextFunc();\nvar player=new WebAudioFontPlayer();\nplayer.adjustPreset(AC,preset);\n")
        ringtoneFile.write( generate_commands(ringtoneNotes, titles)[0] )
        ringtoneFile.write("\n</script>\n</head>\n<body>\n<h1>\"Mamba Number Py\" Ringtone Interpreter</h1>\n")
        ringtoneFile.write( generate_commands(ringtoneNotes, titles)[1] )
        ringtoneFile.write("\n</body>\n</html>")
        
    return (titles, ringtoneNotes)
    

def concatenateJavaScriptCommands(ringtoneList: list, position : int = 0, endTime : float = 0.0, stringToReturn="") -> str:
    if position >= len(ringtoneList):
        return stringToReturn
    
    ringtone = ringtoneList[position]
    stringToReturn += f"var audioBufferSourceNode = player.queueWaveTable(AC, AC.destination, preset, AC.currentTime+{round(endTime, 2)}, {ringtone[1]}, {ringtone[0]});\n"
    
    return concatenateJavaScriptCommands(ringtoneList, position + 1, endTime + ringtone[0], stringToReturn)

if __name__ == '__main__':
    titles, ringtone_notes = convert_song_file("file1.txt")
    print(titles)
    print(ringtone_notes)


