from bss import *
from kinet import *
from Tkinter import *
import tkMessageBox
import serial
from PIL import Image, ImageTk

# Mixer address
# --------------------
# B Rig       00 01 01
# Aux         00 01 02
# Founders    00 01 03
# Stage       00 01 08

# Channel address     MUTES
# -------------------------
# Channel 5   01 90   01 91
# Channel 6   01 F4   01 F5
# Channel 11  03 E8   03 E9

class App:
	def __init__(self):
		self.master = Tk()
		self.master.title('WSOP Audio and Lighting Controller')
		self.master.geometry("1024x768")
		self.master.configure(background='black')
		self.master.iconbitmap('logos/wsopIcon.ico')
		self.master.overrideredirect(1)
		self.master.bind('<Escape>', quit)

		self.dmxStatus = open("config","r").read().rstrip()

		# Startup
		print 'connecting to Blu 80'
		try:
			self.blu = Blu('192.168.1.200')
		except socket.error:
			tkMessageBox.showinfo("Connection Error", "Could not connect to audio system. Contact Nicholas Petty")

		print 'starting DMX'
		try:
			if self.dmxStatus == '1':
				self.dmx = serial.Serial(7, baudrate=115200).write('254,254,127,127,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,0,254,127,254,127,254,0,0,0,0,0,0,127,254,0,0,0,254,0,127,254,254,0,0,0,0,254,0,254~')
			if self.dmxStatus == '0':
				self.dmx = serial.Serial(7, baudrate=115200)
				#time.sleep(1)	
		except serial.serialutil.SerialException:
			self.dmx = serial.serial_for_url('loop://', timeout=1)
			tkMessageBox.showinfo("Connection Error", "Could not connect to lighting system.  Contact Nicholas Petty")

		print 'connecting to cove lighting'
		self.units = [0,1,2,3,4,5]
		self.units[0] = PowerSupply('192.168.1.101')
		self.units[1] = PowerSupply('192.168.1.102')
		self.units[2] = PowerSupply('192.168.1.103')
		self.units[3] = PowerSupply('192.168.1.104')
		self.units[4] = PowerSupply('192.168.1.105')
		self.units[5] = PowerSupply('192.168.1.106')

		x=0
		while x < 510:
		    self.units[0].append(FixtureRGB(x))
		    self.units[1].append(FixtureRGB(x))
		    self.units[2].append(FixtureRGB(x))
		    self.units[3].append(FixtureRGB(x))
		    self.units[4].append(FixtureRGB(x))
		    self.units[5].append(FixtureRGB(x))
		    x+=3

		# Logo's
		bluesvilleImage = ImageTk.PhotoImage(file='logos/bluesville.png')
		bluesvilleLogo = Label(self.master, image=bluesvilleImage, bg='black')
		bluesvilleLogo.place(x=200, y=-10)

		wsopImage = ImageTk.PhotoImage(file='logos/wsop.png')
		wsopLogo = Label(self.master, image=wsopImage, bg='black')
		wsopLogo.place(x=600, y=10)

		contactInfo = Label(self.master, bg='black', fg='white', font=("Helvetica", "20"), text='Nicholas Petty: (662) 288-1214').place(x=325, y=445)
		emailInfo = Label(self.master, bg='black', fg='white', font=("Helvetica", "20"), text='TunicaEntertainment@caesars.com').place(x=295, y=480)

		edycImage = ImageTk.PhotoImage(file='logos/edyc.png')
		edycLogo = Label(self.master, image=edycImage, bg='black')
		edycLogo.place(x=425, y=550)


		# Light Controls
		lightsLabel = Label(self.master, bg='black', fg='white', font=("Helvetica", "20"), text='Lights').place(x=640, y=235)

		lightsOn = Button(self.master, width=10, height=3, text='On', command=lambda: self.lights(1)).place(x=640, y=290)
		lightsOff = Button(self.master, width=10, height=3, text='Off', command=lambda: self.lights(0)).place(x=640, y=350)


		# B Rig Controls
		bRigLabel = Label(self.master, bg='black', fg='white', font=("Helvetica", "20"), text='Floor').place(x=330, y=235)

		dtvLabel1 = Label(self.master, bg='black', fg='white', font=("Helvetica", "16"), text='DTV').place(x=315, y=275)
		dtvScale1 = Scale(self.master, bg='black', fg='white', highlightbackground='black', width=20, from_=300, to=0, command=lambda value: self.setVolume('000101', '0190', '01f4', value)).place(x=300, y=300)

		micLabel1 = Label(self.master, bg='black', fg='white', font=("Helvetica", "16"), text='MIC').place(x=370, y=275)
		micScale1 = Scale(self.master, bg='black', fg='white', highlightbackground='black', width=20, from_=300, to=0, command=lambda value: self.setVolume('000101', '03E8', '03E8', value)).place(x=355, y=300)


		# Stage Controls
		stageLabel = Label(self.master, bg='black', fg='white', font=("Helvetica", "20"), text='Stage').place(x=480, y=235)

		dtvLabel2 = Label(self.master, bg='black', fg='white', font=("Helvetica", "16"), text='DTV').place(x=470, y=275)
		dtvScale2 = Scale(self.master, bg='black', fg='white', highlightbackground='black', width=20, from_=300, to=0, command=lambda value: self.setVolume('000102', '0190', '01f4', value)).place(x=455, y=300)

		micLabel2 = Label(self.master, bg='black', fg='white', font=("Helvetica", "16"), text='MIC').place(x=525, y=275)
		micScale2 = Scale(self.master, bg='black', fg='white', highlightbackground='black', width=20, from_=100, to=0, command=lambda value: self.setVolume('000102', '03E8', '03E8', value)).place(x=510, y=300)

		mainloop()

	def LEDLights(self, state):
		if state == 1:
			for y in range(0,6):
				x=0
				while x <= 75:
					self.units[y][x].rgb = (255,255,255)
					x+=1
				self.units[y].go()
				#time.sleep(1)

		if state == 0:
			for y in range(0,6):
				x=0
				while x <= 75:
					self.units[y][x].rgb = (0,0,0)
					x+=1
				#time.sleep(1)					
				self.units[y].go()
			

	def setVolume(self, mixer, channel1, channel2, percent):
		#print percent
		try:
			self.blu.setPercent('1e19', '03', mixer, channel1, percent)
			self.blu.setPercent('1e19', '03', mixer, channel2, percent)
		except NameError:
			tkMessageBox.showinfo("Connection Error", "Could not connect to audio system.  Contact Nicholas Petty")

	def setMute(self, mixer, channel1, channel2, muteState):
		print muteState
		#blu.setState('1e19', '03', mixer, channel1, muteState)
		#blu.setState('1e19', '03', mixer, channel2, muteState)

	def lights(self, state):
		if state == 1:
			print 'called on'
			self.LEDLights(1)
			open('config', 'w').write('1')
			self.dmx.write('254,254,127,127,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,0,254,127,254,127,254,0,0,0,0,0,0,127,254,0,0,0,254,0,127,254,254,0,0,0,0,254,0,254~')
			#self.dmx.write(dmxOn)

		if state == 0:
			print 'called off'
			self.LEDLights(0)
			open('config', 'w').write('0')
		 	self.dmx.write('0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0~')
		 	#self.dmx.write(dmxOff)

	def test(val):
		print val

app = App()

	