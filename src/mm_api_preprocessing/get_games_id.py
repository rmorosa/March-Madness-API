def get_games_id(key,delimiter):
    """
    Gets the group identifier of a key value
    
    Parameters:
    text (string): The key that is separatd by a delimiter
    delimiter (string): The delimiter separating each word of the string
    
    Returns:
    string: The first two indexes of the key value combined into a string
    """
    if delimiter in key:
        key_word_list = key.split(delimiter)
        first_two_indexes_of_key = ''.join(key_word_list[0:2])

        # Return the first tindexes as one string
        return first_two_indexes_of_key
    else:
        return "There is no delimiter in the key"