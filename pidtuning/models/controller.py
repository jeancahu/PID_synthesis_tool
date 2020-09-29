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

        raise Exception("Wrong value") #TODO

    # Print json format __str__ etc
