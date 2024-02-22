import re as Re # regex library for string comparison.

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
    

    

#used for manual testing purpose
if __name__ == "__main__":
    
    # creating testcases for the function.
    ringtoneTrues: list = ['Scale:d=4,o=5,b=60:4c5,4d5,4e5,4f5,4g5,4a5,4b5,4c6', 'd=8,o=4,b=100:4c5,4d5,4e5,4f5,4g5,4a5,4b5,4c6', '4c6,4b5,4a5,4g5,4f5,4e5,4d5,4c5', 'Twinkle Twinkle:d=4,o=5,b=80:32p,8c,8c,8g,8g,8a,8a,g', 'D= 8 , O  =  4,B =100 :4c5, 4d5,4 e5, 4f 5,4g5, 4a5,  4B5, 4C 6', '4c6,    4b 5,4A 5,4 g5,  4f5, 4e5, 4D5,4C5', 'Twinkle Twinkle : d =4 ,o= 5, B=80: 32p,8 c, 8 c,    8g,   8G,8 A ,8A,    G', 'Scale::4c5']
    ringtoneFalses: list = ['Twinkle Twinkle : d=4 ,o=5, c=80: 32p,8c, 8c,    8g,   8G,8A ,8A,    G', 'd=4 ,b =80 ,   o=5 : 32p,     8c, 8c,    8 g  ,   8G,8A ,8A,    G', 'Twinkle Twinkle: d=4,o=5, B=80:32p,8c,8 c,40g,8g,8a ,8a,12g6', 'Twinkle Twinkle: d=4,o=5, b=80:32P,8m,8c,8g,8g,8AAA ,8A,g', 'Twinkle Twinkle: d=4,o=5, b=80:32p,8  c,8c,86,8g,45 ,8a,g', 'Twinkle Twinkle : d=4 *o=5, B=80: 32p*8c* 8c*    8  g,   8G,8A ,8A,    G', 'Twinkle Twinkle: d=4-o=5- b=80:32p-8c-8  c,8g,8g,8a ,8a-g', 'Twinkle Twinkle: d=4,o=5,b=80', 'Scale:d=-4,o=-5,b=-60:4c5,4d5,4e5,4f5,4g5,4a5,4b5,4c6']
    
    for ringtone in ringtoneTrues:
        print(ringtone)
        print(generate_valid_ringtone(ringtone))
        print()
    
    for ringtone in ringtoneFalses:
        print(ringtone)
        print(generate_valid_ringtone(ringtone))
        print()