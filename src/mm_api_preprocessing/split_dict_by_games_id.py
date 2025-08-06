from src.mm_api_preprocessing.get_games_id import get_games_id

def split_dict_by_games_id(input_dict,strip_word):
    """
    Splits a dictionary into a list of dictionaries based on the numeric part in the keys.
    
    Parameters:
    input_dict (dict): The input dictionary with keys containing numbers.
    
    Returns:
    list: A list of dictionaries grouped by the numeric part in the keys.
    """
    grouped_dicts = {}
    delimiter = "_"

    # Iterate over the input dictionary
    for key, value in input_dict.items():
        
        if strip_word in key:
            # Take the part after strip_word
            new_key = key.split(strip_word, 1)[1]
        else:
            continue  # If strip_word not found, move on to the next iteration

        # Extract the numeric part from the key
        games_identifier = get_games_id(key,delimiter)

        # Initialize a new dictionary in the grouped_dicts if the games id is not yet a key
        if games_identifier not in grouped_dicts:
            grouped_dicts[games_identifier] = {}
        
        # Add the key-value pair to the corresponding grouped dictionary
        grouped_dicts[games_identifier][new_key] = value
    
    # Step 2: Convert grouped dictionaries into a list
    list_of_dicts = [grouped_dicts[games_identifier] for games_identifier in grouped_dicts]

    return list_of_dicts
