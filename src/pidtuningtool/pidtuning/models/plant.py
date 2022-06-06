from ..rules import frac_order as _frac_order # Only rule it has by now

class FractionalOrderModel():
    def __init__(self,
                 alpha=0,                 # Fractional order   (alpha)
                 time_constant=0,         # Main time constant (T)
                 proportional_constant=0, # Gain               (K)
                 dead_time_constant=0,    # Dead time          (L)

                 time_vector=[], # Time vetor to identify the plant model
                 step_vector=[], # Step vector to identify the plant model
                 resp_vector=[]  # Open-loop system response to identify the plant model
                 ):

        print("Create a fractional order model for the plant")

        if not (alpha or time_constant or proportional_constant or dead_time_constant):
            pass

        try:
            self.alpha = float(alpha)
            self.T     = float(time_constant)
            self.K     = float(proportional_constant)
            self.L     = float(dead_time_constant)
        except Exception:
            raise ValueError("Plant model wrong input values")

        self.controllers = self.tune_controllers()

    def tune_controllers(self):
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
