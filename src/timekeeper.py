import datetime as dt 



class TimeKeeper:
    def __init__(self, interval_length=1):
        self.time_initial = dt.datetime.now()
        self.interval_start = self.time_initial
        self.step_counter = 0
        self.interval_length = interval_length

    def inc_frame(self):
        self.step_counter += 1

    def time_now(self):
        return dt.datetime.now()

    def has_interval_passed(self):
        return (dt.datetime.now() - self.interval_start).total_seconds() >= self.interval_length

    def begin_new_interval(self):
        self.interval_start = dt.datetime.now()
        self.step_counter += 1

    def time_delta(self, since=None):
        if not since:
            return dt.now() - self.time_initial
        return dt.now() - since