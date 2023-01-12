import numpy           # for number generator
import pyaudio         # for audio out
import math            # for matematical functions
from tkinter import *  # GUI




import numpy as np    #need to pyplot work
import pyaudio as pa  #for works with microphone 
import struct 
import matplotlib.pyplot as plt #for graph




def sigrec():   #func for liesten button
    
    buf = 1024 * 2 #lengh of buffer
    fr = pa.paInt16
    ch = 1     #adress of microphone on pc
    hz = 44100     # RATE in Hz

    p = pa.PyAudio()    

    stream = p.open(        #streaming params:
        format = fr,
        channels = ch,
        rate = hz,
        input=True,
        output=True,
        frames_per_buffer=buf
    )




    fig,ax = plt.subplots()
    x = np.arange(0,2*buf,2)
    line, = ax.plot(x, np.random.rand(buf),'b')
    ax.set_ylim(-35000,35000)          #amplitude, may to change (sensivity)
    ax.ser_xlim = (0,buf)
    fig.show()

    while 1:     #audio chanel
        data = stream.read(buf)
        dataInt = struct.unpack(str(buf) + 'h', data)
        line.set_ydata(dataInt)
        fig.canvas.draw()
        fig.canvas.flush_events()
   







class ToneGenerator(object):

    def __init__(self, samplerate=44100, frames_per_buffer=4410):  # pyaudio init
        self.p = pyaudio.PyAudio()
        self.samplerate = samplerate
        self.frames_per_buffer = frames_per_buffer
        self.streamOpen = False

    def sinewave(self):                                     #tone sinewave creating
        if self.buffer_offset + self.frames_per_buffer - 1 > self.x_max:
            # We don't need a full buffer or audio so pad the end with 0's
            xs = numpy.arange(self.buffer_offset,
                              self.x_max)
            tmp = self.amplitude * numpy.sin(xs * self.omega)
            out = numpy.append(tmp,
                               numpy.zeros(self.frames_per_buffer - len(tmp)))
        else:
            xs = numpy.arange(self.buffer_offset,
                              self.buffer_offset + self.frames_per_buffer)
            out = self.amplitude * numpy.sin(xs * self.omega)
        self.buffer_offset += self.frames_per_buffer
        return out

    def callback(self, in_data, frame_count, time_info, status):  # callback func
        if self.buffer_offset < self.x_max:
            data = self.sinewave().astype(numpy.float32)
            return (data.tobytes(), pyaudio.paContinue)
        else:
            return (None, pyaudio.paComplete)

    def is_playing(self):                                       # function in work
        if self.stream.is_active():
            return True
        else:
            if self.streamOpen:
                self.stream.stop_stream()
                self.stream.close()
                self.streamOpen = False
            return False

    def play(self, frequency, duration, amplitude):       #working parametrs
        self.omega = int(frequency) * (math.pi * 2) / self.samplerate
        self.amplitude = amplitude
        self.buffer_offset = 0
        self.streamOpen = True
        self.x_max = math.ceil(self.samplerate * duration) - 1
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.samplerate,
                                  output=True,
                                  frames_per_buffer=self.frames_per_buffer,
                                  stream_callback=self.callback)



def point_amount():                 # Button func for play
    
    p_points = int(p_entry.get())   # Var for frequency
    p_points2 = int(p_entry2.get()) # Var for time
    generator = ToneGenerator()     # Create an instance of the ToneGenerator class 

    amplitude = 0.50                # Amplitude of the waveform
    step_duration = p_points2       # Time (seconds) to play at each step

    frequency = p_points            # Frequency in Hz

    print("Playing tone at {0:0.2f} Hz".format(frequency))
    generator.play(frequency, step_duration, amplitude)    # Start to play


###############################################################################
#                                 Graphical interface                         #
###############################################################################



root = Tk()                         # Create the main window
root.title("Sinus tone generator")

p_label = Label(text="Frequency, Hz:")
p_label.grid(row=0, column=0, sticky="w")

p_label = Label(text="Time of play, sek:")
p_label.grid(row=1, column=0, sticky="w")

p_entry = Entry()
p_entry.grid(row=0, column=1, padx=5, pady=5)

p_entry2 = Entry()
p_entry2.grid(row=1, column=1, padx=5, pady=5)

display_button = Button(text="Play tone", command=point_amount)       # Create the button play
display_button.grid(row=3, column=0, sticky="e")

display_button = Button(text="Liesten", command=sigrec)       # Create the button liesten
display_button.grid(row=3, column=1, padx=5, pady=5)



p_label = Label(text="We can hear on the " )
p_label.grid(row=4, column=0, sticky="w")
p_label = Label(text="frequency from 20 to 20000 hz" )
# the sound apparature works on this interval of frequency too
p_label.grid(row=4, column=1, sticky="w")

root.mainloop()         # Start the main loop

