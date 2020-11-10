# sample = ['AGT', 'AGCT']
# sample = ['AGCT','AGT']
sample = ['LIVELY','MICKEY']
PAM_amino = ['C','S','T','P','A','G','N','D','E','Q','H','R','K','M','I','L','V','F','Y','W']
PAM_score = [[12],
            [0,2],
            [-2,0,3],
            [-3,1,0,5],
            [-2,1,1,1,2],
            [-3,1,0,-1,1,5],
            [-4,1,0,-1,0,0,2],
            [-5,0,0,-1,0,1,2,4],
            [-5,0,0,-1,0,0,1,3,4],
            [-5,-1,-1,0,0,-1,1,2,2,4],
            [-3,-1,-1,0,-1,-2,2,1,1,3,6],
            [-4,0,-1,0,-2,-3,0,-1,-1,1,2,6],
            [-5,0,0,-1,-1,-2,1,0,0,1,0,3,5],
            [-5,-2,-1,-2,-1,-3,-2,-3,-2,-1,-2,0,0,5],
            [-2,-1,0,-2,-1,-3,-2,-2,-2,-2,-2,-2,-2,2,5],
            [-6,-3,-2,-3,-2,-4,-3,-4,-3,-2,-2,-3,-3,4,2,6],
            [-2,-1,0,-1,0,-1,-2,-2,-2,-2,-2,-2,-2,2,4,2,4],
            [-4,-3,-3,-5,-4,-5,-4,-5,-5,-5,-2,-4,-5,0,1,2,-1,9],
            [0,-3,-3,-5,-3,-5,-2,-4,-4,-4,0,-4,-4,-2,-1,-1,-2,7,10],
            [-8,-2,-5,-6,-6,-7,-4,-7,-7,-5,-3,2,-3,-4,-2,-2,-6,0,0,17]
            ]
# PAM_score[長い方][短い方]で検索
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
                # PAMのスコアを使う
                # print('$'*100)
                # print('比べるもの:',amino_height[rows_counter - 2])
                # print('比べるもの:',amino_width[simple_counter - 1])
                index_a = amino_height[rows_counter - 2]
                index_b = amino_width[simple_counter - 1]
                index_a_number = PAM_amino.index(index_a)
                index_b_number = PAM_amino.index(index_b)
                # print('index_aは',index_a,'index_bは',index_b,'index_a_numberは',index_a_number,'index_b_number',index_b_number)
                if index_a_number >= index_b_number:
                    gap = PAM_score[index_a_number][index_b_number]
                else:
                    gap = PAM_score[index_b_number][index_a_number]
                # ここまで
                score_array = [left-3, top-3, diagonal + gap]
                # print("斜め",diagonal + gap,"左から", left-3, "上から",top-3)
                max_score = max(score_array)
                max_score_count = score_array.count(max_score)
                #if type(max_score) == list: 
                if max_score_count != 1: # 経路が複数ある場合
                    print(index_a, "=====", index_b, "SCORE======:", gap)
                    print("複数からの経路です", max_score, "が複数あります!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    if score_array[0] == score_array[1] == score_array[2]: #斜め、左から、上からのスコアが共に最大の時
                        number = [this_number - 1, this_number - width, this_number - width - 1]
                        arg[rows_counter - 1][simple_counter]= [max_score, number]
                    elif score_array[0] == score_array[1]: #左から、上からのスコアが共に最大の時
                        number = [this_number - 1, this_number - width]
                        arg[rows_counter - 1][simple_counter]= [max_score, number]
                    elif score_array[0] == score_array[2]: #斜め、左からのスコアが共に最大の時
                        number = [this_number - 1, this_number - width - 1]
                        arg[rows_counter - 1][simple_counter]= [max_score, number]
                    elif score_array[1] == score_array[2]: #斜め、上からのスコアが共に最大の時
                        print("--------斜め、上からのスコアが共に最大の時-------------")
                        number = [this_number - width, this_number - width - 1]
                        arg[rows_counter - 1][simple_counter]= [max_score, number]
                else: # 経路が単数の場合
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
    # print(arg)
    for a in arg:
        print(a)
    # print(max_node)
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
    check_score_and_prenode(simple_array, arg_amino)

# make_array関数を起動
make_array(sample)