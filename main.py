import wave
import Ist_recording
import tongue_wrds
import test


def output_file():
    if take == 0:
        wf = wave.open(save_file_name, 'wb')
        with open("sounds.txt", 'a') as f:
            f.write((Names[0] + "-sample" + str(i) + ".wav")+'\n')
    else:
        wf = wave.open('testing.wav', 'wb')
    wf.setnchannels(Ist_recording.channels)
    wf.setsampwidth(Ist_recording.p.get_sample_size(Ist_recording.sample_format))
    wf.setframerate(Ist_recording.fs)
    wf.writeframes(b''.join(Ist_recording.frames))
    wf.close()

    Ist_recording.frames.clear()


Names = []
filename = "sounds/"

take = int(input("enter 0 for rec or 2 for live :"))

if take == 0:
    for i in range(1):
        name = input("whats your name : ")
        Names.append(name)

    print(Names)
    for i in range(5):
        save_file_name = filename + Names[0] + "-sample" + str(i) + ".wav"
        print("SAY THIS : " + tongue_wrds.Words[i] + " in")
        tongue_wrds.countdown()
        Ist_recording.recording()
        output_file()

else:
    tongue_wrds.countdown()
    while int(take) > 1:
        Ist_recording.recording1()
        output_file()
        test.testing()
