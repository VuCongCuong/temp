class Material():
    def __init__(self, name='material'):
        self.name = name
    
    def assignElastic(self, density, E, u):
        self.density = density
        self.E = E
        self.u = u
    def assignHeatPre(self, Cp = 0, k=0.1):
        """"
        Parameters:
            Cp: Specific heat per unit mass
            k: heat conductivity for isotropic conductivity
        """
        self.Cp = Cp
        self.k = k
    
class JonhsonCook(Material):
    def __init__(self, name):
        super().__init__(name)
    
    def assignPlastic(self, A, B, C, n, m, Tr, Tm):
        self.A = A
        self.B = B
        self.C = C
        self.n = n
        self.m = m
        self.Tr = Tr
        self.Tm = Tm
    
    def assignFailure(self, D1, D2, D3, D4, D5, e0):
        self.D1 = D1
        self.D2 = D2
        self.D3 = D3
        self.D4 = D4
        self.D5 = D5
        self.e0 = e0

    def load_material(self, material):
        self.assignElastic(material['elastic']['density'], 
                           material['elastic']['youngs_modulus'], 
                           material['elastic']['poisson_ratio'])
        
        self.assignHeatPre(material['heat']['specific_heat'],
                           material['heat']['thermal_conductivity'])
        
        self.assignPlastic(material['plastic']['A'],
                           material['plastic']['B'],
                           material['plastic']['C'],
                           material['plastic']['n'],
                           material['plastic']['m'],
                           material['plastic']['Tr'],
                           material['plastic']['Tm'])
        
        self.assignFailure(material['failure']['D1'],
                           material['failure']['D2'],
                           material['failure']['D3'],
                           material['failure']['D4'],
                           material['failure']['D5'],
                           material['failure']['e0'])



    def load_material_tool(self, material):
        self.assignElastic(material['elastic']['density'], 
                           material['elastic']['youngs_modulus'], 
                           material['elastic']['poisson_ratio'])
        
        self.assignHeatPre(material['heat']['specific_heat'],
                           material['heat']['thermal_conductivity'])
       
        

