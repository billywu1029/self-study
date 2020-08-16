class SimpleMapReduce:
    """Simple sequential map reduce framework."""
    def __init__(self, map_func, reduce_func):
        self.map_func = map_func
        self.reduce_func = reduce_func

    def process_inputs(self, infile):
        self.__call__(infile)

    def __call__(self, infile):
        """
        Using infile as input data, call the map function to map inputs to <k, v> pairs,
        shuffle the mapped values to be organized by key, and then call the reduce function
        to reduce the organized map outputs to produce <k2, v2> pairs. Return the result.
        """
        raise NotImplementedError

def file_to_words(filename: str) -> list:
    """Reads in a file, and returns a list of (word, count) pairs."""
    return []

def count_words(map_output: list) -> tuple:
    """Converts the shuffled map output organized by key to a single tuple of (word, sum_count)."""
    assert len(map_output) == 2 and isinstance(map_output[1], list)
    key, values = map_output
    return key, sum(values)


if __name__ == "__main__":
    mr = SimpleMapReduce(file_to_words, count_words)
    input_filename = "mapreduce.in"
    results = mr(input_filename)
    print(results)
