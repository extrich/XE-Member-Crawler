import tkinter as tk
from tkinter import ttk

class main_window :
    def __init__(self):
        self.window = tk.Tk()
        self.notebook_tab = ttk.Notebook(self.window)
        self.frame_db = ttk.Frame(self.notebook_tab)
        self.frame_feild = ttk.Frame(self.notebook_tab)
        self.frame_extra = ttk.Frame(self.notebook_tab)

        self.column_names = ["member_srl", "user_id", "email_address", "password", "email_id", "email_host", "user_name", "nick_name", "find_account_question", "find_account_answer", "homepage", "blog", "birthday", "allow_mailing", "allow_message", "denied", "limit_date", "regdate", "last_login", "change_password_date", "is_admin", "description", "extra_vars", "list_order"]
        self.column_values = []
        #데이터베이스 탭



        #기본필드 탭

        self.column_select_frame = tk.LabelFrame(self.frame_feild, text="결과에 포함시킬 변수")
        for i in range(24):
            self.column_values.append(tk.BooleanVar())
            tk.Checkbutton(self.column_select_frame, text=self.column_names[i], variable=self.column_values[i], command=self.select_column).grid(row=i%12, column=i//12, sticky='W')

        self.column_select_frame.grid(row=1)



        #노트북탭에 개별 프레임 삽입
        self.notebook_tab.add(self.frame_db, text="데이터베이스 연결")
        self.notebook_tab.add(self.frame_feild, text="기본필드")
        self.notebook_tab.add(self.frame_extra, text="확장변수")
        self.notebook_tab.pack()
        
        #메인루프
        self.window.mainloop()

    def select_column(self):
        print(self.column_values[3].get())

#메인루프 실행
main_window()
