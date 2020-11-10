# sample = ['AGT', 'AGCT']
sample = ['AGCT','AGT']
# sample = ['AGTFYUKKPB', 'AGCT']
#sample = ['AGTUT', 'AGCTTT']
#sample = ['AGTT', 'AGCT']
def alignment(aminos, result_array):
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

def  make_optimal_path(arg, max_node, aminos):
    flatten_div_array = []
    for mini_arg in arg:
        for i in mini_arg:
            flatten_div_array.append(i)
    # 3元配列から2元配列に変換
    last = flatten_div_array[-1]
    main_array = [last[1]]
    while type(flatten_div_array[last[1]-1]) == list:
        last = flatten_div_array[last[1]-1]
        main_array.append(last[1])
    main_array.reverse()
    main_array.append(max_node)
    alignment_result(main_array, aminos)

def check_score_and_prenode(arg, aminos):
    width = len(arg[0])
    amino_height = aminos[0] # ['A','G','T']
    amino_width = aminos[1] # ['A','G','C','T']
    max_node = (len(amino_height)+ 1)*(len(amino_width) + 1)
    the_arg = arg[1:] 
    rows_counter = 1
    for mono_array in the_arg: # [-6,None,None,None,None]
        rows_counter = rows_counter + 1
        simple_counter = 0
        for arr in mono_array: # -6
            this_number = width*(rows_counter-1) + simple_counter + 1
            if arr == None:
                # 最大スコアと移動前のノードを決める 
                # rows_counter　が横, simple_counterが縦
                left = arg[rows_counter - 1][simple_counter - 1]
                if type(left) == list:
                    left = left[0]
                top = arg[rows_counter - 2][simple_counter]
                if type(top) == list:
                    top = top[0]
                diagonal = arg[rows_counter - 2][simple_counter - 1]
                if type(diagonal) == list:
                    diagonal = diagonal[0]
                if amino_height[rows_counter - 2] == amino_width[simple_counter - 1]:
                    gap = 1 #　一致した時
                else:
                    gap = -2 #　一致していない時
                score_array = [left-3, top-3, diagonal + gap]
                max_score = max(score_array)
                if type(max_score) == list: # 経路が複数ある場合は最初の経路だけを取得する
                    if max_score[0] == max_score[1] == max_score[2]:
                        number = [this_number - 1, this_number - width, this_number - width - 1]
                        arg[rows_counter - 1][simple_counter]= [max_score, number]
                    elif max_score[0] == max_score[1]:
                        number = [this_number - 1, this_number - width]
                        arg[rows_counter - 1][simple_counter]= [max_score, number]
                    elif max_score[0] == max_score[2]:
                        number = [this_number - 1, this_number - width - 1]
                        arg[rows_counter - 1][simple_counter]= [max_score, number]
                    elif max_score[1] == max_score[2]:
                        number = [this_number - width, this_number - width - 1]
                        arg[rows_counter - 1][simple_counter]= [max_score, number]
                else:
                    if score_array.index(max_score) == 0: # 左から来た時
                        number = this_number - 1
                        arg[rows_counter - 1][simple_counter]= [max_score, number]
                    elif score_array.index(max_score) == 1:  # 上から来た時
                        number = this_number - width
                        arg[rows_counter - 1][simple_counter]= [max_score, number]
                    elif score_array.index(max_score) == 2: # 斜めから来た時
                        number = this_number - width - 1
                        arg[rows_counter - 1][simple_counter] = [max_score, number]
            simple_counter = simple_counter + 1
    make_optimal_path(arg, max_node, aminos)

def make_array(arg):
    arg1 = list(arg[0])
    arg2 = list(arg[1])
    print('アライメント前：', arg1, arg2)
    arg_amino = [arg1, arg2]
    l = [None] * len(arg2)
    simple_array = []
    counter = 0
    for i in range(len(arg1) + 1):
        num = [counter * -3]
        num.extend(l)
        simple_array.append(num)
        counter = counter + 1
    # 配列に初期のギャップを入れる
    first = simple_array[0]
    counter = 0
    first_array = []
    for i in first:
        i = counter*-3
        first_array.append(i)
        counter = counter + 1
    simple_array[0] = first_array
    print(simple_array)
    print("%"*200)
    check_score_and_prenode(simple_array, arg_amino)

# make_array関数を起動
make_array(sample)