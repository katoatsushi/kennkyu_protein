# -*- coding: utf-8 -*-
sample = ['AGT','AGCTT']
# sample = ['AGCTTGGGTTTTTTT','AGCTTGGGTTTGGGGTTTT']

def alignment(aminos, result_array):
    print(result_array)
    amino_a = aminos[0]
    amino_b = aminos[1]
    alignment_s = []
    alignment_l = []
    counter_s = 0
    counter_l = 0
    for i in result_array:
        if i == 'OK':
            alignment_s.append(amino_a[counter_s])
            alignment_l.append(amino_b[counter_l])
            counter_s = counter_s + 1
            counter_l = counter_l + 1
        elif i == 'R': 
            alignment_s.append('-')
            alignment_l.append(amino_b[counter_l])
            counter_l = counter_l + 1
        elif i == 'D':
            alignment_l.append('-')
            alignment_s.append(amino_a[counter_s])
            counter_s = counter_s + 1
    alignment = [alignment_s, alignment_l]
    return alignment

def alignment_result(node_num_array, aminos):   
    print(node_num_array)
    result_array = []
    pre_node = node_num_array[0]
    counter = 0
    width = len(aminos[1]) + 1
    for i in node_num_array:
        gap = node_num_array[counter + 1] - i
        if gap == 1:
            result_array.append("R")
        elif gap == width:
            result_array.append("D")
        else:
            result_array.append("OK")
        pre_node = i
        counter = counter + 1
        if (counter + 1) == len(node_num_array):
            break
    res = alignment(aminos, result_array)
    print('アライメント後：', res)

def  make_optimal_path(arg, node_data, aminos):
    next_node = arg[-1][-1]
    route_path = []
    if type(next_node) == list:
        for i in next_node:
            route_path.extend([i])
    else:
        route_path = [next_node]

    next_node = None
    while next_node != [1]:
        all_ways = []
        for route in route_path:
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
    print("AAAAAAAAAAAAAAAAAAAAAAA")
    print(all_ways)
    max_node_num = node_data['max_node_num'] 
    if type(all_ways[0]) == list: #複数経路がある場合
        for way in all_ways:
            # way = list(map(lambda x: x+1, way))
            way.reverse()
            way.append(node_data['max_node_num'])
            alignment_result(way, aminos)
    else:
        # all_ways = list(map(lambda x: x+1, all_ways))
        all_ways.reverse()
        all_ways.append(node_data['max_node_num'])
        alignment_result(all_ways, aminos)


def check_score_and_prenode(arg, aminos): # ["最大スコア", "ノード番号", ["左スコア", "斜スコア", "上スコア"]]
    width = len(arg[0])
    amino_height = aminos[0] 
    amino_width = aminos[1]
    max_node = (len(amino_height)+ 1)*(len(amino_width) + 1)
    node_data = {'width': len(aminos[1]) + 1,'height': len(aminos[0]) + 1,'max_node_num': max_node}
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
                pre_a = [x for x in pre_d if x is not None] #スコアの中からNoneを排除
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

                d = [max_val, number, pre_d]# ["最大スコア", "ノード番号", ["左スコア", "斜スコア", "上スコア"]]
                arg[rows_counter - 1][simple_counter]= d # 当ノードに上の情報を再代入
            simple_counter = simple_counter + 1

    big_arg = [] # ノードの情報だけを抽出
    for ar in arg:
        node_score_arg = []
        for a in ar:
            node_score_arg.extend([a[1]])
        big_arg.extend([node_score_arg])
    arg = big_arg
    make_optimal_path(arg, node_data, aminos)


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