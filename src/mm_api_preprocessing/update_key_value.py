def update_key_value(data, key, delimiter):
    """
    Updates the value of a specific key in a list of dictionaries by splitting 
    it with a delimiter and keeping only the first part of the split.

    Args:
    - data (list of dict): The list of dictionaries.
    - key (str): The key to look for in the dictionaries.
    - delimiter (str): The delimiter to split the value.

    Returns:
    - list of dict: The updated list of dictionaries.
    """
    for item in data:
        if key in item:
            if delimiter in item[key]:  # Ensure the key exists and the value is a string
                item[key] = item[key].split(delimiter)[0].lower()  # Replace with the first part of the split
            else:
                item[key] = item[key].lower()
    return data