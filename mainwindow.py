import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

import dbconnector as dbc
import dataexporter as dtx

class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('XE 회원정보 DB 크롤러')
        self.notebook_tab = ttk.Notebook(self.window)
        self.frame_db = ttk.Frame(self.notebook_tab) #DB연결설정 탭
        self.frame_feild = ttk.Frame(self.notebook_tab) #기본변수 탭
        self.frame_extra = ttk.Frame(self.notebook_tab) #확장변수 탭
        self.frame_output = ttk.Frame(self.notebook_tab) #내보내기 탭
        self.dbconnector = dbc.DBConnector()
        self.dataexporter = dtx.DataExporter()

        #DB탭 변수
        self.db_setting_names = ["DB 호스트", "포트번호", "DB 접속ID", "비밀번호", "DB 이름", "접두어"]
        self.db_setting_values = []
        self.use_ssh_tunnel = tk.BooleanVar()
        self.ssh_setting_names = ["SSH 호스트", "포트번호", "SSH 접속ID", "비밀번호", "원격 바인딩주소", "바인딩 포트"]
        self.ssh_setting_values = []

        #기본필드탭 변수
        self.column_names = ["ID", "이메일 주소", "이메일 ID", "이메일 호스트", "이름", "닉네임", "홈페이지", "블로그", "생일", "메일링가입", "메시지허용", "관리자", "승인거부", "거부일자", "가입일자", "최종로그인", "비밀번호 변경일", "요약", "확장변수"]
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
            tk.Checkbutton(self.column_select_frame, text=self.column_names[i], variable=self.column_values[i], command=self.toggle_extra_vars).grid(row=i%round((len(self.column_names)/2)), column=i//round((len(self.column_names)/2)), sticky='W')
        self.column_select_frame.grid(row=0)

        #확장변수 탭
        tk.Label(self.frame_extra, text="출력하지 않을 확장변수").pack()
        self.ban_list = ScrolledText(self.frame_extra, undo=True, width=40)
        self.ban_list.pack()

        #내보내기 탭
        self.output_dir_select_frame = tk.LabelFrame(self.frame_output, text="경로설정")
        tk.Label(self.output_dir_select_frame, text="파일이름").grid(row=0, column=0)
        self.output_file_name = tk.Entry(self.output_dir_select_frame)
        self.output_file_name.grid(row=0, column=1)
        self.output_dir_select_frame.grid(row=0, sticky='W')

        self.output_file_frame = tk.LabelFrame(self.frame_output, text="내보내기")
        tk.Button(self.output_file_frame, text=".xlsx파일로 내보내기", command=self.output_xlsx).pack()
        self.output_file_frame.grid(row=1, sticky='W')


        #노트북탭에 개별 프레임 삽입
        self.notebook_tab.add(self.frame_db, text="DB연결 설정")
        self.notebook_tab.add(self.frame_feild, text="기본변수")
        self.notebook_tab.add(self.frame_extra, text="확장변수", state="disabled")
        self.notebook_tab.add(self.frame_output, text="내보내기")
        self.notebook_tab.pack()

        #메인루프
        self.window.mainloop()

    def ssh_tunnel_on(self):
        self.dbconnector.ssh_connect(self.ssh_setting_values[0].get(), self.ssh_setting_values[1].get(), self.ssh_setting_values[2].get(), self.ssh_setting_values[3].get(), self.ssh_setting_values[4].get(), self.ssh_setting_values[5].get())
    def ssh_tunnel_off(self):
        self.dbconnector.ssh_disconnect()
    def ssh_connect_test(self):
        self.ssh_tunnel_on()
        messagebox.showinfo("SSH터널 연결 테스트", "성공" if self.dbconnector.ssh_connect_test() else "실패")
        self.ssh_tunnel_off()

    def db_connect_on(self):
        if self.use_ssh_tunnel.get():
            self.ssh_tunnel_on()
        self.dbconnector.db_connect(self.db_setting_values[0].get(), self.db_setting_values[1].get(), self.db_setting_values[2].get(), self.db_setting_values[3].get(), self.db_setting_values[4].get())
    def db_connect_off(self):
        self.dbconnector.db_disconnect()
        if self.use_ssh_tunnel.get():
            self.ssh_tunnel_off()
    def db_connect_test(self):
        self.db_connect_on()
        messagebox.showinfo("DB연결 테스트", "성공" if self.dbconnector.db_connect_test() else "실패")
        self.db_connect_off()

    def output_xlsx(self):
        self.db_connect_on()
        self.dataexporter.open_xlsx(self.output_file_name.get() + ".xlsx")
        #전체회원 구겨넣기
        self.dataexporter.insert_xlsx_worksheet("전체회원", self.dataexporter.get_aligned_user_list(self.column_names, self.column_values, self.dbconnector.get_extra_vars_list(self.db_setting_values[5].get()), self.ban_list.get('1.0', 'end-1c').splitlines(), self.dbconnector.get_all_user_list(self.db_setting_values[5].get())))
        group_list = self.dbconnector.get_group_list(self.db_setting_values[5].get())
        #그룹별로 회원 구겨넣기
        for group in group_list:
            self.dataexporter.insert_xlsx_worksheet(group[1], self.dataexporter.get_aligned_user_list(self.column_names, self.column_values, self.dbconnector.get_extra_vars_list(self.db_setting_values[5].get()), self.ban_list.get('1.0', 'end-1c').splitlines(), self.dbconnector.get_group_user_list(self.db_setting_values[5].get(), group[0])))
        self.dataexporter.close_xlsx()
        self.db_connect_off()

    def toggle_ssh_tunnel(self):
        #SSH터널 옵션 토글
        for entry in self.ssh_setting_values:
            if self.use_ssh_tunnel.get():
                entry.configure(state="normal")
            else:
                entry.configure(state="readonly")
    def toggle_extra_vars(self):
        #확장변수 탭 토글
        if self.column_values[-1].get():
            self.notebook_tab.tab(self.frame_extra, state="normal")
        else:
            self.notebook_tab.tab(self.frame_extra, state="disabled")

#메인루프 실행
MainWindow()
