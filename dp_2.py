# -*- coding: utf-8 -*-
sample = ['AGT','AGCTT']
def  make_optimal_path(arg, max_node, aminos):
    width = len(arg[0])
    for a in arg:
        print(a)
    print("#"*100)
    big_arg = []
    for ar in arg:
        node_score_arg = []
        for a in ar:
            node_score_arg.extend([a[1]])
        big_arg.extend([node_score_arg])
    arg = big_arg
    for i in arg:
        print(i)
    
    last = arg[-1][-1]
    print(width)
    print(last)
    if type(last) == list:
        route_path = [last]
    else:
    while last != 0:
        if type(last) == list:
            last = last[0]
            route_path.extend([last])
            # path = route_path
            # route_path = []
            # print("PATHは",path)
            # for i in last:
            #     i = arg[(last//width)][last%width - 1]
            #     print(i)
            #     path.extend([i])
            #     route_path.extend(path)
        else:
            last = arg[(last//width)][last%width - 1]
            route_path.extend([last])

    print(route_path)


def check_score_and_prenode(arg, aminos):
    width = len(arg[0])
    amino_height = aminos[0] 
    amino_width = aminos[1]
    max_node = (len(amino_height)+ 1)*(len(amino_width) + 1)
    the_arg = arg[1:] 
    rows_counter = 1
    for mono_array in the_arg: # [-6,None,None,None,None]
        rows_counter = rows_counter + 1
        simple_counter = 0
        for arr in mono_array: # -6
            this_number = width*(rows_counter-1) + simple_counter + 1
            if arr == None: # rows_counterが    横, simple_counterが縦
                left = arg[rows_counter - 1][simple_counter - 1]
                diagonal = arg[rows_counter - 2][simple_counter - 1]
                top = arg[rows_counter - 2][simple_counter]

                if amino_height[rows_counter - 2] == amino_width[simple_counter - 1]:
                    gap = 1 #　一致した時
                else:
                    gap = -2 #　一致していない時

                # ["最大スコア", "ノード番号", ["左スコア", "斜スコア", "上スコア"]]
                if (left[2][0] is None) and (left[2][1] is None):
                    from_left = None
                elif left[2][0] is None:
                    from_left = left[2][1] - 10
                elif left[2][1] is None:
                    from_left = left[2][0] - 2
                else:
                    from_left = max(left[2][0] - 2, left[2][1] - 10)

                if (top[2][1] is None) and (top[2][2] is None):
                    from_top = None
                elif top[2][1] is None:
                    from_top = top[2][2] - 2
                elif top[2][2] is None:
                    from_top = top[2][1] - 10
                else:
                    from_top = max(top[2][1] - 10, top[2][2] - 2)
                pre_d = [from_left, diagonal[0] + gap, from_top] # [左からのスコア, 斜めからのスコア,  上からのスコア]
                pre_a = [x for x in pre_d if x is not None]
                max_val = max(pre_a) #最大スコア
                if pre_d.count(max_val) != 1: # 複数からの経路の時
                    if pre_d[0] == pre_d[1] == pre_d[2]: # 左・斜め・上
                        number = [this_number - 1, this_number - width, this_number - width - 1]
                    elif pre_d[1] == pre_d[2]: # 斜め・上
                        number = [this_number - width, this_number - width - 1]
                    elif pre_d[0] == pre_d[2]: # 左・上
                        number = [this_number - 1, this_number - width]
                    elif pre_d[0] == pre_d[1]:
                       number = [this_number - 1, this_number - width - 1]
                else: # 単数からの経路の時
                    if pre_d.index(max_val) == 0:# 左から
                        number = this_number - 1
                    elif pre_d.index(max_val) == 1: # 斜めから
                        number = this_number - width - 1
                    elif pre_d.index(max_val) == 2: # 上から
                        number = this_number - width

                d = [max_val, number, pre_d]
                arg[rows_counter - 1][simple_counter]= d
            simple_counter = simple_counter + 1
    make_optimal_path(arg, max_node, aminos)


def make_array(arg):
    arg1 = list(arg[0])
    arg2 = list(arg[1])
    print('アライメント前：', arg1, arg2)
    arg_amino = [arg1, arg2]
    l = [None] * len(arg2)
    width = len(arg2) + 1
    simple_array = []
    counter = 0
    col_counter =  1 - width
    for i in range(len(arg1) + 1):
        num = [[counter * -3, col_counter, [None, None, None]]]
        num.extend(l)
        simple_array.append(num)
        counter = counter + 1
        col_counter = col_counter + width 
        
    # 配列に初期のギャップを入れる
    first = simple_array[0]
    counter = 0
    first_array = [] 
    row_counter = 0  
    for i in first:
        i = [counter * -3, row_counter, [None, None, None]]
        first_array.append(i)
        counter = counter + 1
        row_counter = row_counter + 1
    simple_array[0] = first_array
    for i in simple_array:
        print(i)
    check_score_and_prenode(simple_array, arg_amino)

make_array(sample)


a = [
[0, 1, 2, 3, 4, 5]
,[1, 1, 2, [3, 4], 4, 5]
,[7, 7, 8, 9, [16, 10], 17]
,[13, 13, 14, 15, 16, 17]
]