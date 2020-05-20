"""
Huffman Encoding Procedure for data compression.
This mini-project aims to:
    1. Provide a Huffman Tree generic construction, for any input string (acc to char occurrence freq)
    2. Define encoding procedure via generic Huffman Tree
    3. Define decoding procedure given generic Huffman Tree

@author: Bill Wu
Date: May 19, 2020
"""

class HuffmanNode:
    def __init__(self, val, prob, left, right):
        self.val = val
        self.prob = prob
        self.left = left
        self.right = right

def construct_huffman_tree(s: str) -> HuffmanNode:
    if not s:
        raise RuntimeError("Must specify a non-zero length string as input.")
    elif len(s) == 1:
        return HuffmanNode(s, 1, None, None)
    probabilities = {}
    for i in s:
        probabilities[i] = probabilities.get(i, 0) + 1

    # Actually unnecessary for the construction, but we'll include it for now to see probabilities
    sum_probs = sum(probabilities.values())
    for c in probabilities:
        probabilities[c] /= sum_probs

    d = {i: HuffmanNode(i, probabilities[i], None, None) for i in probabilities.keys()}
    artificial_char_name = 0
    while len(d) > 1:
        artificial_char_name += 1
        # Extract 2 min propability chars, remove them, then add the new artificial node w sum of their probabilities
        m1, v1 = min(d.items(), key=lambda x: x[1].prob)
        del d[m1]
        m2, v2 = min(d.items(), key=lambda x: x[1].prob)
        del d[m2]
        d[artificial_char_name] = HuffmanNode(artificial_char_name, v1.prob + v2.prob, v1, v2)

    return d[artificial_char_name]


t = construct_huffman_tree('abcdefababc')
