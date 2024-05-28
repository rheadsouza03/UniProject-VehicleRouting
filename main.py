import numpy as np

import utility as utility
import loader as loader


def main():
    # Paths to the data and solution files.
    vrp_file = "data/n32-k5.vrp"  # "data/n80-k10.vrp"
    sol_file = "data/n32-k5.sol"  # "data/n80-k10.sol"

    # Loading the VRP data file.
    px, py, demand, capacity, depot = loader.load_data(vrp_file)

    # Displaying to console the distance and visualizing the optimal VRP solution.
    vrp_best_sol = loader.load_solution(sol_file)
    best_distance = utility.calculate_total_distance(vrp_best_sol, px, py, depot)
    print("Best VRP Distance:", best_distance)
    utility.visualise_solution(vrp_best_sol, px, py, depot, "Optimal Solution: " + sol_file)

    # Executing and visualizing the nearest neighbour VRP heuristic.
    nnh_solution = nearest_neighbour_heuristic(px, py, demand, capacity, depot)
    nnh_distance = utility.calculate_total_distance(nnh_solution, px, py, depot)
    print("Nearest Neighbour VRP Heuristic Distance:", nnh_distance)
    utility.visualise_solution(nnh_solution, px, py, depot, "Nearest Neighbour Heuristic: "+vrp_file)

    # Executing and visualizing the saving VRP heuristic.
    # Uncomment it to do your assignment!

    sh_solution = savings_heuristic(px, py, demand, capacity, depot)
    sh_distance = utility.calculate_total_distance(sh_solution, px, py, depot)
    print("Saving VRP Heuristic Distance:", sh_distance)
    utility.visualise_solution(sh_solution, px, py, depot, "Savings Heuristic: " + sol_file)


def nearest_neighbour_heuristic(px, py, demand, capacity, depot):
    """
    Algorithm for the nearest neighbour heuristic to generate VRP solutions.

    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param demand: List of each nodes demand.
    :param capacity: Vehicle carrying capacity.
    :param depot: Depot.
    :return: List of vehicle routes (tours).
    """

    # Initialise the route with the depot
    unvisited_indices = set(range(len(px)))
    unvisited_indices.remove(depot)
    routes = []

    current_route = []
    current_load = 0
    current_index = depot

    while len(unvisited_indices) != 0:
        # Search for a valid nearest-neighbour
        nearest_neighbour = (-1, np.inf)
        for i in unvisited_indices:
            distance = utility.calculate_euclidean_distance(px, py, current_index, i)

            if (distance < nearest_neighbour[1]) & (capacity >= (current_load + demand[i])):
                nearest_neighbour = (i, distance)

        # Add the new nearest neighbour to the route
        if nearest_neighbour[0] > -1:
            current_index = nearest_neighbour[0]
            current_route.append(current_index)
            unvisited_indices.remove(current_index)
            current_load += demand[current_index]

        # Reached capacity or no valid neighbours found, finish the current route
        if ((capacity == current_load) | (nearest_neighbour[0] == -1) |
                ((capacity == current_load) & (nearest_neighbour[0] == -1))):
            # Finish the route
            routes.append(current_route)

            # Re-initialise the variables
            current_route = []
            current_index = depot
            current_load = 0

    # Append the depot to complete the last route if it's not empty
    if current_route:
        routes.append(current_route)

    return routes


def savings_heuristic(px, py, demand, capacity, depot):
    """
    Algorithm for Implementing the savings heuristic to generate VRP solutions.

    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param demand: List of each nodes demand.
    :param capacity: Vehicle carrying capacity.
    :param depot: Depot.
    :return: List of vehicle routes (tours).
    """

    # TODO - Implement the Saving Heuristic to generate VRP solutions.
    # Initialise the route with the depot
    routes = [[i] for i in range(len(px))]
    routes.remove([depot])
    savings = {}

    # Compute the savings for each possible merge
    for i in range(int(len(routes)/2)):
        for j in range(int(len(routes)/2), len(routes)):
            # Ensures the 1st and 2nd indices are not the same node
            if i == j:
                continue

            # Calculate the savings
            distance = (utility.calculate_euclidean_distance(px, py, routes[i][0], depot) +
                        utility.calculate_euclidean_distance(px, py, depot, routes[j][0]) -
                        utility.calculate_euclidean_distance(px, py, routes[i][0], routes[j][0]))
            savings[(routes[i][0], routes[j][0])] = distance

    # Sort savings in descending order
    sorted_savings = sorted(savings.items(), key=lambda x: x[1], reverse=True)

    # Merge routes based on savings
    for (i, j), saving in sorted_savings:
        # Check if nodes i and j are not already in the same route
        if not any(i in route and j in route for route in routes):
            # Find the routes containing i and j
            route_i = next(route for route in routes if i in route)
            route_j = next(route for route in routes if j in route)

            # Check capacity is not exceeded
            if utility.is_total_capacity_valid([route_i, route_j], demand, capacity):
                # Merge route_j into route_i
                route_i.extend(route_j)
                routes.remove(route_j)


    return routes


if __name__ == '__main__':
    main()
