class Grid:
    """
    Represents the entire power grid and manages its routes.
    """

    def __init__(self):
        """Constructor for Grid."""
        self.routes = []

    def add_route(self, route):
        """
        Adds a route to the grid.

        Parameters:
        route (Route): Route object to add.
        """
        self.routes.append(route)
