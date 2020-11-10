# -*- coding: utf-8 -*-
sample = ['AGT','AGCTT']

def check_score_and_prenode(arg, aminos):
    for a in arg:
        print(a)
    width = len(arg[0])
    amino_height = aminos[0] # ['A','G','T']
    amino_width = aminos[1] # ['A','G','C','T']
    max_node = (len(amino_height)+ 1)*(len(amino_width) + 1)
    the_arg = arg[1:] 
    rows_counter = 1
    for mono_array in the_arg: # [-6,None,None,None,None]
        rows_counter = rows_counter + 1
        simple_counter = 1
        for arr in mono_array: # -6
            this_number = width*(rows_counter-1) + simple_counter + 1
            # print("arrは", arr)
            # print("+"*100)
            # print(arg[2][0])
            if arr == "None":
                print("rows_counterが", rows_counter,"simple_counterが",simple_counter)
                # 最大スコアと移動前のノードを決める 
                # rows_counter　が横, simple_counterが縦
                left = arg[rows_counter - 1][simple_counter - 1]
                diagonal = arg[rows_counter - 2][simple_counter - 1]
                top = arg[rows_counter - 2][simple_counter]
                if amino_height[rows_counter - 2] == amino_width[simple_counter - 1]:
                    gap = 1 #　一致した時
                else:
                    gap = -2 #　一致していない時
                # ["最大スコア", "ノード番号", ["左スコア", "斜スコア", "上スコア"]]
                print(left,"P"*100)
                print(left)
                print("J"*100)
                if (left[2][0] == "None") and (left[2][1] == "None"):
                    from_left = "None"
                elif left[2][0] == "None":
                    from_left = left[2][1] - 10
                elif left[2][1] == "None":
                    from_left = left[2][0] - 2
                else:
                    from_left = max(left[2][0] - 2, left[2][1] - 10)

                if (top[2][1] == "None" and top[2][2] == "None"):
                    from_top = "None"
                elif top[2][1] == "None":
                    from_top = top[2][1] - 10
                elif top[2][2] == "None":
                    from_top = top[2][2] - 2
                else:
                    from_top = max(top[2][1] - 10, top[2][2] - 2)

                pre_d = [from_left, diagonal[0] + gap, from_top]
                max_val = max(pre_d)

                if pre_d.count(max_val) != 1: # 複数からの経路の時
                    if pre_d[0] == pre_d[1] == pre_d[2]:
                        number = [this_number - 1, this_number - width, this_number - width - 1]
                    elif pre_d[1] == pre_d[2]:
                        number = [this_number - width, this_number - width - 1]
                    elif pre_d[0] == pre_d[2]:
                        number = [this_number - 1, this_number - width]
                    elif pre_d[0] == pre_d[1]:
                       number = [this_number - 1, this_number - width - 1]
                else: # 単数からの経路の時
                    if pre_d.index(max_val) == 0:
                        number = this_number - 1
                    elif pre_d.index(max_val) == 1:
                        number = this_number - width - 1
                    elif pre_d.index(max_val) == 2:
                        number = this_number - width
                d = [max_val, number, pre_d]
                arg[rows_counter - 1][simple_counter]= d

        simple_counter = simple_counter + 1
    # make_optimal_path(arg, max_node, aminos)
    for a in arg:
        print(a)

def make_array(arg):
    arg1 = list(arg[0])
    arg2 = list(arg[1])
    print('アライメント前：', arg1, arg2)
    arg_amino = [arg1, arg2]
    l = ["None"] * len(arg2)
    # print(l)
    simple_array = []
    counter = 0
    for i in range(len(arg1) + 1):
        # num = [counter * -3]
        num = [[counter * -3, "None", ["None", "None", "None"]]]
        num.extend(l)
        simple_array.append(num)
        counter = counter + 1
    # 配列に初期のギャップを入れる
    first = simple_array[0]
    counter = 0
    first_array = []
    for i in first:
        # i = counter*-3
        i = [counter * -3, "None", ["None", "None", "None"]]
        first_array.append(i)
        counter = counter + 1
    simple_array[0] = first_array
    # for s in simple_array:
    #     print(s)
    # print("!"*100)
    check_score_and_prenode(simple_array, arg_amino)

make_array(sample)


# a = [[[0, 'None', ['None', 'None', 'None']], [-3, 'None', ['None', 'None', 'None']], [-6, 'None', ['None', 'None', 'None']], [-9, 'None', ['None', 'None', 'None']], [-12, 'None', ['None', 'None', 'None']], [-15, 'None', ['None', 'None', 'None']]],[[-3, 'None', ['None', 'None', 'None']], 'None', 'None', 'None', 'None', 'None'],[[-6, 'None', ['None', 'None', 'None']], 'None', 'None', 'None', 'None', 'None'],[[-9, 'None', ['None', 'None', 'None']], 'None', 'None', 'None', 'None', 'None']]