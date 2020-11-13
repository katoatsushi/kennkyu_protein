import itertools

arg = [[0, 1, 2, 3, 4, 5],
    [1, 1, 2, 3, 4, 5],
    [7, 7, 8, 9, [16, 10], 17],
    [13, 13, 14, 15, 16, [17, 23]]
]
node_data = {'height': 4, 'width': 6, 'max_node_num': 24}
###############################################################

next_node = arg[-1][-1]
route_path = []
if type(next_node) == list:
    for i in next_node:
        route_path.extend([i])
else:
    route_path = [next_node]

next_node = None
while next_node != [0]:
    all_ways = []
    for route in route_path:
        # print("今回のrouteはこいつだああ", route)
        if type(route) == int:
            route = [route]
        last = route[-1]
        next_node = arg[last//node_data['width']][last%node_data['width'] - 1]
        if type(next_node) == int:
            next_node = [next_node]
        new_one = [route]*len(next_node) #[[7],[7]]
        append_one = list(zip(new_one, next_node))# [([17, 4], 16), ([17, 4], 10)]
        for a in append_one:
            all_ways.append(a[0] + [a[1]])

    route_path = all_ways
print(all_ways)
