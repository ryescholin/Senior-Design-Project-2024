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
        "21": Pico("21"), 
        "22": Pico("22"), 
        "23": Pico("23"), 
        "1_end_2": Pico("1_end_2", closed=False),
    }

    # Create TransmissionLine objects with actual Pico objects as left and right breakers
    transmission_lines = {
        "11-12": TransmissionLine(picos["11"], picos["12"], 1000.0, 770.0),
        "12-13": TransmissionLine(picos["12"], picos["13"], 770.0, 620.0),
        "13-1_end_2": TransmissionLine(picos["13"], picos["1_end_2"], 620.0, 400.0),
        "21-22": TransmissionLine(picos["21"], picos["22"], 1000.0, 770.0),
        "22-23": TransmissionLine(picos["22"], picos["23"], 770.0, 620.0),
        "23-1_end_2": TransmissionLine(picos["23"], picos["1_end_2"], 620.0, 400.0),
    }

    # Create grid
    grid = Grid()

    # Route 1: 11 -> 12 -> 13 -> 1_end_2
    route1 = Route("Route 1")
    route1.add_element(picos["11"])
    route1.add_element(transmission_lines["11-12"])
    route1.add_element(picos["12"])
    route1.add_element(transmission_lines["12-13"])
    route1.add_element(picos["13"])
    route1.add_element(transmission_lines["13-1_end_2"])
    route1.add_element(picos["1_end_2"])
    grid.add_route(route1)

    # Route 2: 21 -> 22 -> 23 -> 1_end_2
    route2 = Route("Route 2")
    route2.add_element(picos["21"])
    route2.add_element(transmission_lines["21-22"])
    route2.add_element(picos["22"])
    route2.add_element(transmission_lines["22-23"])
    route2.add_element(picos["23"])
    route2.add_element(transmission_lines["23-1_end_2"])
    route2.add_element(picos["1_end_2"])
    grid.add_route(route2)

    return grid
