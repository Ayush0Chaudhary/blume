# keep transit callback alive
transit_callback = []
transit_callback_index_arr = []
for vehicle_id in range(data['num_vehicles']):
    distance_matrix = data['distance_matrix'][vehicle_id]

    # Use default value to capture distance_matrix current value
    def distance_callback_vehicle(from_index, to_index, data=distance_matrix):
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(data[from_node][to_node])

    transit_callback.append(distance_callback_vehicle)
    transit_callback_index_arr.append(routing.RegisterTransitCallback(transit_callback[-1]))
                                     
for vehicle_id in range(data['num_vehicles']):
    routing.SetArcCostEvaluatorOfVehicle(transit_callback_index_arr[vehicle_id], vehicle_id)

# Add Distance constraint.
dimension_name = 'Distance'
routing.AddDimensionWithVehicleTransits(
    transit_callback_index_arr,  # list of transit callback, one per vehicle
    0,  # no slack
    300000,  # vehicle maximum travel distance
    True,  # start cumul to zero
    dimension_name)

distance_dimension = routing.GetDimensionOrDie(dimension_name)
# makes the global span the predominant factor in the objective function
# (minimizes the length of the longest route)
distance_dimension.SetGlobalSpanCostCoefficient(100)

# # Add Capacity constraint
demand_evaluator_index = routing.RegisterUnaryTransitCallback(create_demand_evaluator(data, manager))
add_capacity_constraints(manager,routing, data, demand_evaluator_index)



###############################################################################################################3
def create_data_model():
    """Stores the data for the problem for 130 nodes."""
    data = {}
    data['distance_matrix'] = [[0.0,41.6523,42.2404,16.53,13.9472,12.1087],
[41.628,0.0,1.4118,25.6223,28.5948,33.7074],
[44.6087,3.1841,0.0,28.6023,31.5747,36.6873],
[16.79190,25.9814,26.5694,0.0,3.7579,8.8705],
[14.395,29.004,29.592,3.8829,0.0,5.2273],
[13.0226,32.936,33.5241,7.815,5.231,0.0]
    data['demands'] = [0.0, 6.0,7.0,6.0,4.0,5.0]
    data['vehicle_capacities'] = [10,18,18,10,18,18,10,18,18]
    data['num_vehicles'] = 9
    data['depot'] = 0
    data['vehicle_fuel_costs'] = [0.23,0.3,0.3,0.23,0.3,0.3,0.23,0.3,0.3]
    data['time_matrix'] = 
[[0.0,35.6016,36.865,17.8066,15.8583,16.1166],
[35.015,0.0,2.04,18.675,20.715,25.2933],
[37.9716,3.41833,0.0,21.6316,23.6716,28.25],
[17.8650,19.5466,20.81,0.0,3.565,8.1433],
[16.1483,21.41,22.6733,3.615,0.0,6.165],
[15.4233,24.505,25.7683,6.71,4.7616,0.0]]
    data['time_windows'] = 
[(0, 780),
 (0, 780),
 (0, 780),
 (0, 780),
 (0, 780),
 (0, 780)]
    data['service_time'] = [0.0,12.0,14.0,12.0,8.0,10.0]
    return data

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    dist_dict = {}
    print(f'Objective: {solution.ObjectiveValue()}')
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            plan_output += '{0} Time({1},{2}) -> '.format(
                manager.IndexToNode(index), solution.Min(time_var),
                solution.Max(time_var))
            index = solution.Value(routing.NextVar(index))
        time_var = time_dimension.CumulVar(index)
        plan_output += '{0} Time({1},{2})\n'.format(manager.IndexToNode(index),
                                                    solution.Min(time_var),
                                                    solution.Max(time_var))
        plan_output += 'Time of the route: {}min\n'.format(
            solution.Min(time_var))
        print(plan_output)
        total_time += solution.Min(time_var)
    print('Total time of all routes: {}min'.format(total_time))
    return dist_dict, data

def main():
    """Solve the CVRP problem."""
    data = create_data_model()
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)
    callback_indices = []
    for vehicle_idx in range(data['num_vehicles']):
        def vehicle_callback(from_index, to_index, i=vehicle_idx):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['vehicle_fuel_costs'][i] * data['distance_matrix'][from_node][to_node]
        callback_index = routing.RegisterTransitCallback(vehicle_callback)
        routing.SetArcCostEvaluatorOfVehicle(callback_index, vehicle_idx)
        callback_indices.append(callback_index)
    routing.AddDimensionWithVehicleTransits(
        callback_indices,
        0,
        100000000000,
        True,
        'Distance')
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]
    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')
    callback_indices2 = []
    for vehicle_idx in range(data['num_vehicles']):
        def time_callback(from_index, to_index, i=vehicle_idx):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int(data['service_time'][to_node]) + data['time_matrix'][from_node][to_node]
        callback_index2 = routing.RegisterTransitCallback(time_callback)
        routing.SetArcCostEvaluatorOfVehicle(callback_index2, vehicle_idx)
        callback_indices2.append(callback_index2)

        
    routing.AddDimensionWithVehicleTransits(
        callback_indices2,
        780,
        780,
        False,
    'Time')
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 60
    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        dist_dict, data = print_solution(data, manager, routing, solution)
        return dist_dict, data
    else:
        print('No solution with these constraints.')
        return None, None
if __name__ == '__main__':
    dist_dict, data = main()
    dist_dict, data 