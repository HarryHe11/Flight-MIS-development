import sys
from PyQt5 import QtCore, QtWidgets, QtCore
import pymysql
from menu import Ui_MainWindow as Menu_Ui
from login import Ui_MainWindow as Login_Ui
from operate import Ui_MainWindow as Operate_Ui
from add_dialog import Ui_MainWindow as Add_Ui
from PyQt5.QtWidgets import QMessageBox,QInputDialog

def get_connection():
    conn = pymysql.connect(
        host='127.0.0.1',  # 连接主机, 默认127.0.0.1
        user='root',  # 用户名
        passwd='h20011126',  # 密码
        port=3306,  # 端口，默认为3306
        db='mis_db',  # 数据库名称
        charset='utf8'  # 字符编码
    )
    return conn

# 开始菜单窗口
class MenuWindow(QtWidgets.QMainWindow, Menu_Ui):
    switch_window1 = QtCore.pyqtSignal()
    switch_window2 = QtCore.pyqtSignal()
    def __init__(self):
        super(MenuWindow, self).__init__()
        self.setupUi(self)
        self.manageButton.clicked.connect(self.goLogin)
        self.queryButton.clicked.connect(self.goOperate)
    def goLogin(self):
        print("manageButton clicked!!")
        self.switch_window1.emit()
    def goOperate(self):
        print("queryButton clicked!!")
        self.switch_window2.emit()


# 登录窗口
class LoginWindow(QtWidgets.QMainWindow, Login_Ui):
    switch_window1 = QtCore.pyqtSignal()  # 跳转操作
    switch_window2 = QtCore.pyqtSignal()  # 跳转回主菜单
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setupUi(self)
        self.okButton.clicked.connect(self.ok)
        self.cancelButton.clicked.connect(self.cancel)

    def ok(self):
        username = self.userText.text()
        password = self.pwdText.text()
        # 创建数据库连接
        conn = get_connection()
        # 生成游标对象 cursor
        cursor = conn.cursor()
        if (cursor.execute("SELECT * FROM user WHERE u_name='%s' AND u_password='%s'" % (username, password))):
            QMessageBox.information(self, username,"登陆成功",QMessageBox.Yes)
            cursor.close()
            conn.close()
            print("switch to operate")
            self.switch_window1.emit()
        else:
            QMessageBox.warning(self, "警告", "密码错误", QMessageBox.Cancel)
            cursor.close()
            conn.close()

    def cancel(self):
        print("switch to menu")
        self.switch_window2.emit()


# 操作窗口
class OperateWindow(QtWidgets.QMainWindow, Operate_Ui):
    switch_window1 = QtCore.pyqtSignal()
    def __init__(self):
        super(OperateWindow, self).__init__()
        self.setupUi(self)
        self.exitButton.clicked.connect(self.exit)
        self.pushButton.clicked.connect(self.query)
        self.pushButton_3.clicked.connect(self.goAdd)
        self.pushButton_4.clicked.connect(self.goCha)
        self.pushButton_5.clicked.connect(self.goDel)
    def query(self): #查询
        print("querying")
        self.tableWidget.clearContents()
        # 数据库连接对象
        conn = get_connection()
        # 游标对象
        cur = conn.cursor()
        # 查询的sql语句
        sql = "SELECT * FROM flight"
        cur.execute(sql)
        # 获取查询到的数据, 是以二维元组的形式存储的, 所以读取需要使用 data[i][j] 下标定位
        data = cur.fetchall()
        # 遍历二维元组, 将 id 和 name 显示到界面表格上
        x = 0
        for i in data:
            y = 0
            for j in i:
                self.tableWidget.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
                y = y + 1
            x = x + 1
        cur.close()
        conn.close()
        print("querying done")
    def goAdd(self):
        self.switch_window1.emit()
    def goCha(self):
        print("change BUTTON CLICKED")
        conn = get_connection()
        print("connection success")
        # 游标对象
        fid, ok = QInputDialog.getText(None, "修改航班信息", "请输入待修改航班的航班号", text="F006")
        field, ok = QInputDialog.getText(None, "修改航班信息", "请输入待修改字段", text="起点")
        value, ok = QInputDialog.getText(None, "修改航班信息", "请输入修改值", text="上海")
        cur = conn.cursor()

        if field == "起点":
            sql = "UPDATE flight SET f_src = '%s' WHERE f_id = '%s'" % (value,fid)
            if (cur.execute(sql)):
                conn.commit()
                print("success")
                QMessageBox.information(self, "信息", "修改数据成功", QMessageBox.Yes)
                cur.close()
                conn.close()

    def goDel(self):
        fid,ok = QInputDialog.getText(None, "删除航班信息", "请输入待删除航班的航班号", text="F006")
        conn = get_connection()
        # 游标对象
        cur = conn.cursor()
        # 查询的sql语句
        sql = "delete from flight where f_id='%s'" % (fid,)

        if(cur.execute(sql)):
            conn.commit()
            print("success")
            QMessageBox.information(self, "信息", "删除数据成功", QMessageBox.Yes)
            cur.close()
            conn.close()

    def exit(self): #查询退出
        sys.exit(0)

# 添加数据窗口
class AddWindow(QtWidgets.QMainWindow, Add_Ui):
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        super(AddWindow, self).__init__()
        self.setupUi(self)
        self.lineEdit_1.setText("F006")
        self.lineEdit_2.setText('南京')
        self.lineEdit_3.setText('北京')
        self.lineEdit_4.setText('2022-05-12')
        self.lineEdit_5.setText('13:30')
        self.lineEdit_6.setText('15:20')
        self.lineEdit_7.setText( '55')
        self.lineEdit_8.setText('999')
        self.lineEdit_9.setText('5')
        self.lineEdit_10.setText('1')
        self.lineEdit_11.setText('国航')
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.cancel)

    def add(self):
        print("OK BUTTON CLICKED")
        v1 = self.lineEdit_1.text()
        v2 = self.lineEdit_2.text()
        v3 = self.lineEdit_3.text()
        v4 = self.lineEdit_4.text()
        v5 = self.lineEdit_5.text()
        v6 = self.lineEdit_6.text()
        v7 = self.lineEdit_7.text()
        v8 = self.lineEdit_8.text()
        v9 = self.lineEdit_9.text()
        v10 = self.lineEdit_10.text()
        v11 = self.lineEdit_11.text()
        values=(v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11)
        print("values got")
        print(values)

        conn = get_connection()
        print("connection success")
        # 游标对象
        cur = conn.cursor()
        # 查询的sql语句
        sql = "insert into " \
              "flight(f_id,f_src,f_des,f_date,f_start_time,f_end_time,f_remain_seats,f_fares,f_discount_nums,f_discount,f_subordinate_company) " \
              "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        if(cur.execute(sql,values)):
            conn.commit()
            print("success")
            QMessageBox.information(self, "信息", "添加数据成功", QMessageBox.Yes)
            cur.close()
            conn.close()
            self.switch_window.emit()

    def cancel(self):
        self.switch_window.emit()



# 页面的跳转
class Controller:
    def __init__(self):
        self.menu = MenuWindow()#菜单窗口
        self.login = LoginWindow()#登录窗口
        self.operate = OperateWindow()#操作窗口
        self.add = AddWindow()#增加数据对话框窗口
    def show_menu(self):
        self.menu.switch_window1.connect(self.show_login) #跳转登陆界面
        self.menu.switch_window2.connect(self.show_operate) #跳转操作界面
        self.menu.show()
        self.login.close()
        self.operate.close()
    def show_login(self):
        self.login.switch_window1.connect(self.show_operate)#跳转操作界面
        self.login.switch_window2.connect(self.show_menu)#跳转菜单界面
        self.login.show()
        self.menu.close()
        self.operate.close()
    def show_operate(self):
        self.operate.switch_window1.connect(self.show_add)#跳转数据对话框界面
        self.menu.close()
        self.login.close()
        self.add.close()
        self.operate.show()
    def show_add(self):
        self.add.switch_window.connect(self.show_operate)#跳转操作界面
        self.operate.close()
        self.add.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_menu()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
