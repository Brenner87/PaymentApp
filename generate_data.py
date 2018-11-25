import random
import string
import sqlite3
from collections import OrderedDict




def main():
    table_name='USER_DATA'
    my_gen = generateTable()
    data=my_gen.generateTable(100)
    print(data)



class generateTable:
    def __init__(self, row_number=None):
        self.maxLen = 0
        self.columns = {'first_name': self.generateName,
                        'last_name': self.generateName,
                        'age': self.generateAge,
                        'post_code': self.generatePostCode,
                        'phone': self.generatePhone,
                        'email': self.generateMail}
        self.columns = OrderedDict(sorted(self.columns.items(), reverse=True, key=lambda t: t[0]))
        if row_number:
            table = self.generateTable(row_number)
            self.outputTable(table)

    def generateName(self, min_lat=3, max_lat=12):
        n = random.randrange(min_lat, max_lat)
        result = (random.choice(string.ascii_lowercase) for i in range(n))
        return ''.join(result)

    def generateAge(self, min_age=6, max_age=110):
        return random.randint(min_age, max_age)

    def generatePostCode(self, min_num=3, max_num=5):
        n = random.randrange(min_num, max_num)
        result = (random.choice(string.digits) for i in range(n))
        return ''.join(result)

    def generatePhone(self, dig_num=7, code_num=3):
        if dig_num < 6:
            print('minimal phone digits number should be 5')
            dig_num = 6
        cont_code = random.choice(string.digits)
        op_code = ''.join((random.choice(string.digits) for i in range(code_num)))
        main_phone = ''.join((random.choice(string.digits) for i in range(dig_num)))
        str_fmt = '+{}({}){}-{}-{}'
        return str_fmt.format(cont_code, op_code, main_phone[0:3], main_phone[3:5], main_phone[5:dig_num])

    def generateMail(self, first_name=None, last_name=None):
        possible_boxes = ['gmail.com', 'mail.ru', 'yahoo.com', 'ukr.net', 'rambler.ru', 'freemail.com']
        mail = random.choice(possible_boxes)
        box = '{}_{}@{}'.format(first_name, last_name, mail)
        self.maxLen = (self.maxLen, len(box))[self.maxLen < len(box)]
        return box

    def generateRow(self):
        row = {}
        for key, value in self.columns.items():
            if key == 'email':
                row[key] = value(first_name=row['first_name'], last_name=row['last_name'])
            else:
                row[key] = value()
        # row=dict((key,value()) for key,value in self.columns.items())
        return row

    def generateTable(self, row_number):
        self.data = [self.generateRow() for i in range(row_number)]
        return self.data

    def outputRow(self, row):
        a = str(self.maxLen)
        fmt_string = '| '
        empt_string = '| '
        for i in self.columns.keys():
            fmt_string += '{' + i + ': <' + a + '} | '
            empt_string += ' ' * self.maxLen + ' | '
        row_out = (fmt_string).format(**row)
        # print ('_'*(len(row_out)-1))
        # print (empt_string)
        print(row_out)
        print(empt_string)
        print('|{}|'.format(chr(175) * (len(row_out) - 3)))

    def outputHeader(self, ):
        a = str(self.maxLen)
        fmt_string = '| '
        empt_string = '| '
        for i in range(len(self.columns.keys())):
            fmt_string += '{' + str(i) + ': <' + a + '} | '
            empt_string += ' ' * self.maxLen + ' | '
        row_out = (fmt_string).format(*self.columns.keys())
        print('_' * (len(row_out) - 1))
        print(empt_string)
        print(row_out)
        print(empt_string)
        print('|{}|'.format(chr(175) * (len(row_out) - 3)))

    def outputTable(self, table):
        self.outputHeader()
        [self.outputRow(i) for i in table]


if __name__ == '__main__':
    main()
