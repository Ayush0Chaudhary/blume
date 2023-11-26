from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


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



    datas = [
        [1, 4],
        [1, 5],
        [1, 6],
        [1, 7],
        [1, 8],
        [1, 9],
        [1, 10],
        [2, 11],
        [2, 12],
        [2, 13],
        [2, 14],
        [2, 15],
        [2, 16],
        [2, 17],
        [2, 18],
        [2, 19],
        [2, 20],
        [3, 21],
        [3, 22],
        [3, 23],
        [3, 24],
        [3, 25],
    ]



    
    mp_store_to_depot = {}
    mp_depot_to_store = {}

    data["depots"] = [
        [4,5,6,7,8,9,10],
        [11,12,13,14,15,16,17,18,19,20],
        [21,22,23,24,25]
    ]
    for i in range(data["no_of_depot"]):
        for j in range(len(data["depots"][i])):
            data["depots"][i][j] = data["depots"][i][j] - 1

    # print(data["depots"])
    data["depots_dist_matrix"] = []

    for i in range(data["no_of_depot"]):
        data["depots"][i].insert(0,i)
        rows = []
        for ii in range(len(data["depots"][i])):
            row = []
            for jj in range(len(data["depots"][i])):
                row.append(data["distance_matrix"][data["depots"][i][ii]][data["depots"][i][jj]])
            rows.append(row)
        data["depots_dist_matrix"].append(rows)
    
    for i in range(len(datas)):
        mp_store_to_depot[datas[i][1]] = datas[i][0]
        mp_depot_to_store[datas[i][0]] = datas[i][1]

    data["pickups_deliveries_dts"] = mp_store_to_depot
    data["pickups_deliveries_std"] = mp_depot_to_store

    data["vehicles_num"] = [
        [5, 1],
        [3, 1],
        [5, 1]
    ]

    data["vehicle_specs"] = [
        # wgt   vol fixedCost   varCost   maxDist   speed
        [61200, 2389, 1000, 100, 10000000, 40],
        [61200, 2389, 2000, 60, 120, 45]
    ]

    data["demands"] = [
        ('Demand1',  4,  5497, 322, '10:00', '12:00', '15:00', '19:00'),
        ('Demand2',  5,  6072, 460, '10:00', '12:00', '16:00', '19:00'),
        ('Demand3',  6, 11362, 345, '10:00', '12:00', '17:00', '19:00'),
        ('Demand4',  7,  9568, 552, '10:00', '12:00', '12:00', '19:00'),
        ('Demand5',  8,  7153, 391, '10:00', '12:00', '12:00', '19:00'),
        ('Demand6',  8,  5244, 437, '10:00', '12:00', '12:00', '19:00'),
        ('Demand7', 11,  6095, 483, '10:00', '12:00', '12:00', '19:00'),
        ('Demand8', 12,  6072, 253, '10:00', '12:00', '12:00', '19:00'),
        ('Demand9', 13, 10281, 460, '10:00', '12:00', '15:00', '19:00'),
        ('Demand10', 14, 11063, 391, '10:00', '12:00', '16:00', '19:00'),
        ('Demand11', 15,  5635, 322, '10:00', '12:00', '17:00', '19:00'),
        ('Demand12', 16,  9637, 437, '10:00', '12:00', '12:00', '19:00'),
        ('Demand13', 17,  6578, 322, '10:00', '12:00', '12:00', '19:00'),
        ('Demand14', 18,  8556, 253, '10:00', '12:00', '12:00', '19:00'),
        ('Demand15', 19,  5520, 230, '10:00', '12:00', '15:00', '19:00'),
        ('Demand16', 21,  5037, 575, '10:00', '12:00', '16:00', '19:00'),
        ('Demand17', 22,  8280, 368, '10:00', '12:00', '17:00', '19:00'),
        ('Demand18', 23, 11086, 506, '10:00', '12:00', '12:00', '19:00'),
        ('Demand19', 24, 10189, 414, '10:00', '12:00', '12:00', '19:00'),
        ('Demand20', 25,  8970, 322, '10:00', '12:00', '12:00', '19:00'),
        ('Demand21', 21, 11224, 529, '10:00', '12:00', '12:00', '19:00'),
        ('Demand22', 22, 10994, 552, '10:00', '12:00', '12:00', '19:00'),
        ('Demand23', 23,  7291, 414, '10:00', '12:00', '15:00', '19:00'),
        ('Demand24', 10, 11293, 552, '10:00', '12:00', '16:00', '19:00'),
        ('Demand25',  9,  5175, 299, '10:00', '12:00', '17:00', '19:00'),
        ('Demand26',  8,  8257, 299, '10:00', '12:00', '12:00', '19:00'),
        ('Demand27',  7,  5842, 230, '10:00', '12:00', '12:00', '19:00'),
        ('Demand28',  6, 10235, 345, '10:00', '12:00', '12:00', '19:00'),
        ('Demand29',  5,  9177, 414, '10:00', '12:00', '12:00', '19:00'),
        ('Demand30',  4,  5704, 345, '10:00', '12:00', '15:00', '19:00'),
        ('Demand31',  6,  5704, 414, '10:00', '12:00', '16:00', '19:00'),
        ('Demand32',  7,  6716, 368, '10:00', '12:00', '17:00', '19:00'),
        ('Demand33',  8,  9292, 562, '10:00', '12:00', '12:00', '19:00'),
        ('Demand34',  9,  4292, 562, '10:00', '12:00', '12:00', '19:00'),
        ('Demand35', 10,  5292, 563, '10:00', '12:00', '12:00', '19:00'),
        ('Demand36', 20,  6292, 564, '10:00', '12:00', '12:00', '19:00'),
        ('Demand37', 19,  6711, 562, '10:00', '12:00', '15:00', '19:00'),
        ('Demand38', 18, 11711, 563, '10:00', '12:00', '16:00', '19:00'),
        ('Demand39', 17,  6711, 564, '10:00', '12:00', '17:00', '19:00'),
        ('Demand40', 16,  6711, 565, '10:00', '12:00', '12:00', '19:00'),
        ('Demand41', 15,  6711, 566, '10:00', '12:00', '12:00', '19:00'),
        ('Demand42', 14,  6711, 567, '10:00', '12:00', '12:00', '19:00'),
        ('Demand43', 25,  6711, 568, '10:00', '12:00', '12:00', '19:00'),
        ('Demand44', 25,  6711, 569, '10:00', '12:00', '12:00', '19:00'),
        ('Demand45', 24,  6711, 570, '10:00', '12:00', '16:00', '19:00'),
        ('Demand46', 24,  6711, 571, '10:00', '12:00', '17:00', '19:00'),
        ('Demand47', 23,  6711, 572, '10:00', '12:00', '12:00', '19:00'),
        ('Demand48', 23,  6711, 573, '10:00', '12:00', '12:00', '19:00'),
        ('Demand49', 22,  6711, 574, '10:00', '12:00', '12:00', '19:00'),
        ('Demand50', 21,  6711, 575, '10:00', '12:00', '12:00', '19:00')]
    
    return data

def convert_time_to_numeric(time_str):
    # Convert 'HH:MM' format to numeric value
    hours, minutes = map(int, time_str.split(':'))
    return hours + minutes / 60

# data[vehicle_num] 
# conv    electric


def main():
    data = create_data_model()
    # print(data["depots_dist_matrix"])
    # print(data["distance_matrix"])
    # this is the manager for the depot distance matrix. 
    manager = pywrapcp.RoutingIndexManager(
        # Total depot+store,                total vehicle,                                   depot node
        len(data["depots_dist_matrix"][0]), data["vehicles_num"][0][0] + data["vehicles_num"][0][1], 0
    )

    routing = pywrapcp.RoutingModel(manager)

        # Define cost of each arc.
    def distance_callback(from_index, to_index):
        """Returns the manhattan distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]
    
    # TODO: To be change
    def cost_function(vehicle, distance):
        if vehicle in [0,1,2,3,4]:  # Vehicle 1 with $100 for 1 km
            return distance * data["vehicle_specs"][0][3]
        elif vehicle == 5:  # Vehicle 2 with $60 for 1 km
            return distance * data['vehicle_specs'][1][3]

# FIXME: Not sure about this, change in future to setting cost evaluator of individual vehicle
#####################################################
    # registring the callback
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    # TODO: To be changed
    cost_callback = lambda from_index, to_index: cost_function(manager.vehicle(from_index), distance_callback(from_index, to_index))
    transit_callback_index = routing.RegisterTransitCallback(cost_callback)
    # Set the cost function for the arc costs.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
#######################################################33
    # vehicle_id = 0
    # for i in data["vehicles_num"][0]:
    #     # I is here 5 or 1
    #     for j in range(i):
    #         #  j is here 0,1,2,3,4,
    #         print(j)


    #         vehicle_id += 1
    #         if i is 0:
    #             routing.SetFixedCostOfVehicle(cost=1000, vehicle=vehicle_id)
    #             routing.SetArcCostEvaluatorOfVehicle(evaluator_index=transit_callback_index, vehicle=vehicle_id)
    #         else:
    #             routing.SetFixedCostOfVehicle(cost=2000, vehicle=vehicle_id)
    
    # routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
#########################################################

    max_dist_cap = []

    #  data["vehicles_num"] = [
    #     [5, 1],
    #     [3, 1],
    #     [5, 1]
    # ]
    
    # TODO: its for one loop only
    for j in range(data["vehicles_num"][0][0]):
        # TODO: its for one loop only
        max_dist_cap.append(data["vehicle_specs"][0][4])
    # TODO: its for one loop only
    for j in range(data["vehicles_num"][0][1]):
        # TODO: its for one loop only
        max_dist_cap.append(data["vehicle_specs"][1][4])
    
    print(max_dist_cap)
    # Add Distance constraint.
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        max_dist_cap,  # vehicle maximum travel distance
        True,  # start cumul to zero
        "Distance"
    )

    distance_dimension = routing.GetDimensionOrDie("Distance")
    # this is supposed to make the cost of the distance to be 100 times more important than the cost of each step
    # TODO: On verge, copilot suggested that it is for distance/fixed_cost 
    # https://developers.google.com/optimization/reference/python/constraint_solver/pywrapcp#setglobalspancostcoefficient
    distance_dimension.SetGlobalSpanCostCoefficient(100)







if __name__ == "__main__":
    main()
