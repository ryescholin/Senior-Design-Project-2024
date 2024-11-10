class Pico:
    def __init__(self, pico_name, closed=True):
        self.name = pico_name
        self.is_closed = closed
        self.openable = True

    def open(self):
        if self.openable:
            self.is_closed = False

    def perm_open(self):
        self.is_closed = False
        self.openable = False

    def close(self):
        if self.openable:
            self.is_closed = True
            print(self.name, "closed")

    def reset_dynamic(self):
        self.openable = True

    def is_breaker_closed(self):
        return self.is_closed

    def get_breaker_name(self):
        return self.name

    def breaker_status(self):
        status = "Closed" if self.is_closed else "Open"
        print(f"{self.name} - Breaker: {status}")
