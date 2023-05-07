#!/bin/env python3
from typing import List
from itertools import permutations

output_filename = "proto-wordlist.lst"
base_wordlist = ["name", "surname", "security", "itsec", "password", "haslo"]
delims = ["", ".", "-", "_", "+", "=", " ", "0"]
LIMIT = 15
numbering_limit = 10000
substitutes = {
        'a': ['4', '@'],
        'e': ['3'],
        'i': ['1'],
        'T': ['7'],
        's': ['5'],
        'g': ['9'],
        'O': ['0'],
    }

def check(t: str):
    return LIMIT == len(t) 
    
def checkClose(t: str):
    return LIMIT - 2 <= len(t) <= LIMIT + 2

def base(delim) -> List[str]:
    result = []
    for group in permutations(base_wordlist):
        for i in range(len(group)):
            t = f"{delim}".join(x for x in group[i:])
            if checkClose(t):
                result.append(t)
    return result


def leeting(wordlist: List[str]) -> List[str]:
    def leetspeak(instr: str):
        if not instr:
            yield ""
        else:
            first = instr[:1]
            for sub_replace in leetspeak(instr[1:]):
                if first in substitutes:
                    for changed in substitutes[first]:
                        yield changed + sub_replace
                yield first + sub_replace
    result: List[str] = []
    for word in wordlist:
        result.extend([x for x in leetspeak(word) if checkClose(x)])
    return result 


def numbering(wordlist: List[str]) -> List[str]:
    result: List[List[str]] = []
    numbering_limit_chars: int = len(str(numbering_limit))
    for word in wordlist:
        t: List[str] = []
        if check(word):
            t.append(word)
        for number in range(numbering_limit):
            for i in range(numbering_limit_chars - len(str(number)) + 1):
                w: str = f"{word}{'0'*i}{number}"
                if check(w):
                    t.append(w)
        result.append(t)
    return [i for sub in result for i in sub]


def spongebobing(wordlist: List[str]) -> List[str]:
    def all_casings(instr: str):
        if not instr:
            yield ""
        else:
            first = instr[:1]
            for sub_casing in all_casings(instr[1:]):
                if first.isalpha():
                    yield first.lower() + sub_casing
                    yield first.upper() + sub_casing
                else:
                    yield first + sub_casing
    result: List[str] = []
    for word in wordlist:
        result.extend([x for x in all_casings(word) if checkClose(x)])
    return result
        
    
def run():
    for delim in delims:
        print(f"Generating {output_filename} for `{delim}`")
        wordlist: List[str] = base(delim)
        print(f"Generated {len(wordlist)} permutations of keywords")
        wordlist = spongebobing(wordlist)
        print(f"Generated {len(wordlist)} mixed cases")
        wordlist = leeting(wordlist)
        print(f"Generated {len(wordlist)} words with letters substitutions")
        wordlist = numbering(wordlist)
        print(f"Generated {len(wordlist)} words with added numbers")
        writeFile(wordlist)

def writeFile(wordlist: List[str]) -> None:
    outBuffer: str = "".join(f"{word}\n" for word in wordlist)
    with open(output_filename, 'a') as file:
        file.write(outBuffer)
        

if __name__ == "__main__":
    run()
