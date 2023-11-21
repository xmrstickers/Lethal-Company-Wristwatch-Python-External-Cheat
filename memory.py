class memory:
    """
    values work for: BUILD 12681469 (as of 11-20-2023)
    Contains hardcoded offsets and magic numbers necessary to access the memory of Lethal Company (Lethal Company.exe)
    """
    def __init__(self, game_base_address):
        self.game_base_address = game_base_address
        self.TIME_ADDRESS = 0x01C1A478  #stable UnityPlayer.dll entrypoint 
        self.TIME_OFFSETS = [0x430, 0x118, 0x10, 0x158, 0x40C] # in-game time pointer chain 
    def time_address(self):
        return self.game_base_address + self.TIME_ADDRESS
    def time_offsets(self):
        return self.TIME_OFFSETS
