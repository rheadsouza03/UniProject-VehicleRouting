Type `python main.py` or `python3 main.py` and the code should run.

Otherwise, if the loader errors then change line 67 in loader.py "a_route = np.array(a_route_str.split()).astype(int)" to be
"a_route = np.array(a_route_str.split()).astype(np.int)". I changed it to just 'int' because PyCharm was
erroring and saying that it was out  of use and would cause issues with my code.

If you want to view the other data files, then edit the following with the given sol/vrp file in the data directory:

    # Paths to the data and solution files.
    vrp_file = "data/n80-k10.vrp"  # "data/n80-k10.vrp"
    sol_file = "data/n80-k10.sol"  # "data/n80-k10.sol"
