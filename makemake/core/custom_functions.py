def left_pad(number=0, digits=4, char='0'):
    assert (number >= 0), "Sorry, no numbers below zero"
    assert (len(str(number)) <= digits), ' '.join(("Sorry, number of digits exceeds", str(digits), "."))
    assert (len(char) < 2), "Sorry, number of characters exceeds 1."
    string = char * digits
    number = str(number)
    stop = digits - len(number)
    return ''.join((string[:stop], number))


def get_text_choices(value, choices):
    for key, text in choices:
        if key == value:
            return text
    return ''
