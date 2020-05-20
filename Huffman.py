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

    def check_rep(self):
        """[DEBUG] Ensure that probabilities of each node = sum(probability of left and probability of right).
        TODO: May want to ensure that floating point comparisons don't throw assertion errors if probs don't match!"""
        def traverse_verify(node):
            # If the tree were to have a chainlike subtree, then the Huffman coding could be simplified by merging
            # the 2 nodes into 1 to reduce the overall entropy. Therefore, this would never be a valid Huffman Tree.
            assert (node.left is None and node.right is None) or (node.left is not None and node.right is not None)
            if node.left is None and node.right is None:
                assert 0 <= node.prob <= 1
                return node.prob
            else:
                right_prob = traverse_verify(node.right)
                left_prob = traverse_verify(node.left)
                assert node.prob == left_prob + right_prob
                return node.prob

        final_prob = traverse_verify(self)
        assert final_prob == 1

    def construct_encoding_table(self):
        """Uses DFS through the Huffman Tree to construct the encoding table for all characters at the leaves."""
        table = {}

        def dfs(node, curr_bits=None):
            if curr_bits is None:
                curr_bits = []
            if node.left is None and node.right is None:
                if not curr_bits:  # Account for edge case of single node tree
                    table[node.val] = '1'
                else:
                    table[node.val] = ''.join(curr_bits)
            else:
                dfs(node.left, curr_bits + ['1'])
                dfs(node.right, curr_bits + ['0'])

        dfs(self)
        return table


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


def encode_huffman(s: str, tree: HuffmanNode) -> str:
    """Given a string and a Huffman tree encoding, generate the Huffman encoding table,
    and return the bitstring for the encoding of the compressed string.
    Assumes that tree is valid for s, ie every char in s is included in tree."""
    encoding_table = tree.construct_encoding_table()
    return ''.join([encoding_table[i] for i in s])


def decode_huffman(c: str, tree: HuffmanNode) -> str:
    """Given an encoded string and a Huffman tree encoding, traverse the Huffman tree
    to obtain the original string. Assumes that ciphertext c has a valid mapping back
    to an original string given the structure of the Huffman tree."""
    # Traverse the tree, left for 1, right for a 0, until a leaf node/char is visited
    ind = 0
    s = []
    curr_node = tree
    while ind < len(c):
        if curr_node.left is None and curr_node.right is None:
            s.append(curr_node.val)
            curr_node = tree
        if c[ind] == '1':
            curr_node = curr_node.left
        else:
            curr_node = curr_node.right
        ind += 1
    return ''.join(s)


if __name__ == "__main__":
    s = 'abcdefababc'
    t = construct_huffman_tree(s)
    t.check_rep()
    c = encode_huffman(s, t)
    d = decode_huffman(c, t)
    print(c)
    print(d)

