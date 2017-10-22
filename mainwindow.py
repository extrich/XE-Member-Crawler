import tkinter as tk
from tkinter import ttk
import pymysql
import sshtunnel
import time
import xlsxwriter
import os

class main_window :
    def __init__(self):
        self.window = tk.Tk()
        self.notebook_tab = ttk.Notebook(self.window)
        self.frame_db = ttk.Frame(self.notebook_tab) #DB연결설정 탭
        self.frame_feild = ttk.Frame(self.notebook_tab) #기본변수 탭
        self.frame_extra = ttk.Frame(self.notebook_tab) #확장변수 탭

        #DB탭 변수
        self.db_setting_names = ["DB 호스트", "포트번호", "DB 이름", "접두어", "DB 접속ID", "비밀번호"]
        self.db_setting_values = []
        self.use_ssh_tunnel = tk.BooleanVar();
        self.ssh_setting_names = ["SSH 호스트", "포트번호", "SSH 접속ID", "비밀번호", "원격 바인딩주소", "DB 포트번호"]
        self.ssh_setting_values = []

        #기본필드탭 변수
        self.column_names = ["member_srl", "user_id", "email_address", "password", "email_id", "email_host", "user_name", "nick_name", "find_account_question", "find_account_answer", "homepage", "blog", "birthday", "allow_mailing", "allow_message", "denied", "limit_date", "regdate", "last_login", "change_password_date", "is_admin", "description", "extra_vars", "list_order"]
        self.column_values = []
        
        #데이터베이스 탭
        self.db_setting_frame = tk.LabelFrame(self.frame_db, text="DB연결 설정")
        for i in range(len(self.db_setting_names)):
            tk.Label(self.db_setting_frame, text=self.db_setting_names[i]).grid(row=i, column=0, sticky='W')
            self.db_setting_values.append(tk.Entry(self.db_setting_frame))
            self.db_setting_values[i].grid(row=i, column=1)
        self.db_setting_frame.grid(row=0, sticky='W')
        tk.Checkbutton(self.frame_db, text="SSH터널 사용", variable=self.use_ssh_tunnel, command=self.toggle_ssh_tunnel).grid(row=1, sticky='W')
        
        self.ssh_setting_frame = tk.LabelFrame(self.frame_db, text="SSH터널 설정")
        for i in range(len(self.ssh_setting_names)):
            tk.Label(self.ssh_setting_frame, text=self.ssh_setting_names[i]).grid(row=i, column=0, sticky='W')
            self.ssh_setting_values.append(tk.Entry(self.ssh_setting_frame, state="readonly"))
            self.ssh_setting_values[i].grid(row=i, column=1)
        self.ssh_setting_frame.grid(row=2, sticky='W')
        tk.Button(self.frame_db, text="DB연결 테스트", command=self.db_connect_test).grid(row=3, sticky='W')
        tk.Button(self.frame_db, text="SSH터널 테스트", command=self.ssh_connect_test).grid(row=3, sticky='E')


        #기본필드 탭
        self.column_select_frame = tk.LabelFrame(self.frame_feild, text="결과에 포함시킬 변수")
        for i in range(len(self.column_names)):
            self.column_values.append(tk.BooleanVar())
            tk.Checkbutton(self.column_select_frame, text=self.column_names[i], variable=self.column_values[i], command=self.toggle_extra_vars).grid(row=i%12, column=i//12, sticky='W')
        self.column_select_frame.grid(row=0)

        #확장변수 탭
        self.



        #노트북탭에 개별 프레임 삽입
        self.notebook_tab.add(self.frame_db, text="DB연결 설정")
        self.notebook_tab.add(self.frame_feild, text="기본변수")
        self.notebook_tab.add(self.frame_extra, text="확장변수", state="disabled")
        self.notebook_tab.pack()
        
        #메인루프
        self.window.mainloop()

    def ssh_tunnel_on(self):
        pass
    def ssh_tunnel_off(self):
        pass
    def ssh_connect_test(self):
        pass
    def db_connect_on(self):
        pass
    def db_connect_off(self):
        pass
    def db_connect_test(self):
        pass
    def toggle_ssh_tunnel(self):
        #SSH터널 옵션 토글
        for entry in self.ssh_setting_values:
            if self.use_ssh_tunnel.get():
                entry.configure(state="normal")
            else:
                entry.configure(state="readonly")
    def toggle_extra_vars(self):
        #확장변수 탭 토글
        if self.column_values[22].get():
            self.notebook_tab.tab(self.frame_extra, state="normal")
        else:            
            self.notebook_tab.tab(self.frame_extra, state="disabled")
        

#메인루프 실행
main_window()
