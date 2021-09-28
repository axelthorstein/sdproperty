def get_subkey_from_dict(dictionary, subkeys):
    subkeys = list(subkeys)

    for subkey in subkeys:
        if dictionary.get(subkey):
            dictionary = dictionary.get(subkey, {})

    return dictionary


def combine_dicts(dict1, dict2):
    # If there are overlapping keys the value will be taken from the kwarg.
    combined_dict = dict1.copy()
    combined_dict.update(dict2)

    return combined_dict


def combine_lists(list1, list2):
    # Only the first occurance of a common value will be taken.
    for element in list2:
        if element not in list1:
            list1.append(element)

    return list1
