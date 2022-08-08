from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


"""Code taken from 
https://github.com/google/or-tools/blob/stable/ortools/constraint_solver/samples/tsp.py

"""

# [START data_model]
class TSPORSolver:

    def __init__(self,nodeDict,edges):
        self.nodeDict =  nodeDict
        self.edges = edges

    def create_data_model(self):
        """Stores the data for the problem."""
        data = {}
        # Locations in block units
        data['locations'] = [x for x in self.nodeDict.keys()]
        self.locations = data['locations']
        data['num_vehicles'] = 1
        data['depot'] = 0
        return data


    def create_distance_callback(self,data, manager):
        """Creates callback to return distance between points."""
        distances_ = {}
        index_manager_ = manager
        # precompute distance between location to have distance callback in O(1)
        for from_counter, from_node in enumerate(data['locations']):
            distances_[from_counter] = {}
            for to_counter, to_node in enumerate(data['locations']):
                if from_counter == to_counter:
                    distances_[from_counter][to_counter] = 0
                else:
                    distances_[from_counter][to_counter] = self.nodeDict.get(from_node) + self.edges.get((to_node[0],from_node[1]))
                    

        def distance_callback(from_index, to_index):

            from_node = index_manager_.IndexToNode(from_index)
            to_node = index_manager_.IndexToNode(to_index)
            return distances_[from_node][to_node]

        return distance_callback
        # [END distance_callback]


    # [START solution_printer]
    def print_solution(self,manager, routing, assignment):
        """Prints assignment on console."""
        print('Objective: {}'.format(assignment.ObjectiveValue()))
        index = routing.Start(0)
        plan_output = 'Route for vehicle 0:\n'
        route_distance = 0
        route_array = [] 
        while not routing.IsEnd(index):
            
            s = self.locations[index][0] # supply node
            d = self.locations[index][1] # demand node 
            route_array.append(s)
            route_array.append(d)
            plan_output += ' {} ->'.format(s)
            plan_output += '{} ->'.format(d)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))

           # print(self.locations[previous_index][0],self.locations[previous_index][1])
         
            previous_arc_dist = routing.GetArcCostForVehicle(previous_index, index, 0)
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
     
        route_distance -= previous_arc_dist + self.edges.get((self.locations[previous_index][0],self.locations[previous_index][1]))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        
        return route_distance,route_array
       
        
        # [END solution_printer]


    def solve(self):
        """Entry point of the program."""
        # Instantiate the data problem.
        # [START data]
        data = self.create_data_model()
        # [END data]

        # Create the routing index manager.
        # [START index_manager]
        manager = pywrapcp.RoutingIndexManager(len(data['locations']),
                                            data['num_vehicles'], data['depot'])
        # [END index_manager]

        # Create Routing Model.
        # [START routing_model]
        routing = pywrapcp.RoutingModel(manager)
        # [END routing_model]

        # Create and register a transit callback.
        # [START transit_callback]
        distance_callback = self.create_distance_callback(data, manager)
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        # [END transit_callback]

        # Define cost of each arc.
        # [START arc_cost]
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        # [END arc_cost]

        # Setting first solution heuristic.
        # [START parameters]
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        # [END parameters]

        # Solve the problem.
        # [START solve]
        assignment = routing.SolveWithParameters(search_parameters)
        # [END solve]

        # Print solution on console.
        # [START print_solution]
        if assignment:
           return self.print_solution(manager, routing, assignment)
        # [END print_solution]

    # [END program]