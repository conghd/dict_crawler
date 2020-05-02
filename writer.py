import io


class Writer:
    @classmethod
    def write(cls, filename, lines):
        return Writer().__write(filename, lines)

    @classmethod
    def append(cls, filename, lines):
        return Writer().__append(filename, lines)

    def __init__(self):
        pass

    def __write(self, filename, lines):
        file1 = io.open(filename, 'w', encoding='utf-8')
        for line in lines:
            print(line)
            file1.write("%s\n" % unicode(line))

        file1.close()

    def __append(self, filename, lines):
        file1 = io.open(filename, 'a', encoding='utf-8')
        for line in lines:
            file1.write("%s\n" % unicode(line))

        file1.close()
