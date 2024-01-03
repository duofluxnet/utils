from math import pow
combo_dict = {
    "numeric":"0123456789",
    "alpha":"ABCDEFGHIJKLMNOPQRTSUVWXYZ",
}
uniq_sort_char_set = sorted(set(list("".join(combo_dict.values()))))
combs = pow(len(uniq_sort_char_set), 6)

print("Working with char set ({} elements): {}".format(len(uniq_sort_char_set), "".join(uniq_sort_char_set)))
print("Resulting combination size of {}^6 chars = {:,.0f} words.".format(len(uniq_sort_char_set), combs))

word_vector_list = [
    set(uniq_sort_char_set.copy()),
    set(uniq_sort_char_set.copy()),
    set(uniq_sort_char_set.copy()),
    set(uniq_sort_char_set.copy()),
    set(uniq_sort_char_set.copy()),
    set(uniq_sort_char_set.copy()),
]

f_out = open("/tmp/pwd.txt", "w")
count = 0
for i_0 in word_vector_list[0]:
    for i_1 in word_vector_list[1]:
        f_out.flush()
        print("{:,.0f} / {:,.0f} = {:.2f}%".format(count, combs, count / combs * 100))
        for i_2 in word_vector_list[2]:
            for i_3 in word_vector_list[3]:
                for i_4 in word_vector_list[4]:
                    for i_5 in word_vector_list[5]:
                        print("HW" + i_0 + i_1 + i_2 + i_3 + i_4 + i_5, end='\n', file=f_out)
                        count += 1

f_out.close()