from parser import Parser

import json # we're gonna compare our 'Parser.loads' to 'json.loads'

NUM_EXAMPLES = 7 #  some of them are taken from ( jsonplaceholder.typicode.com )


def test():
    for i in range(NUM_EXAMPLES):
        with open(f"examples/json{i}.json") as f:
            data = f.read()
            result1 = Parser.loads(data)
            result2 = json.loads(data) # this is obviously faster, since it is implemented in C

        assert result1 == result2 # success! 

    print("Assertions Succeed!")


if __name__ == "__main__":
    test()

