class IntToStringConverter:

    def convert(self, number):
        if isinstance(number, int):
            return str(number)
        else:
            raise ValueError("输入的值不是整数类型")


