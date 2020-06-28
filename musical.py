
from random import choice, randint, sample
import numpy as np
import simpleaudio as sa
from scipy.io.wavfile import write
from datetime import datetime

fs = 44100   # 44100 samples per second, can also try 22050

tempo = 2 #seconds
songLength = 4 * tempo

chordVolume = 5
noteVolume = 8

Vibrato = False
save = False
		
def soundFunc(samples, time):
	# result =  1 #f0 
	# result =  np.exp(- (1/(time*0.3))*samples) #f2
	# result =  (-1/(1 + np.exp((-1/(0.15 * time)) * (samples - 0.5 * time))) + 1)#f3
	result = (-1/time)*(samples - time) #f4
	
	if Vibrato:
		result += 0.5*np.sin(25*samples) 
	return result

def playNote(frequency, time = 0.1):
	samples = np.arange(44100 * time) / fs
	note = np.cos(2 * np.pi * frequency * samples) * soundFunc(samples, time)
	audio = note * (2**15 - 1) / np.max(np.abs(note))
	audio = audio.astype(np.int16)
	play_obj = sa.play_buffer(audio, 1, 2, fs)
	play_obj.wait_done()
	
def playChord(frequency, time = 0.1):
	samples = np.arange(44100 * time) / fs
	
	note = np.cos(2 * np.pi * frequency[0] * samples) * soundFunc(samples, time)
	for i in frequency[1:3]:
		note += np.cos(2 * np.pi * i * samples) * soundFunc(samples, time)
	
	audio = note * (2**15 - 1) / np.max(np.abs(note))
	audio = audio.astype(np.int16)
	play_obj = sa.play_buffer(audio, 1, 2, fs)
	play_obj.wait_done()
	
def chordSheet(frequency, time, start):
	samples = np.arange(44100 * songLength) / fs
	
	chord = np.cos(2 * np.pi * frequency[0] * (samples - start)) * soundFunc(samples - start, time)
	for i in frequency[1:3]:
		chord += np.cos(2 * np.pi * i * (samples - start)) * soundFunc(samples - start, time)
	
	chord = chord * (np.heaviside(samples - start, 1) - np.heaviside(samples - start - time, 1))
	chord *= chordVolume
	
	return chord

def noteSheet(frequency, time, start):
	samples = np.arange(44100 * songLength) / fs
	
	note = np.cos(2 * np.pi * frequency * (samples - start)) * soundFunc(samples - start, time)
	note = note * (np.heaviside(samples - start, 1) - np.heaviside(samples - start - time, 1))
	
	note *= noteVolume
	
	return note
	
# notes
rest = 0.1

c4 = 261.63
d4 = 293.66
e4 = 329.63
f4 = 349.23
g4 = 392.00
a4 = 440.00
b4 = 493.88

c5 = 523.25
d5 = 587.33
e5 = 659.25
f5 = 698.46
g5 = 783.99
a5 = 880.00
b5 = 987.77

c6 = 1046.50
d6 = 1174.66
e6 = 1318.51
f6 = 1396.91
g6 = 1567.98
a6 = 1760.00
b6 = 1975.53

# chords
A = [554.37, a4, e4, "A"]
Am = [c5, a4, e4, "Am"]
Bb = [d5, 466.16, f4, "Bb"]
B = [622.25, b4, 369.99, "B"]
C = [c5, g4, e4, "C"]
D = [d5, a4, d4, "D"]
Dm = [d5, a4, d4, "Dm"]
E = [b4, 415.30, e4, "E"]
Em = [b4, g4, e4, "Em"]
F = [c5, a4, f4, "F"]
G = [d5, g4, d4, "G"]

Cchords = [Am, C, G, D, Em, Dm, F, Bb, E]#, A, B]

cMajor6 = [c6, d6, e6, f6, g6, a6, b6]
cMajor5 = [c5, d5, e5, f5, g5, a5, b5]
cMajor4 = [c4, d4, e4, f4, g4, a4, b4]

scale = cMajor4 + cMajor5 + cMajor6 + [rest]

tones = [0.5,1,2,4,8] #will divide by 8
full = 0
song = []

def playSong(song):
	for house in song:
		for note in house:
			playNote(note[0], note[1])

def sheetFromHouse(house, time):
	# house: (freq, time)
	samples = np.arange(44100 * songLength) / fs
	sheet = samples
	
	currentTime = time
	for note in house:
		freq = note[0]
		t = note[1]
		sheet += noteSheet(freq, t, currentTime)
		currentTime += t
	return sheet

def createHouse():
	full = 0
	step = []
	house = []
	while True:
		tone = choice(tones)
		if full + tone > 8:
			continue
		full += tone
		step.append(tone)
		if full == 8:
			break
	for i in step:
		freq = choice(scale)
		house.append((freq, i/(8/tempo)))
	return house
		
def createHouseClose():
	full = 0
	step = []
	house = []
	diff = 3
	while True:
		tone = choice(tones)
		if full + tone > 8:
			continue
		full += tone
		step.append(tone)
		if full == 8:
			break
	
	j = randint(0,len(scale)-1)
	for i in step:
		
		# j = randint(j-diff, min(j+diff, len(scale)-1))
		j = randint(j-diff, j+diff) % len(scale)-1
		freq = scale[j]
			
		house.append((freq, i/(8/tempo)))
	return house

def createSong():
	song = []
	for i in range(4):
		song.append(createHouseClose())
	song.append(song[0])
	song.append(song[1])
	for i in range(2):
		song.append(createHouseClose())
	song.append(song[0])
	song.append(song[1])
	return song


chords = sample(Cchords, 4)
chordString = chords[0][3] + " " + chords[1][3] + " " + chords[2][3]+ " " + chords[3][3]+ " "
print(chordString)

sheet = np.arange(44100 * songLength) / fs

sheet += chordSheet(chords[0], tempo, 0 * tempo)
sheet += chordSheet(chords[1], tempo, 1 * tempo)
sheet += chordSheet(chords[2], tempo, 2 * tempo)
sheet += chordSheet(chords[3], tempo, 3 * tempo)

sheet += sheetFromHouse(createHouseClose(), 0 * tempo)
sheet += sheetFromHouse(createHouseClose(), 1 * tempo)
sheet += sheetFromHouse(createHouseClose(), 2 * tempo)
sheet += sheetFromHouse(createHouseClose(), 3 * tempo)

audio = sheet * (2**15 - 1) / np.max(np.abs(sheet))
audio = audio.astype(np.int16)
# play sound
play_obj = sa.play_buffer(audio, 1, 2, fs)
play_obj.wait_done()


# current date and time
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y %H-%M-%S")

if save:
	audio = np.int16(audio * 1)
	write('musical/' + dt_string + " " + chordString + '.wav', fs, audio)





