import re
import string

class SimpleMapReduce:
    """Simple sequential map reduce framework."""
    def __init__(self, map_func, reduce_func):
        self.map_func = map_func
        self.reduce_func = reduce_func

    def shuffle(self, map_outputs):
        """Organize and return map outputs by key: list of (k, list<v>) pairs."""
        shuffled = {}
        for k, v in map_outputs:
            if k not in shuffled:
                shuffled[k] = [v]
            else:
                shuffled[k].append(v)
        return shuffled.items()

    def process_inputs(self, infile):
        self.__call__(infile)

    def __call__(self, infile):
        """
        Using infile as input data, call the map function to map inputs to <k, v> pairs,
        shuffle the mapped values to be organized by key, and then call the reduce function
        to reduce the organized map outputs to produce <k2, v2> pairs. Return the result.
        """
        map_outputs = self.map_func(infile)
        shuffled = self.shuffle(map_outputs)
        reduce_outputs = []
        for item in shuffled:
            reduce_outputs.append(self.reduce_func(item))
        return reduce_outputs

def file_to_words(filename: str) -> list:
    """Reads in a file, and returns a list of (word, count) pairs."""
    result = []
    with open(filename, "r") as f:
        for line in f.readlines():
            words = line.split()
            for word in words:
                # this line is a mindfuck, thank god for python
                word_no_punc = re.sub(rf'[{string.punctuation}]', '', word)
                result.append((word_no_punc, 1))
    return result

def count_words(map_output: list) -> tuple:
    """Converts the shuffled map output organized by key to a single tuple of (word, sum_count)."""
    assert len(map_output) == 2 and isinstance(map_output[1], list)
    key, values = map_output
    return key, sum(values)


if __name__ == "__main__":
    # Testing file_to_words and count_words:
    input_filename = "mapreduce.in"
    # results = file_to_words(input_filename)
    # print(results)
    # counts = {}
    # for word, c in results:
    #     if word not in counts:
    #         counts[word] = [c]
    #     else:
    #         counts[word].append(c)
    #
    # reduce_results = []
    # for word in counts:
    #     reduce_results.append(count_words([word, counts[word]]))
    # reduce_results.sort(key=lambda x: x[1], reverse=True)
    # print(reduce_results)

    mr = SimpleMapReduce(file_to_words, count_words)
    results = mr(input_filename)
    results.sort(key=lambda x: x[1], reverse=True)
    print(results)
