#!/usr/bin/env python
#

from parse import compile


def main():
    guard_logs = open("day4input.txt", "r")

    guard_records = {}

    for guard_record in process_logs(guard_logs.readlines()):
        if (guard_record.guard_id not in guard_records):
            guard_records[guard_record.guard_id] = []
        guard_records[guard_record.guard_id].append(guard_record)

    most_sleep = 0
    most_sleep_id = None
    for guard_id in guard_records.keys():
        guard_sleep = reduce(
            lambda x, y: x+y, map(lambda x: x.get_sleep_count(), guard_records[guard_id]))
        if (guard_sleep > most_sleep):
            most_sleep = guard_sleep
            most_sleep_id = guard_id

    if (most_sleep_id is not None):
        print "sleep_id ", most_sleep_id, ", ", most_sleep
        # print('\n'.join(map(str, guard_records[most_sleep_id])))
        print(find_likely_sleep_minute(guard_records[most_sleep_id]))

    likely = find_likely_sleep_minute_all(guard_records)
    print likely
    print likely[0] * likely[1]

    return None


def process_logs(lines):
    p = compile("[{date:ti}] {event}")
    g = compile("Guard #{guard_id:d} begins shift")
    lines.sort()
    current_guard = None
    guard_records = []

    for line in lines:
        print line
        data = p.parse(line)
        if (data is not None):
            event_str = data['event']
            event_date = data['date']
            if (event_str.endswith("begins shift")):
                # If this is a guard event, make a new guard record
                if (current_guard is not None):
                    current_guard.end_shift()

                guard_data = g.parse(event_str)
                current_guard = GuardRecord(guard_data['guard_id'], event_date)
                guard_records.append(current_guard)

            if (event_str.startswith("wakes up")):
                current_guard.wakeup(event_date.minute)

            if (event_str.startswith("falls asleep")):
                current_guard.go_to_sleep(event_date.minute)

    return guard_records


def find_likely_sleep_minute(individual_guard_records):
    minute_count = get_guard_minute_counts(individual_guard_records)

    max_count = 0
    max_index = -1
    for i in range(60):
        if (minute_count[i] > max_count):
            max_index = i
            max_count = minute_count[i]
    print minute_count
    print "Max count {0}, index {1}".format(max_count, max_index)
    return max_index


def get_guard_minute_counts(individual_guard_records):
    minute_count = [0 for _ in range(60)]
    for i in range(60):
        for guard_record in individual_guard_records:
            if (guard_record.is_sleep(i)):
                minute_count[i] += 1
    return minute_count


def find_likely_sleep_minute_all(guard_records):
    winningest_guard_id = [0 for _ in range(60)]
    max_minute_counts = [0 for _ in range(60)]
    guard_minute_counts = dict((k, get_guard_minute_counts(v))
                               for k, v in guard_records.iteritems())
    # print guard_minute_counts
    for i in range(60):
        for guard_id in guard_minute_counts:
            if (guard_minute_counts[guard_id][i] > max_minute_counts[i]):
                max_minute_counts[i] = guard_minute_counts[guard_id][i]
                winningest_guard_id[i] = guard_id

    # now, loop through for the max minute_count
    max_minute = 0
    max_index = -1
    for i in range(60):
        if (max_minute_counts[i] > max_minute):
            max_index = i
            max_minute = max_minute_counts[i]

    return winningest_guard_id[max_index], max_index


class GuardRecord:
    def __init__(self, guard_id, date):
        self.guard_id = guard_id
        self.date = date
        self.sleep = [0 for _ in range(60)]
        self.last_sleep = -1

    def wakeup(self, minute):
        if (self.last_sleep > 0):
            for minute in range(self.last_sleep, minute):
                self.sleep[minute] = 1
        self.last_sleep = -1

    def go_to_sleep(self, minute):
        self.last_sleep = minute
        self.sleep[minute] = 1

    def end_shift(self):
        if (self.last_sleep > 0):
            self.wakeup(60)

    def get_sleep_count(self):
        return self.sleep.count(1)

    def is_sleep(self, minute):
        return self.sleep[minute] == 1

    def __str__(self):
        return "{0} {1} {2}".format(self.guard_id, self.date, self.sleep)


if __name__ == "__main__":
    print main()
