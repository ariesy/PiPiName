from config import name_source, name_source_dict, last_name, dislike_words, \
    min_stroke_count, max_stroke_count, allow_general, name_validate, gender, \
    check_name, check_name_resource, author, use_wuge, use_sancai,max_stroke_total, dislike_pinyin, \
    check_l_n
from name_set import check_resource, get_source
from wuge import check_wuge_config, get_stroke_list
from duyin import check_name_duyin


def contain_bad_word(first_name:str) ->bool:
    for word in first_name:
        if word in dislike_words:
            return True
    return False


if len(check_name) == 3:
    # 查看姓名配置
    check_wuge_config(check_name)
    if check_name_resource:
        check_resource(check_name)
    print(">>输出完毕")
else:
    # 起名
    names = list()
    filename = f"names-{name_source_dict[name_source]}-{author}.txt" 
    with open(filename, ''"w+", encoding='utf-8') as f:
        for i in get_source(name_source, name_validate, get_stroke_list(last_name, allow_general, use_sancai, use_wuge), last_name, author):
            if i.stroke_number1 < min_stroke_count or i.stroke_number1 > max_stroke_count or \
                    i.stroke_number2 < min_stroke_count or i.stroke_number2 > max_stroke_count or \
                    i.stroke_number1 + i.stroke_number2 + i.stroke_number0 > max_stroke_total:
                # 笔画数过滤
                continue
            if name_validate and gender != "" and i.gender != gender and i.gender != "双" and i.gender != "未知":
                # 性别过滤
                continue
            if contain_bad_word(i.first_name):
                # 不喜欢字过滤
                continue
            if(not check_name_duyin(i, dislike_pinyin, check_l_n)):
                continue
            names.append(i)
        print(">>输出结果...")
        names.sort()
        for i in names:
            f.write(last_name + str(i) + "\n")
        print(f">>输出完毕，请查看「{filename}」文件")
