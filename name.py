from opencc import OpenCC
from typing import Text

from stroke_number import get_stroke_number

class Name():
    __slots__ ="last_name", "first_name","stroke_number0", "stroke_number1", "stroke_number2", "count", "source", "gender","author", "title"

    def __init__(self, last_name:str, first_name:Text, source:str, gender:str, author:str="", title:str="") -> None:
        self.last_name = last_name
        self.stroke_number0 = get_stroke_number(last_name)
        self.stroke_number1 = get_stroke_number(first_name[0])
        self.stroke_number2 = get_stroke_number(first_name[1])
        self.count = len(first_name)
        self.source = source.replace(first_name[0], "「" + first_name[0] + "」") \
            .replace(first_name[1], "「" + first_name[1] + "」")
        self.gender = gender
        # 转回简体
        cc = OpenCC('t2s')
        self.first_name = cc.convert(first_name)
        self.author=author
        self.title=title

    def __eq__(self, other:object) -> bool:
        if not isinstance(other, Name):
            return NotImplemented
        return self.first_name == other.first_name

    def __ne__(self, other:object) -> bool:
        if not isinstance(other, Name):
            return NotImplemented
        return not self.first_name == other.first_name

    def __lt__(self, other:object) -> bool:
        if not isinstance(other, Name):
            return NotImplemented
        return self.first_name < other.first_name

    def __str__(self) -> str:
        return self.first_name + "\t" + \
               str(self.gender) + "\t" + \
               self.first_name[0] + "\t" + \
               self.first_name[1] + "\t" + \
               str(self.stroke_number1) + "\t" + str(self.stroke_number2) + "\t" + \
               self.source + "\t" + \
               self.author + "\t" + \
               self.title

    def __hash__(self) -> int:
        return hash(self.first_name)
