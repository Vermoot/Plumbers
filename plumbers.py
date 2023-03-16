# Chords
# Chords in these dicts should be written without any '-', and can't contain an asterisk.
linker = "KWRAO"

unique = {
    "SRAO":      0,
    "WAOPB":     1,
    "TWO":       2,
    "THRAOE":    3,
    "TPOUR":     4,
    "TPAOEUF":   5,
    "SEUBGS":    6,
    "SEFPB":     7,
    "AET":       8,
    "TPHAOEUPB": 9,
    "TEPB":      10,
    "HREFPB":    11,
    "WAOFPB":    11,
    "TWEFL":     12,
    "STWFPB":    12,
    "STHRFPB":   13,
    "STPRFPB":   14,
    "STPHRFPB":  15,
    "SKHFPB":    16,
    "SKPHFPB":   17,
    "SKPRFPB":   18,
    "STWHFPB":    19,
}

starters = {
    "STKHR":     0,
    "WU":        1,
    "STW":       2,
    "STHR":      3,
    "STPR":      4,
    "STPHR":     5,
    "SKH":       6,
    "SKPH":      7,
    "SKPR":      8,
    "STWH":      9,
}

enders = {
    "UPB":       1,
    "AO":        2,
    "AOE":       3,
    "OUR":       4,
    "AOEUF":     5,
    "EUBGS":     6,
    "EFPB":      7,
    "AET":       8,
    "AOEUPB":    9,
}

big_enders = {
    "T":         10,
    "DZ":        100,
    "PBD":       1000,
    "FPL":       1000000,
    "BL":        1000000000
}

separators = {
    "KPHA*":     ",",
    "SP*":       " ",
    "PR*":       ".",
}

# "One hundred **and** twenty" vs "One hundred twenty"
write_and = True

# "One thousand, one hundred" vs "One thousand one hundred"
# Probably unneccessary, since it's very uncommon to be writing numbers without commas
write_commas = True



# Sort the lists by key length, so that you don't catch UPB for AOEUPB
for dict in (starters, enders, big_enders):
    list(dict.items()).sort(key=lambda x:len(x[0]),reverse=False)

def oom(n:int) -> int:
    """Return the order of magnitude of a number"""
    return len(str(n))

def num_to_words(num):
    """
    Converts a number to its written-out form.
    Commas and "and" are toggleable with variables depending on your preference.

    Args:
        num (int): The number to convert.

    Returns:
        str: The written-out form of the number.
    """

    ones  = ['zero',        'one',        'two',        'three',     'four',     'five',        'six',     'seven',     'eight',    'nine']
    tens  = ['ten',         'twenty',     'thirty',     'forty',     'fifty',    'sixty',       'seventy', 'eighty',    'ninety']
    teens = ['ten',         'eleven',     'twelve',     'thirteen',  'fourteen', 'fifteen',     'sixteen', 'seventeen', 'eighteen', 'nineteen']
    bigs  = ['',            'thousand',   'million',    'billion',   'trillion', 'quadrillion',
             'quintillion', 'sextillion', 'septillion', 'octillion', 'nonillion']

    if num < 10:
        return ones[num]
    if num < 20:
        return teens[num - 10]
    if num < 100:
        return tens[num // 10 - 1] + ('' if num % 10 == 0 else '-' + ones[num % 10])
    if num < 1000:
        return ones[num // 100] + ' hundred' + ((' and ' if write_and else ' ') + num_to_words(num % 100) if num % 100 > 0 else '')

    words = ''
    for i in range(len(bigs)-1, 0, -1):
        if num >= 1000 ** i:
            prefix = num_to_words(num // 1000 ** i) + ' ' + bigs[i]
            num %= 1000 ** i
            if write_commas and i >= 1 and num >= 100:
                prefix += ','
            words += ('' if words == '' else ' ') + prefix

    if num > 0:
        if words: words += ' '
        if num < 100 and num % 10 != 0:
            words += ('and ' if write_and else '')
        words += num_to_words(num)

    return words

def with_separator(number, separator):
    """
    Format a number with a separator every 3 digit from the right.
    123456789 -> 123,456,789 or 123 456 789

    Args:
        number (int): The number to convert.
        separator (str): The separator to use.

    Returns:
        str: The string with the separator every 3 digits from the end.
    """
    number = str(number)
    n = len(number)
    if n <= 3: return number
    else: return with_separator(number[:n-3], separator) + separator + number[n-3:]

class Stroke(str):
    """ A Stroke object is just a string with a few extra methods. """

    def sanitized(self):
        """ Remove the dash or asterisk from the stroke. """
        return self.replace("-", "").replace("*", "")

    def is_plumber(self) -> bool:
        """ Check if the stroke is a valid plumber. """
        if self in unique:
            return True
        for ender in big_enders:
            if self == linker + ender: return True
        for starter in starters:
            for ender in big_enders:
                if self == starter + ender: return True
            for ender in enders:
                if self == starter + ender: return True
        return False

    def to_num(self) -> int:
        """ Convert the stroke to a number. """
        if self in unique:
            return unique[self]
        for starter in starters:
            for ender in big_enders:
                if self == starter + ender:
                    return starters[starter] * big_enders[ender]
            for ender in enders:
                if self == starter + ender:
                    return starters[starter] * 10 + enders[ender]

class Outline(list):
    """ An Outline object is a list (not a tuple) of Stroke objects. """

    def __init__(self, outline):
        outline_list = []
        for stroke in outline:
            outline_list.append(Stroke(stroke))
        super().__init__(outline_list)

    def __str__(self):
        return "/".join(self)

    def is_plumber(self) -> bool:
        """ Checks that every stroke in the outline is a valid plumber """
        for stroke in self:
            if not stroke.is_plumber():
                return False
        return True

    def sanitized(self):
        """ Returns a version of the outline that doesn't contain any separator stroke and removes stars and dashes from every stroke. """
        outline = []
        for stroke in self:
            if stroke in separators: continue
            outline.append(stroke.replace("*", "").replace("-", ""))
        if len(outline) == 0: raise KeyError
        return Outline(outline)

    def to_num(self):
        """ Convert the whole outline to a number. """

        num = 0
        max_allowed_oom = 13
        last_big_oom = 13
        last_under_thou = 0

        for stroke in self:

            # Linker
            if stroke.startswith(linker):
                if last_under_thou == 0: raise KeyError
                valid_multiplicator = False

                for big_ender in big_enders:
                    if not stroke == linker + big_ender: continue
                    valid_multiplicator = True
                    multiplicator = big_enders[big_ender]

                    # Special case: multiplicator is DZ (100)
                    # Can be used with 3 -> 300 and 19 -> 1900 but not 200 -> 20000
                    if multiplicator == 100:
                        if not last_under_thou < 100: raise KeyError

                    if oom(last_under_thou * multiplicator) > last_big_oom:
                        print(f"{last_under_thou} * {multiplicator} > {last_big_oom}")
                        raise KeyError
                    num = num - last_under_thou + multiplicator * last_under_thou
                    last_big_oom = oom(multiplicator)
                    max_allowed_oom = oom(multiplicator) - 1
                    last_under_thou = 0
                    break

            # Not linker
            else:
                if oom(stroke.to_num()) > max_allowed_oom: raise KeyError
                num += stroke.to_num()
                if last_under_thou + stroke.to_num() < 1000: last_under_thou += stroke.to_num()
                max_allowed_oom = str(stroke.to_num()).count('0')

        return num

LONGEST_KEY = 20
def lookup(outline):

    assert len(outline) <= LONGEST_KEY
    outline = Outline(outline)

    # Can't start a number with a multiplicator stroke
    if outline[0].sanitized().startswith(linker): raise KeyError
    
    # Cancel everything if the whole outline isn't a valid plumber
    if not outline.sanitized().is_plumber(): raise KeyError

    zero = False
    for i in starters:
        if starters[i] == 0:
            zero_starter = i
            break
    if outline[0].startswith(zero_starter):
        zero = True

    num = outline.sanitized().to_num()

    # If there's an odd number if separator strokes in the outline
    # Meaning we can toggle formatting with a separator by hitting the separator stroke at any time.
    for separator in separators:
        if outline.count(separator) % 2 != 0:
            return with_separator(num, separators[separator])

    # Same thing with asterisks to wordify a number
    if str(outline).count("*") % 2 != 0:
        return ("zero " if zero else "") + num_to_words(num)

    # No separator stroke, no asterisk -> Just a number
    return "{#}" + ("0" if zero else '') + str(num)
