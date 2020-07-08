from math import sin
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
save = True

def soundFunc(samples, time):
	result =  1 #f0 
	# result =  np.exp(- (1/(time*0.3))*samples) #f2
	# result =  (-1/(1 + np.exp((-1/(0.15 * time)) * (samples - 0.5 * time))) + 1)#f3
	# result = (-1/time)*(samples - time) #f4
	
	
	# if Vibrato:
		# result += 0.5*np.sin(25*samples) 
	if Vibrato:
		result *= 1+0.5*np.sin(25*samples) 
	
	# noise
	# result *= 1 + 0.5*(((500 * np.sin(200 * samples)) % 1 )- 0.5)
	# result *= 10*np.sin(10*np.cos(samples) + samples)*np.cos(samples)
	
	return result
	
def addInsideNote(samples, frequency):
	
	# return ((500 * np.sin(samples))%1 - 0.5)
	
	# return 25*np.sin(2*np.pi*samples)
	# return 25*np.sin(1 * 2*np.pi*samples**2)
	# return 
	# return 2 * np.pi * frequency *0.001* np.exp(samples*30) # water bloop
	# return 2 * np.pi * frequency *0.001* np.sin(samples*30) # proper vibrato
	return 0

def squareWave(samples):
	result = 0.5
	for n in range(20):
		result += (2/((2*n+1)*np.pi)) * np.sin((2*n+1) * np.pi * samples)
	return result
	
def squareWave2(c):
	samples = np.arange(44100 * songLength) / fs
	for i in range(len(samples)):
		samples[i] = int(sin(samples[i] * np.pi * c)) + 1
	return samples

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
	
def chordSheet(frequency, time, start, strum=0):
	samples = np.arange(44100 * songLength) / fs
	
	if strum == 0:
		chord = np.cos(2 * np.pi * frequency[0] * (samples - start)) * soundFunc(samples - start, time)
		for i in frequency[1:chordLength]:
			chord += np.cos(2 * np.pi * i * (samples - (start + time*0.25))) * soundFunc(samples - (start + time*0.25), time)
		
		chord = chord * (np.heaviside(samples - start, 1) - np.heaviside(samples - start - time, 1))
		
	elif strum == 1:
		chord = np.cos(2 * np.pi * frequency[3] * (samples - start)) * soundFunc(samples - start, time)
		chord = chord * (np.heaviside(samples - start, 1) - np.heaviside(samples - start - time, 1))
		
		note2 = np.cos(2 * np.pi * frequency[2] * (samples - start - time*(1/4))) * soundFunc(samples - start -time*(1/4), time/4)
		note2 = note2 * (np.heaviside(samples - start -time*(1/4), 1) - np.heaviside(samples - start - time, 1))
		
		chord += note2
		
		note3 = np.cos(2 * np.pi * frequency[1] * (samples - start - time*(1/2))) * soundFunc(samples - start -time*(1/2), time/4)
		note3 = note3 * (np.heaviside(samples - start -time*(2/4), 1) - np.heaviside(samples - start - time, 1))
		
		chord += note3
		
		note4 = np.cos(2 * np.pi * frequency[0] * (samples - start - time*(3/4))) * soundFunc(samples - start -time*(3/4), time/4)
		note4 = note4 * (np.heaviside(samples - start -time*(3/4), 1) - np.heaviside(samples - start - time, 1))
		
		chord += note4
		
	elif strum == 2:
		chord = np.cos(2 * np.pi * frequency[3] * (samples - start)) * soundFunc(samples - start, time)
		chord = chord * (np.heaviside(samples - start, 1) - np.heaviside(samples - start - time, 1))
		
		note = np.cos(2 * np.pi * frequency[2] * (samples - start - time*(1/8))) * soundFunc(samples - start -time*(1/8), time/8)
		note = note * (np.heaviside(samples - start -time*(1/8), 1) - np.heaviside(samples - start - time*(2/8), 1))
		chord += note
		
		note = np.cos(2 * np.pi * frequency[1] * (samples - start - time*(2/8))) * soundFunc(samples - start -time*(2/8), time/8)
		note = note * (np.heaviside(samples - start -time*(2/8), 1) - np.heaviside(samples - start - time*(3/8), 1))
		chord += note
		
		note = np.cos(2 * np.pi * frequency[2] * (samples - start - time*(3/8))) * soundFunc(samples - start -time*(3/8), time/8)
		note = note * (np.heaviside(samples - start -time*(3/8), 1) - np.heaviside(samples - start - time*(4/8), 1))
		chord += note
		
		note = np.cos(2 * np.pi * frequency[0] * (samples - start - time*(4/8))) * soundFunc(samples - start -time*(4/8), time/8)
		note = note * (np.heaviside(samples - start -time*(4/8), 1) - np.heaviside(samples - start - time*(5/8), 1))
		chord += note
		
		note = np.cos(2 * np.pi * frequency[2] * (samples - start - time*(5/8))) * soundFunc(samples - start -time*(5/8), time/8)
		note = note * (np.heaviside(samples - start -time*(5/8), 1) - np.heaviside(samples - start - time*(6/8), 1))
		chord += note
		
		note = np.cos(2 * np.pi * frequency[1] * (samples - start - time*(6/8))) * soundFunc(samples - start -time*(6/8), time/8)
		note = note * (np.heaviside(samples - start -time*(6/8), 1) - np.heaviside(samples - start - time*(7/8), 1))
		chord += note
		
		note = np.cos(2 * np.pi * frequency[2] * (samples - start - time*(7/8))) * soundFunc(samples - start -time*(7/8), time/8)
		note = note * (np.heaviside(samples - start -time*(7/8), 1) - np.heaviside(samples - start - time*(8/8), 1))
		chord += note
	
	elif strum == 3:
		chord = np.cos(2 * np.pi * frequency[3] * (samples - start)) * soundFunc(samples - start, time)
		chord = chord * (np.heaviside(samples - start, 1) - np.heaviside(samples - start - time, 1))
		
		note = np.cos(2 * np.pi * frequency[2] * (samples - start - time*(1/6))) * soundFunc(samples - start -time*(1/6), time/6)
		note = note * (np.heaviside(samples - start -time*(1/6), 1) - np.heaviside(samples - start - time*(2/6), 1))
		chord += note
		
		note = np.cos(2 * np.pi * frequency[1] * (samples - start - time*(2/6))) * soundFunc(samples - start -time*(2/6), time/6)
		note = note * (np.heaviside(samples - start -time*(2/6), 1) - np.heaviside(samples - start - time*(3/6), 1))
		chord += note
		
		note = np.cos(2 * np.pi * frequency[0] * (samples - start - time*(3/6))) * soundFunc(samples - start -time*(3/6), time/6)
		note = note * (np.heaviside(samples - start -time*(3/6), 1) - np.heaviside(samples - start - time*(4/6), 1))
		chord += note
		
		note = np.cos(2 * np.pi * frequency[1] * (samples - start - time*(4/6))) * soundFunc(samples - start -time*(4/6), time/6)
		note = note * (np.heaviside(samples - start -time*(4/6), 1) - np.heaviside(samples - start - time*(5/6), 1))
		chord += note
		
		note = np.cos(2 * np.pi * frequency[2] * (samples - start - time*(5/6))) * soundFunc(samples - start -time*(5/6), time/6)
		note = note * (np.heaviside(samples - start -time*(5/6), 1) - np.heaviside(samples - start - time*(6/6), 1))
		chord += note
		
	elif strum == 4: #guitar flat strum
		chord = tempGuitar(frequency[0], time, start) * soundFunc(samples - start, time)
		timid = 0.1
		for i in frequency[1:chordLength]:
			chord += tempGuitar(i, time, start) * soundFunc(samples - (start), time)
			timid += 0.1
		
		chord = chord * (np.heaviside(samples - start, 1) - np.heaviside(samples - start - time, 1))
	
	elif strum == 5: #guitar down strumming
		halves = 32
		# chord = np.cos(2 * np.pi * frequency[3] * (samples - start)) * soundFunc(samples - start, time)
		chord = tempGuitar(frequency[3], time, start)
		chord = chord * (np.heaviside(samples - start, 1) - np.heaviside(samples - start - time, 1))
		
		# note2 = np.cos(2 * np.pi * frequency[2] * (samples - start - time*(1/4))) * soundFunc(samples - start -time*(1/4), time/4)
		note2 = tempGuitar(frequency[2], time/halves, start + time*(1/halves)) * soundFunc(samples - (start + time*(1/halves)), time/halves)
		note2 = note2 * (np.heaviside(samples - start -time*(1/halves), 1) - np.heaviside(samples - start - time, 1))
		
		chord += note2
		
		# note3 = np.cos(2 * np.pi * frequency[1] * (samples - start - time*(1/2))) * soundFunc(samples - start -time*(1/2), time/4)
		note3 = tempGuitar(frequency[1], time/halves, start + time*(2/halves)) * soundFunc(samples - (start + time*(2/halves)), time/halves)
		note3 = note3 * (np.heaviside(samples - start -time*(2/halves), 1) - np.heaviside(samples - start - time, 1))
		
		chord += note3
		
		# note4 = np.cos(2 * np.pi * frequency[0] * (samples - start - time*(3/4))) * soundFunc(samples - start -time*(3/4), time/4)
		note4 = tempGuitar(frequency[0], time/halves, start + time*(3/halves)) * soundFunc(samples - (start + time*(3/halves)), time/halves)
		note4 = note4 * (np.heaviside(samples - start -time*(3/halves), 1) - np.heaviside(samples - start - time, 1))
		
		chord += note4
	
	
	chord *= chordVolume
	
	return chord

def noteSheet(frequency, time, start):
	return noteGuitar(frequency, time, start)
	samples = np.arange(44100 * songLength) / fs
	
	note = np.cos(2 * np.pi * frequency * (samples - start) + addInsideNote(samples-start, frequency) ) * soundFunc(samples - start, time)
	note = note * (np.heaviside(samples - start, 1) - np.heaviside(samples - start - time, 1))
	
	note *= noteVolume
	
	return note
	
def noteGuitar(frequency, time, start):
	
	samples = np.arange(44100 * songLength) / fs
	h = 1
	L = 100
	d = 1
	b = 0.0
	
	a = lambda n: ((2*h*L**2)/((np.pi**2)*(n**2)*d*(L-d)))* np.sin((n*np.pi*d)/L)
	f = lambda n: n*frequency*((1 + (b**2)*(n**2))**0.5)
	
	result = a(1)*np.cos(2 * np.pi * f(1) * (samples - start))
	
	for i in range(2,50):
		result += a(i)*np.cos(2 * np.pi * f(i) * (samples - start)) * np.exp(- i * 1 * (samples - start))
	
	result = result * (np.heaviside(samples - start, 1) - np.heaviside(samples - start - time, 1))
	result *= noteVolume
	
	return result

def tempGuitar(frequency, time, start):
	samples = np.arange(44100 * songLength) / fs
	h = 1
	L = 100
	d = 1
	b = 0.0
	# print(frequency)
	a = lambda n: ((2*h*L**2)/((np.pi**2)*(n**2)*d*(L-d)))* np.sin((n*np.pi*d)/L)
	f = lambda n: n*frequency*((1 + (b**2)*(n**2))**0.5)
	
	result = a(1)*np.cos(2 * np.pi * f(1) * (samples - start))
	
	for i in range(2,50):
		result += a(i)*np.cos(2 * np.pi * f(i) * (samples - start)) * np.exp(- i * 1 * (samples - start))
	
	# result = result * (np.heaviside(samples - start, 1) - np.heaviside(samples - start - time, 1))
	return result

	
	
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
chordLength = 4

A = [e5, 554.37, a4, e4, "A"]
Am = [e5, c5, a4, e4, "Am"]
Bb = [f5, d5, 466.16, f4, "Bb"]
B = [739.99, 622.25, b4, 369.99, "B"]
C = [e5, c5, g4, e4, "C"]
D = [739.99, d5, a4, d4, "D"]
Dm = [f5, d5, a4, d4, "Dm"]
E = [e5, b4, 415.30, e4, "E"]
Em = [e5, b4, g4, e4, "Em"]
F = [f5, c5, a4, f4, "F"]
G = [g5, d5, g4, d4, "G"]

Cchords = [Am, C, G, D, Em, Dm, F, Bb]# ,E]#, A, B]

cMajor6 = [c6, d6, e6, f6, g6, a6, b6]
cMajor5 = [c5, d5, e5, f5, g5, a5, b5]
cMajor4 = [c4, d4, e4, f4, g4, a4, b4]

scale = cMajor4 + cMajor5  + [rest]#+ cMajor6

tones = [0.5, 1,2,4,8] #will divide by 8
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

def createSongOrg():
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

################### MAIN SETUP

def playSong():
	chords = sample(Cchords, 4)
	
	# chords = [G, D, Em, C]
	
	chordString = chords[0][chordLength] + " " + chords[1][chordLength] + " " + chords[2][chordLength]+ " " + chords[3][chordLength]+ " "
	print(chordString)
	
	sheet = np.arange(44100 * songLength) / fs
	
	strum = 5
	
	sheet += chordSheet(chords[0], tempo, 0 * tempo, strum)
	sheet += chordSheet(chords[1], tempo, 1 * tempo, strum)
	sheet += chordSheet(chords[2], tempo, 2 * tempo, strum)
	sheet += chordSheet(chords[3], tempo, 3 * tempo, strum)
	
	sheet += sheetFromHouse(createHouseClose(), 0 * tempo)
	sheet += sheetFromHouse(createHouseClose(), 1 * tempo)
	sheet += sheetFromHouse(createHouseClose(), 2 * tempo)
	sheet += sheetFromHouse(createHouseClose(), 3 * tempo)
	
	# make audio
	audio = sheet * (2**15 - 1) / np.max(np.abs(sheet))
	audio = audio.astype(np.int16)
	# play sound
	play_obj = sa.play_buffer(audio, 1, 2, fs)
	play_obj.wait_done()
	
	return (audio, chordString)

audio, chordString = playSong()


# noteg = noteGuitar(440, 1, 0)

# audio = noteg * (2**15 - 1) / np.max(np.abs(noteg))
# audio = audio.astype(np.int16)

# play_obj = sa.play_buffer(audio, 1, 2, fs)
# play_obj.wait_done()


# current date and time
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y %H-%M-%S")

if save:
	audio = np.int16(audio * 1)
	write('musical/' + dt_string + " " + chordString + '.wav', fs, audio)





