import pymysql
import sshtunnel

class DBConnector:
    def __init__(self):
        self.server = None
        self.conn = None
        self.cursor = None
    def db_connect(self, db_host, db_port, user_id, password, db_name):
        if self.server is None:
            self.conn = pymysql.connect(host=db_host, port=int(db_port), user=user_id, passwd=password, db=db_name, charset='utf8')
        else:
            self.conn = pymysql.connect(host=db_host, port=self.server.local_bind_port, user=user_id, passwd=password, db=db_name, charset='utf8')
        self.cursor = self.conn.cursor()
    def ssh_connect(self, ssh_host, ssh_port, ssh_id, ssh_passwd, remote_bind_addr, db_port):
        self.server=sshtunnel.SSHTunnelForwarder((ssh_host, int(ssh_port)), ssh_password=ssh_passwd, ssh_username=ssh_id, remote_bind_address=(remote_bind_addr, int(db_port)))
        self.server.start()
    def db_disconnect(self):
        self.cursor.close()
        self.conn.close()
    def ssh_disconnect(self):
        self.server.close()
    def db_connect_test(self):
        return False if (self.conn is None) else True
    def ssh_connect_test(self):
        return False if (self.server is None) else True

    def get_group_list(self, prefix):
        self.cursor.execute("select group_srl, title from {0}_member_group;".format(prefix))
        return self.cursor.fetchall()
    def get_extra_vars_list(self, prefix):
        self.cursor.execute("select column_type, column_name, column_title from {0}_member_join_form;".format(prefix))
        return self.cursor.fetchall()
    def get_all_user_list(self, prefix):
        self.cursor.execute("select ifnull(user_id, ''), ifnull(email_address, ''), ifnull(email_id, ''), ifnull(email_host, ''), ifnull(user_name, ''), ifnull(nick_name, ''), ifnull(homepage, ''), ifnull(blog, ''), ifnull(birthday, ''), ifnull(allow_mailing, ''), ifnull(allow_message, ''), ifnull(regdate, ''), ifnull(last_login, ''), ifnull(change_password_date, ''), ifnull(description, ''), ifnull(extra_vars, '') from {0}_member;".format(prefix))
        return self.cursor.fetchall()
    def get_group_user_list(self, prefix, group_srl):
        self.cursor.execute("select ifnull(user_id, ''), ifnull(email_address, ''), ifnull(email_id, ''), ifnull(email_host, ''), ifnull(user_name, ''), ifnull(nick_name, ''), ifnull(homepage, ''), ifnull(blog, ''), ifnull(birthday, ''), ifnull(allow_mailing, ''), ifnull(allow_message, ''), ifnull({0}_member.regdate, ''), ifnull(last_login, ''), ifnull(change_password_date, ''), ifnull(description, ''), ifnull(extra_vars, '') from {0}_member, {0}_member_group_member where {0}_member.member_srl = {0}_member_group_member.member_srl and {0}_member_group_member.group_srl = {1};".format(prefix, group_srl))
        return self.cursor.fetchall()
    