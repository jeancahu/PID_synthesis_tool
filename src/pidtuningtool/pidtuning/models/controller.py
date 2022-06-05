class Controller():
    def __init__(self, ctype, Ms, n_kp, n_ti, n_td, kp, ti, td):
        self.ctype = ctype
        self.Ms = Ms
        self.n_kp = n_kp
        self.n_ti = n_ti
        self.n_td = n_td
        self.kp = kp
        self.ti = ti
        self.td = td

        # raise Exception("Wrong value") #TODO
        # raise ValueError("Wrong value") #TODO

    # Print json format __str__ etc

    def toDict(self):
        return {
            'ctype' : self.ctype,
            'Ms'    : self.Ms,
            'n_kp'  : self.n_kp,
            'n_ti'  : self.n_ti,
            'n_td'  : self.n_td,
            'kp'    : self.kp,
            'ti'    : self.ti,
            'td'    : self.td
        }

    def __str__(self):
        return str(self.toDict())
