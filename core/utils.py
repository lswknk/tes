import sys
import datetime as dt


def print_4s(value, end=None):
    print(' ' * 4, end='')
    try:
        print(value, end=end)
    except SyntaxError:
        return


def print_8s(value, end=None):
    print(' ' * 8, end='')
    try:
        print(value, end=end)
    except SyntaxError:
        return


# define switch class
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


class Timer(object):

    def __init__(self):
        self.start_dt = None

    def start(self):
        self.start_dt = dt.datetime.now()

    def stop(self):
        end_dt = dt.datetime.now()
        print('Time taken: %s' % (end_dt - self.start_dt))


class File(object):

    def __init__(self, path, fileName="model.py"):
        self.name = fileName
        self.path = path

    def open(self):
        output = sys.stdout
        fileName = open(self.path + '/model.py', 'w', encoding='utf8')
        #print('File %s opend!' % fileName)
        sys.stdout = fileName
        return fileName, output

    def close(self, fileName, output):
        fileName.close()
        sys.stdout = output
        #print('File %s closed!' % fileName)
        return True
