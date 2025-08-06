def get_num_of_zeros(roundIndex):
    # Based on the column of the round, this is how many zeros should be filled in the round columns for that row
    num_of_zeros = {
        3:6,
        4:5,
        5:4,
        6:3,
        7:2,
        8:1
    }
    return num_of_zeros[roundIndex] # Add one to account for index