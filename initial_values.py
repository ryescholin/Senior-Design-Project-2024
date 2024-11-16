from pico_control import Pico
from transmission_lines import TransmissionLine
from grid import Grid
from route import Route

def setup_initial_values():
    # Create Pico objects
    picos = {
        "11": Pico("11"), 
        "12": Pico("12"), 
        "13": Pico("13"), 
        "1_end": Pico("1_end", closed=False),
    }

    # Create TransmissionLine objects with actual Pico objects as left and right breakers
    transmission_lines = {
        "11-12": TransmissionLine(picos["11"], picos["12"], 400.0, 350.0),
        "12-13": TransmissionLine(picos["12"], picos["13"], 350.0, 300.0),
        "13-1_end": TransmissionLine(picos["13"], picos["1_end"], 300.0, 250.0),
    }

    # Create grid
    grid = Grid()

    # Route 1: 11 -> 12 -> 13 -> 1_end
    route1 = Route("Route 1")
    route1.add_element(picos["11"])
    route1.add_element(transmission_lines["11-12"])
    route1.add_element(picos["12"])
    route1.add_element(transmission_lines["12-13"])
    route1.add_element(picos["13"])
    route1.add_element(transmission_lines["13-1_end"])
    route1.add_element(picos["1_end"])
    grid.add_route(route1)

    return grid
