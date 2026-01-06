class StrToInt:
    @staticmethod
    def str_to_int(s: str) -> int:
        return int(s)
if __name__ == '__main__':
    s="123"
    print(type(StrToInt.str_to_int(s)))