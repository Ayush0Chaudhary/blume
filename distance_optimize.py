
from functools import partial
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def convert_time_to_numeric(time_str):
    # Convert 'HH:MM' format to numeric value
    hours, minutes = map(int, time_str.split(':'))
    return hours


def create_data_model():
    data = {}
    data["no_of_depot"] = 3
    data["no_of_store"] = 22
    data["distance_matrix"] = [
                            # fmt: off
                            [0, 500, 500, 180, 130, 240, 210, 220, 170, 180, 700, 720, 750, 320, 340, 750, 740, 600, 650, 650, 500, 540, 560, 580, 600],
                            [500, 0, 500, 600, 650, 700, 620, 630, 640, 650, 220, 250, 260, 270, 230, 240, 250, 260, 250, 235, 500, 510, 520, 530, 540],
                            [500, 500, 0, 500, 520, 530, 540, 600, 620, 540, 530, 550, 560, 590, 600, 630, 650, 620, 610, 500, 200, 210, 220, 230, 240],
                            [180, 600, 500, 0, 20, 25, 30, 26, 35, 15, 500, 510, 520, 540, 550, 530, 560, 500, 570, 600, 580, 540, 570, 576, 578],
                            [130, 650, 520, 20, 0, 15, 18, 20, 25, 24, 500, 510, 520, 540, 550, 530, 560, 500, 570, 600, 580, 540, 570, 576, 578],
                            [240, 700, 530, 25, 15, 0, 20, 24, 23, 21, 500, 510, 520, 540, 550, 530, 560, 500, 570, 600, 580, 540, 570, 576, 578],
                            [210, 620, 540, 30, 18, 20, 0, 25, 23, 20, 500, 510, 520, 540, 550, 530, 560, 500, 570, 600, 580, 540, 570, 576, 578],
                            [220, 630, 600, 26, 20, 24, 25, 0, 15, 18, 500, 510, 520, 540, 550, 530, 560, 500, 570, 600, 580, 540, 570, 576, 578],
                            [170, 640, 620, 35, 25, 23, 23, 15, 0, 20, 500, 510, 520, 540, 550, 530, 560, 500, 570, 600, 580, 540, 570, 576, 578],
                            [180, 650, 540, 15, 24, 21, 20, 18, 20, 0, 30, 20, 15, 13, 15, 16, 18, 20, 21, 23, 500, 510, 520, 530, 540],
                            [700, 220, 530, 500, 500, 500, 500, 500, 500, 30, 0, 15, 18, 20, 13, 18, 29, 14, 16, 19, 500, 510, 520, 530, 540],
                            [720, 250, 550, 510, 510, 510, 510, 510, 510, 20, 15, 0, 20, 21, 14, 15, 18, 20, 15, 18, 500, 510, 520, 530, 540],
                            [750, 260, 560, 520, 520, 520, 520, 520, 520, 15, 18, 20, 0, 24, 15, 16, 18, 12, 19, 20, 500, 510, 520, 530, 540],
                            [320, 270, 590, 540, 540, 540, 540, 540, 540, 13, 20, 21, 24, 0, 15, 23, 12, 15, 16, 18, 500, 510, 520, 530, 540],
                            [340, 230, 600, 550, 550, 550, 550, 550, 550, 15, 13, 14, 15, 15, 0, 15, 18, 17, 20, 15, 500, 510, 520, 530, 540],
                            [750, 240, 630, 530, 530, 530, 530, 530, 530, 16, 18, 15, 16, 23, 15, 0, 17, 25, 23, 15, 500, 510, 520, 530, 540],
                            [740, 250, 650, 560, 560, 560, 560, 560, 560, 18, 29, 18, 18, 12, 18, 17, 0, 24, 15, 18, 500, 510, 520, 530, 540],
                            [600, 260, 620, 500, 500, 500, 500, 500, 500, 20, 14, 20, 12, 15, 17, 25, 24, 0, 16, 17, 500, 510, 520, 530, 540],
                            [650, 250, 610, 570, 570, 570, 570, 570, 570, 21, 16, 15, 19, 16, 20, 23, 15, 16, 0, 18, 500, 510, 520, 530, 540],
                            [650, 235, 500, 600, 600, 600, 600, 600, 600, 23, 19, 18, 20, 18, 15, 15, 18, 17, 18, 0, 500, 510, 520, 530, 540],
                            [500, 500, 200, 580, 580, 580, 580, 580, 580, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 0, 15, 25, 35, 5],
                            [540, 510, 210, 540, 540, 540, 540, 540, 540, 510, 510, 510, 510, 510, 510, 510, 510, 510, 510, 510, 15, 0, 35, 45, 50],
                            [560, 520, 220, 570, 570, 570, 570, 570, 570, 520, 520, 520, 520, 520, 520, 520, 520, 520, 520, 520, 25, 35, 0, 10, 15],
                            [580, 530, 230, 576, 576, 576, 576, 576, 576, 530, 530, 530, 530, 530, 530, 530, 530, 530, 530, 530, 35, 45, 10, 0, 16],
                            [600, 540, 240, 578, 578, 578, 578, 578, 578, 540, 540, 540, 540, 540, 540, 540, 540, 540, 540, 540, 5, 50, 15, 16, 0]
                            # fmt: on
    ]

    data["depots"] = [
        [4, 5, 6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25]
    ]
    # [[0, 3, 4, 5, 6, 7, 8, 9],
    # [1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    # [2, 20, 21, 22, 23, 24]]

    for i in range(data["no_of_depot"]):
        for j in range(len(data["depots"][i])):
            data["depots"][i][j] = data["depots"][i][j] - 1

    data["vehicles_num"] = [
        [5, 1],
        [3, 1],
        [5, 1]
    ]

    data["vehicle_specs"] = [
        # wgt   vol fixedCost varCost maxDist speed
        [61200, 2389, 1000, 100, 10000, 40],
        [61200, 2389, 2000, 60, 120, 45]
    ]

    data['depot_timings'] = ['10:00', '12:00']

    data["demands"] = [
        ['Demand1',  4,  5497, 322, '10:00', '12:00', '15:00', '19:00'],
        ['Demand2',  5,  6072, 460, '10:00', '12:00', '16:00', '19:00'],
        ['Demand3',  6, 11362, 345, '10:00', '12:00', '17:00', '19:00'],
        ['Demand4',  7,  9568, 552, '10:00', '12:00', '12:00', '19:00'],
        ['Demand5',  8,  7153, 391, '10:00', '12:00', '12:00', '19:00'],
        ['Demand6',  8,  5244, 437, '10:00', '12:00', '12:00', '19:00'],
        ['Demand7', 11,  6095, 483, '10:00', '12:00', '12:00', '19:00'],
        ['Demand8', 12,  6072, 253, '10:00', '12:00', '12:00', '19:00'],
        ['Demand9', 13, 10281, 460, '10:00', '12:00', '15:00', '19:00'],
        ['Demand10', 14, 11063, 391, '10:00', '12:00', '16:00', '19:00'],
        ['Demand11', 15,  5635, 322, '10:00', '12:00', '17:00', '19:00'],
        ['Demand12', 16,  9637, 437, '10:00', '12:00', '12:00', '19:00'],
        ['Demand13', 17,  6578, 322, '10:00', '12:00', '12:00', '19:00'],
        ['Demand14', 18,  8556, 253, '10:00', '12:00', '12:00', '19:00'],
        ['Demand15', 19,  5520, 230, '10:00', '12:00', '15:00', '19:00'],
        ['Demand16', 21,  5037, 575, '10:00', '12:00', '16:00', '19:00'],
        ['Demand17', 22,  8280, 368, '10:00', '12:00', '17:00', '19:00'],
        ['Demand18', 23, 11086, 506, '10:00', '12:00', '12:00', '19:00'],
        ['Demand19', 24, 10189, 414, '10:00', '12:00', '12:00', '19:00'],
        ['Demand20', 25,  8970, 322, '10:00', '12:00', '12:00', '19:00'],
        ['Demand21', 21, 11224, 529, '10:00', '12:00', '12:00', '19:00'],
        ['Demand22', 22, 10994, 552, '10:00', '12:00', '12:00', '19:00'],
        ['Demand23', 23,  7291, 414, '10:00', '12:00', '15:00', '19:00'],
        ['Demand24', 10, 11293, 552, '10:00', '12:00', '16:00', '19:00'],
        ['Demand25',  9,  5175, 299, '10:00', '12:00', '17:00', '19:00'],
        ['Demand26',  8,  8257, 299, '10:00', '12:00', '12:00', '19:00'],
        ['Demand27',  7,  5842, 230, '10:00', '12:00', '12:00', '19:00'],
        ['Demand28',  6, 10235, 345, '10:00', '12:00', '12:00', '19:00'],
        ['Demand29',  5,  9177, 414, '10:00', '12:00', '12:00', '19:00'],
        ['Demand30',  4,  5704, 345, '10:00', '12:00', '15:00', '19:00'],
        ['Demand31',  6,  5704, 414, '10:00', '12:00', '16:00', '19:00'],
        ['Demand32',  7,  6716, 368, '10:00', '12:00', '17:00', '19:00'],
        ['Demand33',  8,  9292, 562, '10:00', '12:00', '12:00', '19:00'],
        ['Demand34',  9,  4292, 562, '10:00', '12:00', '12:00', '19:00'],
        ['Demand35', 10,  5292, 563, '10:00', '12:00', '12:00', '19:00'],
        ['Demand36', 20,  6292, 564, '10:00', '12:00', '12:00', '19:00'],
        ['Demand37', 19,  6711, 562, '10:00', '12:00', '15:00', '19:00'],
        ['Demand38', 18, 11711, 563, '10:00', '12:00', '16:00', '19:00'],
        ['Demand39', 17,  6711, 564, '10:00', '12:00', '17:00', '19:00'],
        ['Demand40', 16,  6711, 565, '10:00', '12:00', '12:00', '19:00'],
        ['Demand41', 15,  6711, 566, '10:00', '12:00', '12:00', '19:00'],
        ['Demand42', 14,  6711, 567, '10:00', '12:00', '12:00', '19:00'],
        ['Demand43', 25,  6711, 568, '10:00', '12:00', '12:00', '19:00'],
        ['Demand44', 25,  6711, 569, '10:00', '12:00', '12:00', '19:00'],
        ['Demand45', 24,  6711, 570, '10:00', '12:00', '16:00', '19:00'],
        ['Demand46', 24,  6711, 571, '10:00', '12:00', '17:00', '19:00'],
        ['Demand47', 23,  6711, 572, '10:00', '12:00', '12:00', '19:00'],
        ['Demand48', 23,  6711, 573, '10:00', '12:00', '12:00', '19:00'],
        ['Demand49', 22,  6711, 574, '10:00', '12:00', '12:00', '19:00'],
        ['Demand50', 21,  6711, 575, '10:00', '12:00', '12:00', '19:00']]

    '''Makiing demand iinto 0 based indexing'''
    for i in range(len(data["demands"])):
        data['demands'][i][1] -= 1

    '''Seprating the demand of different depots'''
    data["depot_demands"] = []
    for depots_store in data["depots"]:
        # depots_store = [3, 4, 5, 6, 7, 8, 9]
        rows = []
        for demand in data["demands"]:
            # because the number are reduced by one in depots_store
            store_idx = demand[1]
            if store_idx in depots_store:
                rows.append(demand)
        data["depot_demands"].append(rows)

    # As we know that the demand reoccur for same shop multiple times in a day
    # and we cannot assign multiple time window to single node
    # NOTE So we will use PSUEDO NODES which happens to be the same node

    # TODO The process of finding the psuedo node can be ooptimized, python not my native DSA language

    frequency_map = {}
    '''Iterate over the demands and find the psuedo node'''
    for demand in data["demands"]:
        # demand = ('Demand1',  4,  5497, 322, '10:00', '12:00', '15:00', '19:00')
        frequency_map[demand[1]] = frequency_map.get(demand[1], 0) + 1

    '''In this we made the noormal matrix without considering the pseudo node yet'''
    data["depots_distance_matrix"] = []
    for i in range(data["no_of_depot"]):
        data["depots"][i].insert(0, i)
        rows = []
        for ii in range(len(data["depots"][i])):
            row = []
            for jj in range(len(data["depots"][i])):
                row.append(data["distance_matrix"]
                           [data["depots"][i][ii]][data["depots"][i][jj]])
            rows.append(row)
        data["depots_distance_matrix"].append(rows)

    # [[0, 3, 4, 5, 6, 7, 8, 9],
    # [1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    # [2, 20, 21, 22, 23, 24]]
    data["time_windows"] = {}
    data["psuedo_nodes_data"] = {}

    '''Making the Time Windows'''
    for index, demands_of_a_depo in enumerate(data["depot_demands"]):
        # demand_of_a_depot contains all the demands of particular component
        freq = {}
        data["time_windows"][index] = {}
        data["time_windows"][index][0] = [convert_time_to_numeric(data["depot_timings"][0]), convert_time_to_numeric(data["depot_timings"][1]), 0]
        last = len(data["depots"][index])
        for demand in demands_of_a_depo:
            key_to_check = demand[1]
            row_num = data["depots"][index].index(key_to_check)
    #         # print(demand[1])
            if key_to_check in freq:
                # matlab pehle hi ho chuka h iska kaam, second oirder from the same store

                # print(row_num, key_to_check)
                # print("last : " + str(last))
                data["time_windows"][index][last] = [convert_time_to_numeric(
                    demand[6]), convert_time_to_numeric(demand[7]), demand[2]]
                data["psuedo_nodes_data"][last] = row_num
                row_to_be_duplicated = data["depots_distance_matrix"][index][row_num]
                data["depots_distance_matrix"][index].append(
                    row_to_be_duplicated)
                last += 1
                cnt = 0
                for i in range(len(data["depots_distance_matrix"][index])):
                    if cnt < len(row_to_be_duplicated):
                        data["depots_distance_matrix"][index][i].append(
                            row_to_be_duplicated[cnt])
                    else:
                        data["depots_distance_matrix"][index][i].append(0)
            else:
                data["time_windows"][index][row_num] = [convert_time_to_numeric(
                    demand[6]), convert_time_to_numeric(demand[7]), demand[2]]
                freq[key_to_check] = 1
                # print("row_num : " + str(row_num))
                data["psuedo_nodes_data"][row_num] = row_num
    # print(data["depots_distance_matrix"])
            data["psuedo_nodes_data"][0] = 0
        # print(freq)
    


    # print(data["psuedo_nodes_data"])
    # print((data["time_windows"][0]))
    # print(frequency_map)
    # print(len(data["depots_distance_matrix"][0]))
    # print(len(data["depots_distance_matrix"][1]))
    # print(len(data["depots_distance_matrix"][2]))
    # print(len(data["depots_distance_matrix"][2])+len(data["depots_distance_matrix"][1])+len(data["depots_distance_matrix"][0]))
    print("\n\n\n\n")
    return data

def print_solution(data, manager, routing, solution, iter):
    """Prints solution on console."""
    total_distance = 0
    time_dimension = routing.GetDimensionOrDie('Time')
    capacity_dimension = routing.GetDimensionOrDie('Capacity')
    print(data["vehicles_num"][iter][0] + data["vehicles_num"][iter][1])
    for vehicle_id in range(data["vehicles_num"][iter][0] + data["vehicles_num"][iter][1]) :
        index = routing.Start(vehicle_id)
        plan_output = f'Route for vehicle {vehicle_id}:\n'
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            load_var = capacity_dimension.CumulVar(index)
            route_load = solution.Value(load_var)
            plan_output += f' {node_index} Load({route_load}) -> '
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        node_index = manager.IndexToNode(index)
        load_var = capacity_dimension.CumulVar(index)
        route_load = solution.Value(load_var)
        plan_output += f' {node_index} Load({route_load})\n'
        plan_output += f'Cost of the route: {route_distance} Ruppees\n'
        print(plan_output)
        total_distance += route_distance
    print(f'Total Cost of all routes: {total_distance} Ruppees')
    return total_distance

def main(increase_trucks: bool = False, truck_type: int = 0, amount: int = 0, max_work_hours: int = 1000):
    '''We are solving the VRPTW problem just 3 times'''
    data = create_data_model()
    operation_cost = 0
    for iter in range(data["no_of_depot"]):

        distance_matrix = data["depots_distance_matrix"][iter]
        time_windows = data["time_windows"][iter]
        depot_number = iter
        vehicle_list = data["vehicles_num"][iter]
        total_vehicles = sum(vehicle_list)
        if increase_trucks:
            if truck_type == 0 or truck_type == 1:
                vehicle_list[truck_type] += amount
                total_vehicles += amount
        '''Calculating all the demands of the depot'''
        total_demands = 0
        for demand in data["depot_demands"][iter]:
            total_demands += demand[2]


        manager = pywrapcp.RoutingIndexManager(
            len(distance_matrix), total_vehicles, 0)

        routing = pywrapcp.RoutingModel(manager)

        ############### DISTANCE #####################

        def distance_callback(from_index, to_index, cost):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distance_matrix[from_node][to_node]*cost


        expensive_vehicle_callback = partial(
            distance_callback, cost=data["vehicle_specs"][0][3])
        cheap_vehicle_callback = partial(
            distance_callback, cost=data["vehicle_specs"][1][3])

        expensive_index = routing.RegisterTransitCallback(
            expensive_vehicle_callback)
        cheap__index = routing.RegisterTransitCallback(cheap_vehicle_callback)

        evaluaters = []
        limits = []
        capacities = []

        # conventional vehicle cost
        for i in range(0, vehicle_list[0]):
            evaluaters.append(expensive_index)
            capacities.append(data["vehicle_specs"][0][0])
            limits.append(data["vehicle_specs"][0][4])
            routing.SetFixedCostOfVehicle(data["vehicle_specs"][0][2], i)
            routing.SetArcCostEvaluatorOfVehicle(expensive_index, i)

        # for electric vehicle cost
        for i in range(vehicle_list[0], total_vehicles):
            evaluaters.append(cheap__index)
            capacities.append(data["vehicle_specs"][1][0])
            limits.append(data["vehicle_specs"][1][4])
            routing.SetFixedCostOfVehicle(data["vehicle_specs"][1][2], i)
            routing.SetArcCostEvaluatorOfVehicle(cheap__index, i)

        dimension_name = "Distance"
        routing.AddDimensionWithVehicleTransitAndCapacity(
            evaluator_indices=evaluaters,
            slack_max=0,  # no slack
            vehicle_capacities=limits,  # vehicle maximum travel distance
            fix_start_cumul_to_zero=True,  # start cumul to zero
            name=dimension_name)

        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        ############### DISTANCE #####################

        ############### CAPACITY #####################

        def demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            if from_index == 0:
                return -total_demands
            from_node = manager.IndexToNode(from_index)
            return data["time_windows"][iter][from_node][2]


        demand_callback_index = routing.RegisterUnaryTransitCallback(
            demand_callback)
        

        capacity = "Capacity"
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            slack_max=total_demands,  # Null Slack, but given for  the depot node
            vehicle_capacities=capacities,
            fix_start_cumul_to_zero=True,
            name=capacity)

        capacity_dimension = routing.GetDimensionOrDie(capacity)

        # As we have set the slack to total_demands, we need to set the store node to 0 OR DO WE?
        for i in range(len(distance_matrix)):
            if i == 0:
                capacity_dimension.SlackVar(i).SetRange(0, total_demands)
                continue
            capacity_dimension.SlackVar(i).SetRange(0, 0)

        ############### CAPACITY #####################


        ############### TIME #####################

        def time_callback(from_index, to_index, speed):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distance_matrix[from_node][to_node]/speed
        

        # wgt   vol fixedCost varCost maxDist speed
        # [61200, 2389, 1000, 100, 10000, 40],
        # [61200, 2389, 2000, 60, 120, 45]
        slow_vehicle_callback = partial(
            time_callback, speed=data["vehicle_specs"][0][5])
        
        fast_vehicle_callback = partial(
            time_callback, speed=data["vehicle_specs"][1][5])
        
        slow_index = routing.RegisterTransitCallback(
            slow_vehicle_callback)
        fast_index = routing.RegisterTransitCallback(
            fast_vehicle_callback)
        
        time_indexes = []
                # conventional vehicle cost
        for i in range(0, vehicle_list[0]):
            time_indexes.append(slow_index)

        # for electric vehicle cost
        for i in range(vehicle_list[0], total_vehicles):
            time_indexes.append(fast_index)

        time = "Time"
        routing.AddDimensionWithVehicleTransits(
            evaluator_indices=time_indexes,
            slack_max=30,  # no slack
            capacity=10000,  # vehicle maximum travel distance
            fix_start_cumul_to_zero=False,  # start cumul to zero
            name=time)
        
        time_dimension = routing.GetDimensionOrDie(time)
        '''Adding the time windows'''
        for i in range(0, len(distance_matrix)):
            #  This is Depot timing, but the things is that the truck can return to the depot at any time
            if i == 0:
                time_dimension.CumulVar(i).SetRange( convert_time_to_numeric(data['depot_timings'][0]), convert_time_to_numeric(data['depot_timings'][1]))
                continue
            time_dimension.CumulVar(i).SetRange(
                data["time_windows"][iter][i][0], data["time_windows"][iter][i][1])


        for vehicle_id in range(total_vehicles):
            index = routing.Start(vehicle_id)
            time_dimension.CumulVar(index).SetRange(convert_time_to_numeric(data['depot_timings'][0]), convert_time_to_numeric(data['depot_timings'][1]))

        for vehicle_id in range(total_vehicles):
            routing.AddVariableMinimizedByFinalizer(
                time_dimension.CumulVar(routing.Start(vehicle_id)))
            routing.AddVariableMinimizedByFinalizer(
                time_dimension.CumulVar(routing.End(vehicle_id)))
            
        ############### TIME #####################

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        search_parameters.time_limit.FromSeconds(1)

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)
        #setting time limit to 1 second



        if solution:
            print(solution.ObjectiveValue())
            operation_cost += print_solution(data, manager, routing, solution, iter)
        else:
            print(solution)
    print(f"Total Operation Cost : {operation_cost} Ruppees")

    return operation_cost


def check_benefit_of_increasing_conventional_trucks():
    '''To check difference between adding the two types of trucks'''
    type1 = main(increase_trucks=True, truck_type=0, amount=1)
    type2 = main(increase_trucks=True, truck_type=1, amount=1)
    print("Total benefit of using conventional trucks : " + str(type1 - type2) + " Ruppees")


def check_benefit_of_increasing_electric_trucks():
    '''To check difference between adding the two types of trucks'''
    type1 = main(increase_trucks=True, truck_type=0, amount=1)
    type2 = main(increase_trucks=True, truck_type=1, amount=1)
    print("Total benefit of using conventional trucks : " + str(- type1 + type2) + " Ruppees")

def check_for_driver_safe_limit():
    '''To check the limit of the driver'''
    no_over_worked_drivers = main(max_work_hours=8)
    print("Cost when we dont force driver to work over hours : " + str(no_over_worked_drivers))

if __name__ == "__main__":
    main()

    '''To check what will happen on incresing the number of trucks'''
    # main(increase_trucks=True, truck_type=0)
    # main(increase_trucks=True, truck_type=1)

    # check_benefit_of_increasing_conventional_trucks()
    # check_benefit_of_increasing_electric_trucks()
    # check_for_driver_safe_limit()

