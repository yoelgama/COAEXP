list_numbers = list(range(1, 96))
print(list_numbers)


def create_chunks(list_name, n):
    for i in range(0, len(list_name), n):
        yield list_name[i:i + n]



# Call the 'create_chunks' function to divide the list further into sub-lists of 10 items each
print(list(create_chunks(list_numbers, 10)))
