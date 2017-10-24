import xlsxwriter as xlsx
import re
from phpserialize import *

class DataExporter:
    def __init__(self):
        self.xlsx_workbook = None
        self.xlsx_worksheets = []

    def get_aligned_user_list(self, column_names, column_values, extra_vars, user_list):
        result = []
        header = []

        #기본필드 머리 삽입
        for i in range(len(column_names[:-1])):
            if column_values[i].get():
                header.append(column_names[i])
        #확장필드 머리 삽입
        if column_values[-1].get():
            for i in range(len(extra_vars)):
                header.append(extra_vars[i][2]) #삽입할 확장변수 여기서 체크
        result.append(header)

        #몸통 삽입
        for i in range(len(user_list)):
            body = []
            #기본필드 몸통 삽입
            for j in range(len(user_list[i][:-1])):
                if column_values[j].get():
                    body.append(user_list[i][j])
            #확장필드 몸통 삽입
            if column_values[-1].get():
                extra_var = unserialize(user_list[i][-1].encode(), decode_strings=True, object_hook=phpobject)._asdict()
                for j in range(len(extra_vars)):
                    #확장필드가 주소 형태라면
                    if re.match(r'.*zip$', extra_vars[j][0]) is not None:
                        body.append(extra_var[extra_vars[j][1]][1]+' '+extra_var[extra_vars[j][1]][2]+' '+extra_var[extra_vars[j][1]][4]+' '+extra_var[extra_vars[j][1]][3] if (extra_vars[j][1] in extra_var) else '')
                    #주소 이외의 다른 형태라면
                    else:
                        body.append(extra_var[extra_vars[j][1]] if (extra_vars[j][1] in extra_var) else '')
            result.append(body)
        
        return result

    def open_xlsx(self, file_name):
        self.xlsx_workbook = xlsx.Workbook(file_name)
