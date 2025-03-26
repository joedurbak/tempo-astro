import pandas as pd

class Grid:
    def __init__(self):
        self.grid = None
        self.minimum_ra_offset = None
        self.maximum_ra_offset = None
        self.minimum_dec_offset = None
        self.maximum_dec_offset = None
        self.load_grid()

    def load_grid(self):
        self.grid = pd.DataFrame()
