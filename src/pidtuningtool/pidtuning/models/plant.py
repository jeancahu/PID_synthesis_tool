from pidtuning.rules import frac_order as _frac_order # Only rule it has by now

class FractionalOrderModel():
    def __init__(self,
                 alpha,                 # Fractional order   (alpha)
                 time_constant,         # Main time constant (T)
                 proportional_constant, # Gain               (K)
                 dead_time_constant):   # Dead time          (L)
        print("fractional order model for plant")

        try:
            self.alpha = float(alpha)
            self.T     = float(time_constant)
            self.K     = float(proportional_constant)
            self.L     = float(dead_time_constant)
        except Exception:
            raise ValueError("Plant model wrong input values")

        self.controllers = self.tuning_controllers()

    def tuning_controllers(self):
        controllers = []
        for ctype in _frac_order.valid_controllers:
            for Ms in _frac_order.valid_Ms:
                temp = _frac_order.tuning(self.alpha, self.T, self.K, self.L, Ms, ctype)
                if temp:
                    controllers.append(temp)
        return controllers

    def toDict(self):
        return {
            'alpha' : self.alpha,
            'T'     :     self.T,
            'K'     :     self.K,
            'L'     :     self.L
        }

    def __str__(self):
        return str(self.toDict())
