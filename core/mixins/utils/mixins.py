import re

def name_to_url(name):
    result = ''
    valid_symbols = "abcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;="

    for symbol in name.lower():
        if symbol in valid_symbols:
            result += symbol
    return result
