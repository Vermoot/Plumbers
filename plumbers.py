from pprint import pprint
LONGEST_KEY = 1

class Number():
    pass

unique = {
    "WAOPB":     "1",
    "TWO":       "2",
    "THRAOE":    "3",
    "TPOUR":     "4",
    "TPAOEUF":   "5",
    "SEUBGS":    "6",
    "SEFPB":     "7",
    "AET":       "8",
    "TPHAOEUPB": "9",
    "TEPB":      "10",
    "HREFPB":    "11",
    "TWEFL":     "12",
    "STHR-FPB":  "13",
    "STPR-FPB":  "14",
    "STPW-FPB":  "15",
    "SKH-FPB":   "16",
    "STPHR-FPB": "17",
    "STWH-FPB":  "18",
    "SKPR-FPB":  "19",
}

starters = {
    "KWH":    "{^}",
    "SKPH":   "0",
    "WU":     "1",
    "STWH":   "8",
    "STW":    "2",
    "STHR":   "3",
    "STPR":   "4",
    "STPW":   "5",
    "SKH":    "6",
    "STPHR":  "7",
    "SKPR":   "9",
}

enders = {
    "-T":     "0",
    "AOEUPB": "9",
    "UPB":    "1",
    "AO":     "2",
    "AOE":    "3",
    "OUR":    "4",
    "AOEUF":  "5",
    "EUBGS":  "6",
    "EFPB":   "7",
    "AET":    "8",
    "DZ":     "00",
    "PBD":    "000",
}

# Written-out numbers {{{
#  starters = {
    #  #  "SRAO":   "",
    #  "STWH":   "eighty",
    #  "STW":    "twenty",
    #  "STHR":   "thirty",
    #  "STPR":   "forty",
    #  "STPW":   "fifty",
    #  "SKH":    "sixty",
    #  "STPHR":  "seventy",
    #  "SKPR":   "ninety",
#  }

#  enders = {
    #  "-T":     "&",
    #  "AOEUPB": "nine&",
    #  "UPB":    "one&",
    #  "AO":     "two&",
    #  "AOE":    "three&",
    #  "OUR":    "four&",
    #  "AOEUF":  "five&",
    #  "EUBGS":  "six&",
    #  "EFPB":   "seven&",
    #  "AET":    "eight&",
#  }
# }}}

def lookup(outline):
  assert len(outline) <= LONGEST_KEY

  stroke = outline[0]

  for i in unique:
      if stroke == i: return unique[stroke]

  for starter_chord, starter in starters.items():
      if stroke.startswith(starter_chord):
          print("Starter matched with %s" % (starter_chord))
          for ender_chord, ender in enders.items():
              if stroke == starter_chord + ender_chord or stroke == starter_chord + "-" + ender_chord:
                  return "".join([starter, ender]) + "{}"
  raise KeyError
