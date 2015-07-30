"""
##################################################################
launch FTP getfile function with a reusable GUI class; uses 
os.chdir to goto target local dir; runs getfile.getfile in a thread
to allow more than one to be running at once (avoid blocking)

-supports both user and anonymous FTP as currently coded
- not 100 percent thread safe
##################################################################
"""

from tkinter import Tk, mainloop
from tkinter.messagebox import showinfo
import getfile
import os
import sys
import _thread
from PP4E.Internet.Sockets.form import Form


class FtpForm(Form):

    def __init__(self):
        root = Tk()
        root.title(self.title)
        labels = ["Server Name", "Remote Dir", "File Name",
                  "Local Dir", "User Name?", "Password"]
        Form.__init__(self, labels, root)
        self.mutex = thread.allocate_lock()
        self.threads = 0

    def transfer(self, filename, servername, remotedir, userinfo):
        try:
            self.do_transfer(filename, servername, remotedir, userinfo)
            print("%s of %s successful" % (self.mode, filename))
        except:
            print("%s of %s has failed" % (self.mode, filename), end=" ")
            print(sys.exec_info()[0], sys.exec_info()[1])
        self.mutex.acquire()
        self.threads -= 1
        self.mutex.release()

    def onSubmit(self):
        Form.onSubmit(self)
        localdir = self.content["Local Dir"].get()
        remotedir = self.content["Remote Dir"].get()
        servername = self.content["Server Name"].get()
        filename = self.content["File Name"].get()
        username = self.content["User Name?"].get()
        password = self.content["Password"].get()

        if username and password:
            userinfo = (username, password)
        if localdir:
            os.chdir(localdir)
        self.mutex.acquie()
        self.threads += 1
        self.mutex.release()

        ftpargs = (filename, servername, remotedir, userinfo)
        _thread.start_new_thread(self.transfer, ftpargs)
        showinfo(self.title, "%s of %s started" % (self.mode, filename))

    def onCancel(self):
        if self.threads == 0:
            Tk.quit()
        else:
            showinfo(self.title, "Cannot exit: %d threads running" %
                     self.threads)


class FtpGetfileForm(FtpForm):
    title = "FtpGetfileGUI"
    mode = "Download"

    def do_transfer(self, filename, servername, remotedir, userinfo):
        getfile.getfile(
            filename, servername, remotedir, userinfo, verbose=False, refetch=True)


if __name__ == "__main__":
    FtpGetfileGUI()
    mainloop()
