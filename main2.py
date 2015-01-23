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
		self.master.geometry("640x640")
		self.master.configure(background='black')
		self.master.iconbitmap('logos/wsopIcon.ico')

		# Starup
		print 'connecting to Blu 80'
		try:
			self.blu = Blu('192.168.1.200')
		except socket.error:
			tkMessageBox.showinfo("Connection Error", "Could not connect to audio system. Contact Nicholas Petty")

		print 'starting DMX'
		try:
			self.dmx = serial.Serial(7, baudrate=115200)
			time.sleep(1)	
		except serial.serialutil.SerialException:
			self.dmx = serial.serial_for_url('loop://', timeout=1)
			tkMessageBox.showinfo("Connection Error", "Could not connect to lighting system.  Contact Nicholas Petty")

		print 'connecting to cove lighting'
		self.units = []
		units[0].append(PowerSupply('192.168.1.101'))
		units[1].append(PowerSupply('192.168.1.102'))
		units[2].appedn(PowerSupply('192.168.1.103'))
		units[3].append(PowerSupply('192.168.1.104'))
		units[4].append(PowerSupply('192.168.1.105'))
		units[5].append(PowerSupply('192.168.1.106'))

		x=0
		while x < 510:
		    self.units[0]rgb = (FixtureRGB(x))
		    self.units[1].append(FixtureRGB(x))
		    self.units[2].append(FixtureRGB(x))
		    self.units[3].append(FixtureRGB(x))
		    self.units[4].append(FixtureRGB(x))
		    self.units[5].append(FixtureRGB(x))
		    x+=3

		# Logo's
		bluesvilleImage = ImageTk.PhotoImage(file='logos/bluesville.png')
		bluesvilleLogo = Label(self.master, image=bluesvilleImage, bg='black')
		bluesvilleLogo.place(x=0, y=-10)

		wsopImage = ImageTk.PhotoImage(file='logos/wsop.png')
		wsopLogo = Label(self.master, image=wsopImage, bg='black')
		wsopLogo.place(x=400, y=10)

		contactInfo = Label(self.master, bg='black', fg='white', font=("Helvetica", "20"), text='Nicholas Petty: (662) 288-1214').place(x=125, y=445)
		emailInfo = Label(self.master, bg='black', fg='white', font=("Helvetica", "20"), text='TunicaEntertainment@caesars.com').place(x=95, y=480)

		edycImage = ImageTk.PhotoImage(file='logos/edyc.png')
		edycLogo = Label(self.master, image=edycImage, bg='black')
		edycLogo.place(x=225, y=550)


		# Light Controls
		lightsLabel = Label(self.master, bg='black', fg='white', font=("Helvetica", "20"), text='Lights').place(x=440, y=235)

		lightsOn = Button(self.master, width=10, height=3, text='On', command=lambda: self.lights(1)).place(x=440, y=290)
		lightsOff = Button(self.master, width=10, height=3, text='Off', command=lambda: self.lights(0)).place(x=440, y=350)


		# B Rig Controls
		bRigLabel = Label(self.master, bg='black', fg='white', font=("Helvetica", "20"), text='Floor').place(x=130, y=235)

		dtvLabel1 = Label(self.master, bg='black', fg='white', font=("Helvetica", "16"), text='DTV').place(x=115, y=275)
		dtvScale1 = Scale(self.master, bg='black', fg='white', highlightbackground='black', width=20, from_=100, to=0, command=lambda value: self.setVolume('000101', '0190', '01f4', value)).place(x=100, y=300)

		micLabel1 = Label(self.master, bg='black', fg='white', font=("Helvetica", "16"), text='MIC').place(x=170, y=275)
		micScale1 = Scale(self.master, bg='black', fg='white', highlightbackground='black', width=20, from_=100, to=0, command=lambda value: self.setVolume('000101', '03E8', '03E8', value)).place(x=155, y=300)


		# Stage Controls
		stageLabel = Label(self.master, bg='black', fg='white', font=("Helvetica", "20"), text='Stage').place(x=280, y=235)

		dtvLabel2 = Label(self.master, bg='black', fg='white', font=("Helvetica", "16"), text='DTV').place(x=270, y=275)
		dtvScale2 = Scale(self.master, bg='black', fg='white', highlightbackground='black', width=20, from_=100, to=0, command=lambda value: self.setVolume('000102', '0190', '01f4', value)).place(x=255, y=300)

		micLabel2 = Label(self.master, bg='black', fg='white', font=("Helvetica", "16"), text='MIC').place(x=325, y=275)
		micScale2 = Scale(self.master, bg='black', fg='white', highlightbackground='black', width=20, from_=100, to=0, command=lambda value: self.setVolume('000102', '03E8', '03E8', value)).place(x=310, y=300)

		mainloop()

	def LEDLights(self, state):


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
			#status = Label(self.master, bg='black', fg='white', text='Turning on lights...').place(x=100,y=2)
			#tkMessageBox.showinfo("On")
			x = 0
			while x <= 160:
				self.pds1[x].rgb = (255,255,240)
				self.pds2[x].rgb = (255,255,240)
				self.pds3[x].rgb = (255,255,240)
				self.pds4[x].rgb = (255,255,240)
				self.pds5[x].rgb = (255,255,240)
				self.pds6[x].rgb = (255,255,240)
				#time.sleep(.2)
				x += 1
			#self.dmx.write('254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,0,254,254,254,254,254,0,0,0,0,0,0,254,254,0,0,0,254,0,254,254,254,0,0,0,0,254,0,254~')

		if state == 0:
			print 'called off'
			#tkMessageBox.showinfo("Off")
			x = 0
			while x <= 160:
				self.pds1[x].rgb = (0,0,0)
				self.pds2[x].rgb = (0,0,0)
				self.pds3[x].rgb = (0,0,0)
				self.pds4[x].rgb = (0,0,0)
				self.pds5[x].rgb = (0,0,0)
				self.pds6[x].rgb = (0,0,0)
				#time.sleep(.2)
				x += 1
		 	#self.dmx.write('0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0~')
		
		time.sleep(1)
		self.pds1.go()
		time.sleep(1)
		self.pds2.go()
		time.sleep(1)
		self.pds3.go()
		time.sleep(1)
		self.pds4.go()
		time.sleep(1)
		self.pds5.go()
		time.sleep(1)
		self.pds6.go()
		time.sleep(1)

	def test(val):
		print val

app = App()
	