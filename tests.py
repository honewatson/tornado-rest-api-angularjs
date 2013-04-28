
class b(object):
    def __init__(self, x):
        self.x = x
    def go(self):
        print "b go %s" % self.x

class a(object):
    def __init__(self, b):
        self.b = b
    def get(self):
        print "get"
    def put(self):
        print "put"


class c(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def do(self):
        return self.a(self.b('hello'))


z = {"a":a}
z['a'](b('hello'))

d = c(a, b)

d.do()