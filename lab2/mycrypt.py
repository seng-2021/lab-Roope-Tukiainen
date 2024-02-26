import codecs

def encode(s):
    if not isinstance(s,str):
        raise TypeError
    valid_chars = set
    (
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
        "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", 
        "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7",
        "8", "9", "!", '"', "#", "€", "%", "&", "/", "(", ")", "=", "'"
    )
    origlen = len(s)
    crypted = ""
    non_letter_mapping = dict(zip('1234567890!"#€%&/()=','!"#€%&/()=1234567890'))
    if len(s) > 1000:
        raise ValueError
    for c in s:
        if c.isalpha():
            if not c.lower() in valid_chars:
                raise ValueError
            if c.islower():
                c=c.upper()
            else:
                c=c.lower()
            # Rot13 the character for maximum security
            crypted+=codecs.encode(c,'rot13')
        else:
            if not c in valid_chars:
                raise ValueError
            crypted+=non_letter_mapping[c]

    return crypted

def decode(s):
    return encode(s)

