import datetime


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
        return self.year * 100 + self.month

    def __repr__(self):
        return str(self.year) + '-' + str(self.month)

    def next_month(self):
        if self.month + 1 > 12:
            return Date(year=self.year + 1, month=1)
        else:
            return Date(year=self.year, month=self.month + 1)


class Event(object):
    ip = None
    ttp = None
    date = None

    def __init__(self, ip, ttp, date):
        self.ip = ip
        self.ttp = ttp
        self.date = date

    def __eq__(self, other):
        if isinstance(self, other.__class__) and self.ip is other.ip and self.ttp is other.ttp:
            return True
        else:
            return False

    def __hash__(self):
        return self.ip.__hash__() + self.ttp.__hash__()

    def __repr__(self):
        return '< Event IP: ' + self.ip + '  TTP: ' + self.ttp + '  DATE: ' + str(self.date) + '>'

    def to_dict_without_month(self):
        return {'ip': self.ip, 'ttp': self.ttp}


def dictlist_to_eventlist(dictlist):
    result = list()
    for each in dictlist:
        result.append(Event(each['ip'], each['ttp'], Date(each['year'], each['month'])))
    return result


def collect_event(event_list):
    collect = dict()
    for each in sorted(event_list, key=lambda event: event.date.__hash__()):
        try:
            collect[each.date] = collect[each.date] | {each}
        except KeyError:
            collect[each.date] = {each}
    return collect


def set_to_list(input_set):
    result = list()
    for each in input_set:
        result.append(each.to_dict_without_month())
    return result


def filter_month(collection_data, continuous):
    result = set()
    if continuous == 1:
        for each in collection_data.keys():
            result |= collection_data[each]
    elif continuous == 2:
        for each in collection_data.keys():
            fir_month = each
            sec_month = each.next_month()
            try:
                temp = collection_data[fir_month] & collection_data[sec_month]
                result |= temp
            except KeyError:
                break
    else:
        for each in collection_data.keys():
            fir_month = each
            last = sec_month = each.next_month()
            try:
                temp = collection_data[fir_month] & collection_data[sec_month]
                for i in range(2, continuous):
                    last = last.next_month()
                    temp &= collection_data[last]
                result |= temp
            except KeyError:
                break
    return result


def continuous_filter(dictlist, continuous):
    data_list = dictlist_to_eventlist(dictlist)
    collection = collect_event(data_list)
    result_set = filter_month(collection, continuous)
    result_list = set_to_list(result_set)
    return result_list


def get_datetime_year(dateTime):
    return dateTime.datetime.year


def get_datetime_month(dateTime):
    return dateTime.datetime.month


if __name__ == '__main__':
    a = {'ip': '127.0.0.1', 'ttp': '1', 'year': 2017, 'month': 12}
    b = {'ip': '127.0.0.1', 'ttp': '1', 'year': 2018, 'month': 1}
    c = {'ip': '127.0.0.1', 'ttp': '1', 'year': 2018, 'month': 2}
    d = {'ip': '127.0.0.1', 'ttp': '1', 'year': 2018, 'month': 3}
    e = {'ip': '127.0.0.1', 'ttp': '2', 'year': 2018, 'month': 4}
    data = [a, b, c, d, e]
    print(continuous_filter(data, 4))
