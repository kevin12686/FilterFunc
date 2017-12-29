class Date(object):
    year = None
    month = None

    def __init__(self, year, month):
        self.year = year
        self.month = month

    def __eq__(self, other):
        if isinstance(self, other.__class__) and self.year == other.year and self.month == other.month:
            return True
        else:
            return False

    def __hash__(self):
        return self.year * 10 + self.month

    def __repr__(self):
        return self.year + '-' + self.month

    def next_month(self):
        if self.month + 1 > 12:
            return Date(year=self.year + 1, month=1)
        else:
            return Date(year=self.year, month=self.month + 1)


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

    def to_dict_without_month(self):
        return {'ip': self.ip, 'ttp': self.ttp}


def dictlist_to_eventlist(dictlist):
    result = list()
    for each in dictlist:
        result.append(Event(each['ip'], each['ttp'], each['month']))
    return result


def generate_empty_collection():
    empty_collection = dict()
    for each in range(1, 13):
        empty_collection[str(each)] = set()
    return empty_collection


def collect_event(event_list):
    collect = generate_empty_collection()
    for each in event_list:
        collect[each.month] = collect[each.month] | {each}
    return collect


def set_to_list(input_set):
    result = list()
    for each in input_set:
        result.append(each.to_dict_without_month())
    return result


def filter_month(collection_data, continuous):
    result = set()
    if continuous == 1:
        for each in range(0, 12):
            result |= collection_data[str(each + 1)]
    elif continuous == 2:
        for each in range(0, 12):
            fir_month = each + 1
            sec_month = (each + 1) % 12 + 1
            temp = collection_data[str(fir_month)] & collection_data[str(sec_month)]
            result |= temp
    else:
        for each in range(0, 12):
            fir_month = each + 1
            sec_month = (each + 1) % 12 + 1
            temp = collection_data[str(fir_month)] & collection_data[str(sec_month)]
            for i in range(2, continuous):
                n = (each + i) % 12 + 1
                temp &= collection_data[str(n)]
            result |= temp
    return result


def continuous_filter(dictlist, continuous):
    data_list = dictlist_to_eventlist(dictlist)
    collection = collect_event(data_list)
    result_set = filter_month(collection, continuous)
    result_list = set_to_list(result_set)
    return result_list


if __name__ == '__main__':
    a = {'ip': '127.0.0.1', 'ttp': '1', 'month': '1'}
    b = {'ip': '127.0.0.1', 'ttp': '1', 'month': '2'}
    c = {'ip': '127.0.0.1', 'ttp': '1', 'month': '11'}
    d = {'ip': '127.0.0.1', 'ttp': '1', 'month': '12'}
    data = [a, b, c, d]
    print(continuous_filter(data, 4))
