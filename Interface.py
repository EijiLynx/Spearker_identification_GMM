from preptime import Ui_MainWindow
import sys
from test import testing, create_model
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer, QThreadPool, QRunnable, pyqtSlot
import pyaudio
import wave

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
seconds = 5
fs = 44100  # Record at 44100 samples per second
p = pyaudio.PyAudio()  # Create an interface to PortAudio
frames = []  # Initialize array to store frames

Words = ["SHE SELLS SEA SHELLS BY THE SEASHORE",
         "WHICH WITCH IS WHICH",
         "HOW MUCH WOULD A WOODCHUCK CHUCK, IF A WOODCHUCK COULD CHUCK WOOD",
         "I SAW A SAW THAT COULD OUT SAW ANY OTHER SAW I EVER SAW",
         "BETTY BOUGHT A BIT OF BUTTER BUT THE BIT OF BUTTER WAS TOO BITTER",
         ""]

k = 0
n = 0
save_file_name = None
name = ""


class Recordings(QRunnable):
    @pyqtSlot()
    def run(self):
        global k, n
        global save_file_name, name

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        # Store data in chunks for 3 seconds
        if k == 0:
            for i in range(0, int(fs / chunk * seconds)):
                data = stream.read(chunk)
                frames.append(data)
            if n == 5:
                n = 0
                frames.clear()
            else:
                self.output_file()

        else:
            while k == 2:
                for i in range(0, int(fs / chunk * 2)):
                    data = stream.read(chunk)
                    frames.append(data)
                self.output_file()

    def output_file(self):
        global save_file_name
        if save_file_name is not None:
            wf = wave.open(save_file_name, 'wb')
            with open("names.txt", 'a') as f:
                f.write((name + "-sample" + str(n) + ".wav") + '\n')
        else:
            wf = wave.open('testing.wav', 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
        frames.clear()


class Mywindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(Mywindow, self).__init__(parent)
        self.setupUi(self)

        self.threadpool = QThreadPool()

        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_lcd)
        self.s = 0

        self.Stop_btn.setDisabled(True)
        self.testing_btn.clicked.connect(self.Testing_main_page)
        self.create_btn.clicked.connect(self.Creating_page)
        self.close_btn.clicked.connect(self.Closing)
        self.live_test_btn.clicked.connect(self.livetest_page)
        self.gender_id_btn.clicked.connect(self.genderid_page)
        self.test_test_btn.clicked.connect(self.Testing_page)
        self.Rec_btn.clicked.connect(self.rec_start1)
        self.Rec_2_btn.clicked.connect(self.rec_start2)
        self.Rec_3_btn.clicked.connect(self.rec_start3)
        self.Rec_4_btn.clicked.connect(self.pre_record)
        self.Stop_btn.clicked.connect(self.btn_stop)
        self.Rec_btn.clicked.connect(self.threaddding)
        self.Rec_3_btn.clicked.connect(self.threaddding)
        self.Rec_2_btn.clicked.connect(self.threaddding)
        self.create_model_btn.clicked.connect(self.model_create)
        self.Starting_point.clicked.connect(self.threaddding)
        self.Starting_point.clicked.connect(self.namings)
        self.train_model_btn.clicked.connect(self.train)
        self.train_model_btn.setDisabled(True)
        self.tempo.clicked.connect(self.Timer_timestop)

        self.label.hide()
        self.Many_left_lb.hide()
        self.clock.hide()
        self.Starting_point.hide()
        self.widget_29.hide()

    def timer_lcd(self):
        global k, n
        if k == 2:
            self.s += 1
        else:
            self.s -= 1
        if not self.Rec_btn.isEnabled():
            self.Timer_time.display(self.s)
        elif not self.Rec_2_btn.isEnabled():
            self.Timer_time2.display(self.s)
        elif not self.Rec_3_btn.isEnabled():
            self.Timer_time3.display(self.s)
        elif not self.create_model_btn.isEnabled():
            self.clock.display(self.s)

        print(self.s)

        if k == 2 and self.s >= 2 and self.s % 2 == 0:
            self.textBrowser_3.setText("Detected As :\n" + testing("speaker-models/"))
        else:
            if self.s == 0:
                if not self.Rec_btn.isEnabled():
                    self.textBrowser_2.setText("Detected As :\n" + testing("speaker-models/"))
                    self.Timer_timestop()
                elif not self.create_model_btn.isEnabled():
                    n += 1
                    self.s = 7
                    self.Starting_point.click()
                elif not self.Rec_3_btn.isEnabled():

                    self.pre_record()
                    self.Timer_timestop()

    def Timer_timestop(self):
        self.timer.stop()
        if not self.Rec_2_btn.isEnabled():
            self.Timer_time2.display(self.s)
            self.Stop_btn.setDisabled(True)
            self.s = 0
        elif not self.Rec_btn.isEnabled() or not self.Rec_3_btn.isEnabled():
            self.s = 5
            self.Timer_time.display(self.s)
            self.Timer_time3.display(self.s)
        self.widget_21.setStyleSheet("border-radius:15px; background-color: rgb(104, 118, 141);text-align:right;")
        self.widget_15.setStyleSheet("border-radius:15px; background-color: rgb(104, 118, 141);text-align:right;")
        self.widget_15.setStyleSheet("border-radius:15px; background-color: rgb(104, 118, 141);text-align:right;")
        self.widget_8.setStyleSheet("border-radius:15px; background-color: rgb(104, 118, 141);text-align:right;")
        self.widget_28.setStyleSheet("border-radius:15px; background-color: rgb(104, 118, 141);text-align:right;")
        self.widget_26.setStyleSheet("")

        self.Starting_point.show()
        self.widget_29.hide()
        self.widget_29.setDisabled(False)
        self.widget_29.setStyleSheet("border-radius:15px; background-color: rgb(104, 118, 141);text-align:right;")

        self.Rec_btn.setText("Record")
        self.Rec_2_btn.setText("Record")
        self.Rec_3_btn.setText("Record")
        self.Starting_point.setText("Start")
        self.Starting_point.setDisabled(False)
        self.Starting_point.hide()
        self.test_name.clear()
        self.test_name.setDisabled(False)
        self.test_test_btn.setDisabled(False)
        self.gender_id_btn.setDisabled(False)
        self.live_test_btn.setDisabled(False)
        self.create_btn.setDisabled(False)
        self.testing_btn.setDisabled(False)
        self.Rec_btn.setDisabled(False)
        self.Rec_2_btn.setDisabled(False)
        self.Rec_3_btn.setDisabled(False)
        self.Rec_4_btn.setDisabled(False)
        self.create_model_btn.setDisabled(False)

    def Testing_main_page(self):
        self.testing_btn.setStyleSheet("background-color: rgb(31, 35, 42);")
        self.create_btn.setStyleSheet("background-color: rgb(22, 25, 29);")
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_2.setCurrentIndex(1)

    def Creating_page(self):
        self.testing_btn.setStyleSheet("background-color: rgb(22, 25, 29);")
        self.create_btn.setStyleSheet("background-color: rgb(31, 35, 42);")
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)

    def livetest_page(self):
        self.live_test_btn.setStyleSheet("background-color: rgb(76, 86, 103);")
        self.test_test_btn.setStyleSheet("#16181d;")
        self.gender_id_btn.setStyleSheet("#16181d;")
        self.stackedWidget_3.setCurrentIndex(1)

    def genderid_page(self):
        self.gender_id_btn.setStyleSheet("background-color: rgb(76, 86, 103);")
        self.live_test_btn.setStyleSheet("#16181d")
        self.test_test_btn.setStyleSheet("#16181d;")
        self.stackedWidget_3.setCurrentIndex(2)

    def Testing_page(self):
        self.test_test_btn.setStyleSheet("background-color: rgb(76, 86, 103);")
        self.gender_id_btn.setStyleSheet("#16181d;")
        self.live_test_btn.setStyleSheet("#16181d;")
        self.stackedWidget_3.setCurrentIndex(0)

    def rec_start1(self):
        self.s = 5
        self.timer.start(1000)
        self.widget_21.setStyleSheet("border-radius:15px;background-color: rgb(22, 25, 29);")
        self.Rec_btn.setText("Recording")

        self.test_test_btn.setDisabled(True)
        self.gender_id_btn.setDisabled(True)
        self.live_test_btn.setDisabled(True)
        self.create_btn.setDisabled(True)
        self.testing_btn.setDisabled(True)
        self.Rec_btn.setDisabled(True)

    def rec_start2(self):
        global k
        k = 2
        self.s = 0
        self.Stop_btn.setDisabled(False)
        self.timer.start(1000)
        self.widget_8.setStyleSheet("border-radius:15px;background-color: rgb(22, 25, 29);")
        self.Rec_2_btn.setText("Recording")

        self.test_test_btn.setDisabled(True)
        self.gender_id_btn.setDisabled(True)
        self.live_test_btn.setDisabled(True)
        self.create_btn.setDisabled(True)
        self.testing_btn.setDisabled(True)
        self.Rec_2_btn.setDisabled(True)

    def rec_start3(self):
        self.s = 6
        self.timer.start(1000)
        self.widget_15.setStyleSheet("border-radius:15px;background-color: rgb(22, 25, 29);")
        self.Rec_3_btn.setText("Recording")

        self.test_test_btn.setDisabled(True)
        self.gender_id_btn.setDisabled(True)
        self.live_test_btn.setDisabled(True)
        self.create_btn.setDisabled(True)
        self.testing_btn.setDisabled(True)
        self.Rec_3_btn.setDisabled(True)
        self.Rec_4_btn.setDisabled(True)

    def threaddding(self):
        self.threadpool.start(Recordings())

    def btn_stop(self):
        global k
        k = 0
        y = self.s

        self.Timer_timestop()
        self.Timer_time2.display(y)

    def model_create(self):
        self.s = 7
        temp = self.test_name.text()

        if not self.test_name.text():
            self.widget_30.setStyleSheet("border:1px solid red;border-color: rgb(170, 0, 0);")
            self.textBrowser.setText("ENTER A NAME")
            print("hello")
        elif temp[0].isdigit() or not temp.isalnum():
            self.widget_30.setStyleSheet("border:1px solid red;border-color: rgb(170, 0, 0);")
            self.textBrowser.setText("Name cannot be a number,space or begins with a number")
            print("mo")

        else:
            print(temp[0])
            self.widget_29.show()
            self.tempo.setText("Back")
            self.widget_30.setStyleSheet("")
            self.textBrowser.setText("")
            self.test_name.setDisabled(True)

            self.create_model_btn.setDisabled(True)
            self.widget_26.setStyleSheet(
                "border-top-left-radius:10px;border-bottom-left-radius:10px;background-color: rgb(22, 25, 29);")
            self.train_model_btn.setDisabled(True)
            self.create_btn.setDisabled(True)
            self.testing_btn.setDisabled(True)

            self.label.show()
            self.Starting_point.show()
            self.Many_left_lb.show()
            self.clock.show()

    def namings(self):
        global n, name
        self.Starting_point.hide()
        self.widget_29.show()
        self.tempo.setText("Recording")
        self.widget_29.setDisabled(True)
        self.widget_29.setStyleSheet("border-radius:15px;background-color: rgb(22, 25, 29);")

        # self.widget_28.setStyleSheet("border-radius:15px;background-color: rgb(22, 25, 29);")
        self.textBrowser.setText(Words[n])
        name = self.test_name.text()

        self.timer.start(1000)
        global save_file_name
        save_file_name = "sounds/" + name + "-sample" + str(n) + ".wav"
        print("n is : ", n)
        self.Many_left_lb.setText(str(n + 1) + "/5")
        if n == 5:
            self.train_model_btn.setDisabled(False)
            self.Timer_timestop()
            self.Many_left_lb.setText(str(n) + "/5")
            self.test_name.clear()

    def train(self):
        self.textBrowser.clear()
        self.train_model_btn.setDisabled(True)

        self.widget_27.setStyleSheet(
            "border-top-left-radius:10px;border-bottom-left-radius:10px;background-color: rgb(22, 25, 29);")
        asp = create_model()
        print(asp)
        for i in range(len(asp)):
            self.textBrowser.append(str(asp[i]))
            self.widget_27.setStyleSheet("")
            self.train_model_btn.setDisabled(False)

    def pre_record(self):
        containment = testing("speaker-models/Gender/")
        print(containment)
        if containment == "Male":
            self.Male_frame.setStyleSheet("background-color: rgb(0, 170, 0);")
            self.Female_frame.setStyleSheet("background-color: rgb(170, 170, 127);color: rgb(0, 0, 0);")
        else:
            self.Female_frame.setStyleSheet("background-color: rgb(0, 170, 0);")
            self.Male_frame.setStyleSheet("background-color: rgb(170, 170, 127);color: rgb(0, 0, 0);")

    def Closing(self):
        global k
        self.threadpool.cancel(Recordings())
        k = 0
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Mywindow()
    window.show()
    sys.exit(app.exec_())
