import matplotlib.pyplot as plt
import math

import numpy as np


def calculate_euclidean_distance(px, py, index1, index2):

    """
    Calculating the Euclidean distances between two nodes

    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param index1: Node 1 index in the coordinate list.
    :param index2: Node 2 index in the coordinate list.
    :return: Euclidean distance between node 1 and 2.
    """

    x_diff = px[index1] - px[index2]
    y_diff = py[index1] - py[index2]

    distance = np.sqrt(x_diff ** 2 + y_diff ** 2)

    return distance


def calculate_total_distance(routes, px, py, depot):

    """
    Calculating the total Euclidean distance of all routes in a solution.

    :param routes: List of routes (list of lists).
    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param depot: Depot.
    :return: Total tour Euclidean distance.
    """
    total_distance = 0
    for route in routes:
        # Add the distance from the depot back to the first node to the total distance
        total_distance += calculate_euclidean_distance(px, py, depot, route[0])

        # Add the distance between customer nodes to the total distance
        for i in range(len(route) - 1):
            total_distance += calculate_euclidean_distance(px, py, route[i], route[i + 1])

        # Add the distance from the last node back to the depot to the total distance
        total_distance += calculate_euclidean_distance(px, py, depot, route[-1])

    return total_distance


def is_total_capacity_valid(routes, demand, capacity):
    """
    Checking if the total demand across all routes are valid, for savings heuristic.

    :param routes: list of routes (list of lists).
    :param demand: list of each node's demand (list of numbers).
    :param capacity: total capacity allowed across the both routes to be merged.
    :return: True is capacity >= total demand. Otherwise, false.
    """
    total_load = 0
    for route in routes:
        for node_index in route:
            total_load += demand[node_index]

            if total_load > capacity:
                return False

    return True


def visualise_solution(vrp_sol, px, py, depot, title):
    """
    Function to visualize the tour on a 2D figure.

    :param vrp_sol: The vrp solution, which is a list of lists (excluding the depot).
    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param depot: the depot index
    :param title: Plot title.
    """
    n_routes = len(vrp_sol)

    # Set axis to slightly larger than the set of x and y
    min_x, max_x, min_y, max_y = min(px), max(px), min(py), max(py)
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2

    width = (max(px) - min(px)) * 1.1
    height = (max(py) - min(py)) * 1.1

    min_x = center_x - width / 2
    max_x = center_x + width / 2
    min_y = center_y - height / 2
    max_y = center_y + height / 2

    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)

    plt.plot(px[depot], py[depot], 'rs', markersize=5)
    plt.text(px[depot], py[depot], str(depot), fontsize=12, ha='right')

    cmap = plt.cm.get_cmap("tab20", n_routes)
    for k in range(n_routes):
        a_route = vrp_sol[k]

        # Draw the route: linking to the depot
        plt.plot([px[depot], px[a_route[0]]], [py[depot], py[a_route[0]]], color=cmap(k))
        plt.plot([px[a_route[-1]], px[depot]], [py[a_route[-1]], py[depot]], color=cmap(k))

        # Draw the route: one by one
        for i in range(len(a_route)-1):
            plt.plot([px[a_route[i]], px[a_route[i + 1]]], [py[a_route[i]], py[a_route[i + 1]]], color=cmap(k))
            plt.plot(px[a_route[i]], py[a_route[i]], 'co', markersize=5, color=cmap(k))
            plt.text(px[a_route[i]], py[a_route[i]], str(a_route[i]), fontsize=12, ha='right')

        plt.plot(px[a_route[-1]], py[a_route[-1]], 'co', markersize=5, color=cmap(k))
        plt.text(px[a_route[-1]], py[a_route[-1]], str(a_route[-1]), fontsize=12, ha='right')

    plt.title(title)
    plt.show()
