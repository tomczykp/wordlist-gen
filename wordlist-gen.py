#!/bin/env python3
from typing import List
from itertools import permutations

output_filename = "wordlist.lst"
base_wordlist = ["foo", "bar", "baz"]
word_len_limit = 8
numbering_limit = 2023
substites = {
        'a': ['4', '@'],
        'e': ['3'],
        'i': ['1'],
        'T': ['7'],
        's': ['5'],
        'g': ['9'],
        'O': ['0'],
    }

def base() -> List[str]:
    result = []
    for group in permutations(base_wordlist):
        for i in range(len(group)):
            t = ''.join(x for x in group[i:])
            if len(t) <= word_len_limit and len(t) > 0:
                result.append(t)
    return result

def leeting(wordlist: List[str]) -> List[str]:
    def leetspeak(instr: str):
        if not instr:
            yield ""
        else:
            first = instr[:1]
            for sub_replace in leetspeak(instr[1:]):
                if first in substites:
                    for changed in substites[first]:
                        yield changed + sub_replace
                yield first + sub_replace
    result: List[str] = []    
    for word in wordlist:
        result.extend([x for x in leetspeak(word)])
    return result 
    
def numbering(wordlist: List[str]) -> List[str]:
    result: List[str] = []
    for word in wordlist:
        t: List[str] = []
        for number in range(numbering_limit):
            t.append(f"{word}{number:02d}")
            t.append(f"{word}{number:03d}")
            t.append(f"{word}{number:04d}")
            t.append(f"{word}{number}")
        result.extend(t)
    return result
    
def spongebobing(wordlist: List[str]) -> List[str]:
    def all_casings(instr: str):
        if not instr:
            yield ""
        else:
            first = instr[:1]
            for sub_casing in all_casings(instr[1:]):
                yield first.lower() + sub_casing
                yield first.upper() + sub_casing
    result: List[str] = []
    for word in wordlist:
        result.extend([x for x in all_casings(word)])
    return result 
        
    
def run():
    print("Generating wordlist.lst")
    wordlist: List[str] = base()
    print(f"Generated {len(wordlist)} permutations of keywords")
    wordlist = spongebobing(wordlist)
    print(f"Generated {len(wordlist)} mixed cases")
    wordlist = leeting(wordlist)
    print(f"Generated {len(wordlist)} words with letters substitutions")
    wordlist = numbering(wordlist)
    print(f"Generated {len(wordlist)} words with added numbers")
    outBuffer = "".join(f"{word}\n" for word in wordlist)
    print(f"Result length: {len(wordlist)}")
    with open(output_filename, 'w') as file:
        file.write(outBuffer)

if __name__ == "__main__":
    run()
    
