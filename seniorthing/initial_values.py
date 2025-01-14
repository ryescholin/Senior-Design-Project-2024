from pico_control import Pico
from route import Route
from grid import Grid

def setup_initial_values():
    # Create Pico objects with fault limits and connections
    breakers = {
        "11": Pico("11", fault_upper_limit=400),
        "12": Pico("12", fault_upper_limit=350),
        "13": Pico("13", fault_upper_limit=300),
        "1_end": Pico("1_end", fault_upper_limit=250, closed=False, connections={"Route 1": True, "Power": True}),
    }

    # Create a grid
    grid = Grid()

    # Define Route 1 with Pico objects
    route1 = Route(
        "Route 1",
        breakers=[breakers["11"], breakers["12"], breakers["13"], breakers["1_end"]],
        end_breaker=breakers["1_end"]
    )
    grid.add_route(route1)

    return grid, breakers
