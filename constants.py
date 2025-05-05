# Author: Vu Hoai Lam
# Date: 2025/03/23
# Description: This file contains the constants used in the simulation.

# first is the properties of the material used in the simulation.
# the system used in this simulation is the mirco meter system.

# lenght is in [micro meter], time is in [second], temperature is in [kelvin].
# density is in [10^18 kg/m^3], youngs_modulus is in [MPa], poisson_ratio is in [percentage].
# thermal_conductivity is in [10^-6 W/m*K], thermal_capacity is in [10^-12 jun/kg*K].
# stress is in [MPa], strain is in [percentage].

# e-6 meter, kilogram, kevin, s,  

materials = {
    "aluminium": {
        "type": "jonhson_cook",
        "elastic": {
            "density":2.7e-15,
            "youngs_modulus":70e3,
            "poisson_ratio": 0.33 
        },
        "heat": {
            "heat_capacity": 910e12,
            "thermal_conductivity": 6.6e6,
            "thermal_expansion": 0.0000023,
            "specific_heat": 910e12
        },
        "plastic": {
            "A": 324.1,
            "B": 113.8,
            "C": 0.002,
            "n": 0.42,
            "m": 1.34,
            "Tr": 298,
            "Tm": 1500
        },
        "failure": {
            "D1": -0.77,
            "D2": 1.45,
            "D3": -0.47,
            "D4": 0,
            "D5": -1.6,
            "e0": 1
        }
    },
    "cBN": {
        "elastic": {
            "density":3.25e-15,
            "youngs_modulus":909e3,
            "poisson_ratio": 0.12 
        },
        "heat": {
            "thermal_conductivity": 240e6,
            "thermal_expansion": 0.0000047,
            "specific_heat": 670e12
        },
        "plastic": {
            
        },
        "failure": {
            
        }
    },
    "Ti64": {
        "type": "jonhson_cook",
        "elastic": {
            "density":4.5e-15,
            "youngs_modulus":144e3,
            "poisson_ratio": 0.32 
        },
        "heat": {
            "heat_capacity": 910e12,
            "thermal_conductivity": 6.6e6,
            "specific_heat": 656e12
        },
        "plastic": {
            "A": 870,
            "B": 990,
            "C": 0.011,
            "n": 0.25,
            "m": 1,
            "Tr": 298,
            "Tm": 1833
        },
        "failure": {
            "D1": -0.09,
            "D2": 0.25,
            "D3": 0.5,
            "D4": 0.014,
            "D5": 3.87,
            "e0": 0.7
        }
    },
    "steel": {
        "type": "jonhson_cook",
        "elastic": { 
            "density": 4.5e-15,
            "youngs_modulus": 210e3,
            "poisson_ratio": 0.3
        },
        "heat": {
            "heat_capacity": 0.486e12,
            "thermal_conductivity": 46.6e6,
            "thermal_expansion": 0.121,
            "specific_heat": 0.486
        },
        "plastic": {
            "A": 553,
            "B": 600,
            "C": 0.0134,
            "n": 0.234,
            "m": 1,
            "Tr": 298,
            "Tm": 1763
        },
        "failure": {
            "D1": 0.06,
            "D2": 3.31,
            "D3": -1.96,
            "D4": 0.0018,
            "D5": 0.58,
            "e0": 1
        }
    }
}

tool_shapes = ["cylinder", "sphere"]
tool_mode = ["single", "multi"]
grain_distributions = ["random", "normal", "uniform"]
