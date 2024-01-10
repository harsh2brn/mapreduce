def main(params):
    shuffle_dict = {}
    for key, value in params:
        if key in shuffle_dict:
            shuffle_dict[key].append(value)
        else:
            shuffle_dict[key] = [value]
    return shuffle_dict
