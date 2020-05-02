class Reader:
    @classmethod
    def read(cls, filename):
        return Reader().__read(filename)

    def __init__(self):
        pass

    def __read(self, filename):
        file1 = open(filename, 'r')
        lines = file1.readlines()
        words = []

        for line in lines:
            words.append(line.strip())

        return words
