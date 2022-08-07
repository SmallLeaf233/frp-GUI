import os
import time
from tkinter import *
from tkinter import messagebox


class Application(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createWidget()

    def createWidget(self):
        # 输入ip
        self.labelIp = Label(self, text="本地IP")
        self.labelIp.grid(row=0, column=0, sticky=SW)
        self.ip = StringVar()
        self.entryIp = Entry(self, textvariable=self.ip)
        self.entryIp.grid(row=1, column=0)
        self.ip.set("127.0.0.1")

        # 输入端口
        self.labelPort = Label(self, text="端口")
        self.labelPort.grid(row=0, column=1, sticky=SW)
        self.port = StringVar()
        self.entryPort = Entry(self, textvariable=self.port)
        self.entryPort.grid(row=1, column=1)

        # 隧道名称
        self.labelName = Label(self, text="隧道名称")
        self.labelName.grid(row=2, column=0, sticky=SW)
        self.name = StringVar()
        self.entryName = Entry(self, textvariable=self.name)
        self.entryName.grid(row=3, column=0)

        # 隧道类型
        self.labeltyp = Label(self, text="隧道类型")
        self.labeltyp.grid(row=2, column=1, sticky=SW)
        self.typ = StringVar(self)
        self.typ.set("TCP")
        self.om01 = OptionMenu(self, self.typ, "TCP", "UDP")
        self.om01.grid(row=3, column=1)

        self.btn01 = Button(self, text="创建", command=self.establish)
        self.btn01.grid(row=4, column=0, sticky=EW)
        self.btn02 = Button(self, text="启动", command=self.run)
        self.btn02.grid(row=4, column=1, sticky=W)
        self.btn03 = Button(self, text="停止", command=self.end)
        self.btn03.grid(row=4, column=1, sticky=E)

    def establish(self):
        if self.typ.get() == "TCP":
            typ = "tcp"
        if self.typ.get() == "UDP":
            typ = "udp"
        with open("frpc.ini", "w") as f:
            list = ['[common]\n',
                    'server_addr = 【这里填服务器IP】\n',
                    'server_port = 7000\n',
                    'log_file = ./frpc.log\n',
                    'token = 【这里填密钥，如果没有将这行删除】\n'
                    '\n',
                    '[' + self.name.get() + ']\n',
                    'type = ' + typ + '\n',
                    'local_ip = ' + self.ip.get() + '\n',
                    'local_port = ' + self.port.get() + '\n',
                    'remote_port = 6002']
            f.writelines(list)

    def run(self):
        os.popen('frpc.exe')
        time.sleep(0.5)
        with open("frpc.log", "r") as f:
            self.log = str(f.readlines()[-3:])
            print(self.log)
            if "[W]" in self.log:
                os.system('taskkill /F /IM frpc.exe')
                if "port already" in self.log:
                    messagebox.showerror("启动失败", "远程端口已被使用，请改用其他端口\n\n程序已禁用自选远程端口功能，请联系小叶子")
                elif "proxy name" in self.log:
                    messagebox.showerror("启动失败", "隧道名称" + self.name.get() + "已被使用，请检查并更换一个隧道名称")
                else:
                    messagebox.showerror("启动失败", "出现了没有预料的错误，请检查日志文件frpc.log，将日志文件发给小叶子")
            else:
                messagebox.showinfo("启动成功", "您的本地地址：" + self.ip.get() + ":" + self.port.get() +
                                    "已映射到服务器地址：【这里填服务器IP】:6001")

    def end(self):
        os.system('chcp 65001')
        os.system('taskkill /F /IM frpc.exe')


if __name__ == '__main__':
    root = Tk()
    root.geometry("300x150+600+250")
    root.title("FRPGUI")
    app = Application(master=root)


    def end():
        os.system('taskkill /F /IM frpc.exe')
        root.destroy()


    root.protocol('WM_DELETE_WINDOW', end)
    root.mainloop()
