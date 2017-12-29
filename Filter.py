class Event(object):
    ip = None
    ttp = None
    month = None

    def __init__(self, ip, ttp, month):
        self.ip = ip
        self.ttp = ttp
        self.month = month

    def __eq__(self, other):
        if isinstance(self, other.__class__) and self.ip is other.ip and self.ttp is other.ttp:
            return True
        else:
            return False

    def __hash__(self):
        return self.ip.__hash__() + self.ttp.__hash__()

    def __repr__(self):
        return '< Event IP: ' + self.ip + '  TTP: ' + self.ttp + '  Month: ' + self.month + '>'


if __name__ == '__main__':
    a = Event('127.0.0.1', '1', '1')
    b = Event('127.0.0.1', '2', '1')
    A = {a}
    B = {b}
    print(A | B)
