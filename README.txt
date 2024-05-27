This should work like the other skeleton codes for python.
If the loader errors then change line 64 "a_route = np.array(a_route_str.split()).astype(int)" to be
"a_route = np.array(a_route_str.split()).astype(np.int)". I changed it to just 'int' because PyCharm was
erroring and saying that it was out  of use and would cause issues with my code.