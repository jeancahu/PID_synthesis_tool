class FractionalOrderModel():
    def __init__(self,
                 alpha,                 # Fractional order   (alpha)
                 time_constant,         # Main time constant (T)
                 proportional_constant, # Gain               (K)
                 dead_time_constant):   # Dead time          (L)
        print("fractional order model for plant")

        self.alpha = alpha
        self.T = time_constant
        self.K = proportional_constant
        self.L = dead_time_constant

