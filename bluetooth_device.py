class BluetoothDevice:
    def __init__ (self, name, state = True):
        self.name = name
        self.state = state # True means closed
        self.perm_open = False

    def get_state(self):
        return self.state
    
    def set_state_close(self):
        if self.perm_open:
            print(self.name, "is perm_open, can not close")
        else:
            self.state = True
    
    def set_state_open(self):
        self.state = False

    def set_perm_open(self):
        self.perm_open = True
        self.state = False