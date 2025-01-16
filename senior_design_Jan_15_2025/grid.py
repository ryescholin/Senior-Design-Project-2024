class Grid:
    #Combines all routes into a grid map.
    def __init__(self):
        self.routes = []

    def add_route(self, route):
        #Adds a route to the grid.
        self.routes.append(route)

    def get_routes(self):
        #Returns all routes in the grid.
        return self.routes