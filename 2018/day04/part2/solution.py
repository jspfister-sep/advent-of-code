import re, sys
from datetime import datetime
from operator import attrgetter, itemgetter

class Entry:
    FORMAT = '%Y-%m-%d %H:%M'

    def __init__(self, timestamp_str, payload_str):
        self.timestamp = datetime.strptime(timestamp_str, self.FORMAT) 
        if payload_str.isdigit():
            self.guard_id = int(payload_str)
            self.action = None
        else:
            self.guard_id = None
            self.action = payload_str
            
    def __str__(self):
        return '{} {}'.format(self.timestamp.strftime(self.FORMAT), self.action if self.action else self.guard_id)
        
class SleepInterval:
    def __init__(self, sleep_time):
        self.start = sleep_time.minute
        self.end = 59
        
    def wake(self, wake_time):
        self.end = wake_time.minute - 1
        
    @property
    def duration(self):
        return self.end - self.start + 1
        
    def includes(self, minute):
        return self.start <= minute <= self.end
        
class SleepTime:
    def __init__(self):
        self.intervals = []
        
    def sleep(self, sleep_time):
        self.intervals.append(SleepInterval(sleep_time))
        
    def wake(self, wake_time):
        self.intervals[-1].wake(wake_time)
        
    @property
    def total(self):
        return sum(list(map(lambda x: x.duration, self.intervals)))
        
    def sleep_count_by_minute(self, minute):
        return len(list(filter(lambda x: x.includes(minute), self.intervals)))

def read_sorted_entries_from_file():
    entries = []

    with open(sys.argv[1], 'r') as file:
        for line in file:
            m = re.match('\[(.+)\].+?([0-9]+|wakes|falls)', line)
            entries.append(Entry(m.group(1), m.group(2)))

    return sorted(entries, key=attrgetter('timestamp'))

    
def create_guard_records(entries):
    guards = {}

    for e in entries:
        if e.guard_id:
            guard = guards.setdefault(e.guard_id, SleepTime())
        elif e.action == 'falls':
            guard.sleep(e.timestamp)
        else:
            guard.wake(e.timestamp)
            
    return guards
    
def find_best_guard_and_sleep_count_pair_for_each_minute(guards):
    best_guard_and_sleep_count_by_minute = []
    
    for m in range (0, 60):
        guard_that_sleeps_most_this_minute = max(guards.keys(), key=lambda id: guards[id].sleep_count_by_minute(m))
        sleep_count = guards[guard_that_sleeps_most_this_minute].sleep_count_by_minute(m)
        best_guard_and_sleep_count_by_minute.append((guard_that_sleeps_most_this_minute, sleep_count))
    
    return best_guard_and_sleep_count_by_minute
    
entries = read_sorted_entries_from_file()
guards = create_guard_records(entries)
best_guard_and_sleep_count_by_minute = find_best_guard_and_sleep_count_pair_for_each_minute(guards)

best_guard_and_sleep_count = max(best_guard_and_sleep_count_by_minute, key=itemgetter(1))

best_guard = best_guard_and_sleep_count[0]
best_minute = best_guard_and_sleep_count_by_minute.index(best_guard_and_sleep_count)
best_sleep_count = best_guard_and_sleep_count[1]

print('Guard {} sleeps more ({} times) on minute {} than any other guard/minute'.format(best_guard, best_sleep_count, best_minute))
print('{} x {} = {}'.format(best_guard, best_minute, best_guard * best_minute))