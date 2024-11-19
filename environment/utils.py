class LiquidityRange:
    def __init__(self, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        
    def width(self, relative=False):
        if relative:
            return self.upper_bound/self.lower_bound-1
        else:
            return self.upper_bound - self.lower_bound