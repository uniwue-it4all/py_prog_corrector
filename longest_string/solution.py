def longest_string(my_list):
    longest = ""
    for string in my_list:
        if len(string) > len(longest):
            longest = string
    return longest
