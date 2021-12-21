from typing import List, Set, Text
from pypinyin import lazy_pinyin, Style
from name_set import Name

#音调组合
not_allowed_yindiao = {"111", "133","233","333", "344","441"}
#结尾闭口音
not_allowed_bikouyin = {"eng", "in", "ing", "uo", "uei", "uai", "ui","uan", "ue", "un", "uen", "ueng", "ong", "iong"}
def check_name_duyin(name:Name, dislike_pinyin:Set[str], check_l_n:bool)-> bool:
    nameStr:Text = f"{name.last_name}{name.first_name}"
    duyin_tone3 = lazy_pinyin(nameStr, style=Style.TONE3, neutral_tone_with_five=True, strict=False)
    duyin_normal = lazy_pinyin(nameStr, style=Style.NORMAL)
    duyin_initals = lazy_pinyin(nameStr, style=Style.INITIALS, strict=False)
    first_name_initals:List[Text] = lazy_pinyin(name.first_name)
    
    # #平仄规则
    if f"{duyin_tone3[0][-1]}{duyin_tone3[1][-1]}{duyin_tone3[2][-1]}" in not_allowed_yindiao:
        return False
    #姓与名的第一个字读音不能相同    
    if duyin_normal[0] == duyin_normal[1]:
        return False
    #避免闭口音结尾
    for bikouyin in not_allowed_bikouyin:
        if duyin_normal[2].endswith(bikouyin):
            return False
    #避免平舌卷舌交错
    pinshe = {"z", "c", "s"}
    juanshe = {"zh", "ch", "sh", "r"}
    not_allowd_shengmu = set()
    for a in pinshe:
        for b in juanshe:
            not_allowd_shengmu.add(f"{a}:{b}")
            not_allowd_shengmu.add(f"{b}{a}")

    shengmu = f"{duyin_initals[0]}{duyin_initals[1]}{duyin_initals[2]}"
    for x in not_allowd_shengmu:
        if(shengmu.endswith(x) or shengmu.startswith(x)):
            return False
    #过滤不想要的读音
    if duyin_normal[1] in dislike_pinyin or duyin_normal[2] in dislike_pinyin:
        return False
    #过滤声母中的l和n
    if check_l_n:
        for i in first_name_initals:
            if i in {"l", "n"}:
                return False

    return True