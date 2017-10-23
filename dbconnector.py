import pymysql
import sshtunnel

class DBConnector:
    def __init__(self):
        self.server = None
        self.conn = None
        self.cursor = None
    def db_connect(self, db_host, db_port, user_id, password, db_name):
        if self.server is None:
            self.conn = pymysql.connect(host=db_host, port=int(db_port), user=user_id, passwd=password, db=db_name)
        else:
            self.conn = pymysql.connect(host=db_host, port=self.server.local_bind_port, user=user_id, passwd=password, db=db_name)
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
        
    