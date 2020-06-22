# MFT EXTRACT BY CHRIS TROY VER 1.0.0
import struct
import os
import time
from concurrent.futures import ThreadPoolExecutor
import shutil
import psutil
import re
from tqdm import tqdm

# drive_filename = r'\\.\\'
log_filename = r'C:\scriptlog\\volumeDump.txt'
MFTrecord = 'C:\\scriptlog\\MFTrecord.txt'
ntfs_info = r'C:\scriptlog\ntfs.txt'
MFT_SIZE = r'C:\scriptlog\MFTSize.txt'


class NTFSinfo:
	def __init__(self):
		print('Is this your first time running this program?')
		print('In order for this script to work, a data dump of your drive is required which will be stored in C drive')
		print('PLEASE LISTEN CAREFULLY!!!')
		print('THE DATA DUMP WILL BE THE SAME SIZE OF YOUR HARD DRIVE. IF YOUR DRIVE IS 400GB, YOU WILL NEED 400GB OF SPACE in C: TO STORE THE DATA DUMP')
		print('Type (no) if you have already taken a memory dump of the volume, or (yes) to proceed to taking one')
		self.results = []
		accept = input('yes/no: ')
		if accept == "yes":
			print('Provide the volume label. e.g. C, D, E, F:')
			getVolumeLabel = input('Volume Label: ')
			drive_filename = r'\\.\\'+getVolumeLabel+':'
			print(drive_filename)
			print('Volume Dump Beginning. please be patient and allow the data to be extracted')
			with ThreadPoolExecutor(max_workers=8) as e:
				e.submit(shutil.copy, drive_filename, log_filename)

			print('VOLUME DUMP COMPLETE')
			continuation = True
			while continuation:

				self.choice = self.menu()
				if self.choice == "1":
					self.getOEMID()
					more = input('Continue? y/n: ')
					if more == "y":
						continue
					else:
						continuation = False
				elif self.choice == "2":
					self.getBPS()
					more = input('Continue? y/n: ')
					if more == "y":
						continue
					else:
						continuation = False
				elif self.choice == "3":
					self.getSPC()
					more = input('Continue? y/n: ')
					if more == "y":
						continue
					else:
						continuation = False
				elif self.choice == "4":
					self.getHPT()
					more = input('Continue? y/n: ')
					if more == "y":
						continue
					else:
						continuation = False
				elif self.choice == "5":
					self.totalSectors()
					more = input('Continue? y/n: ')
					if more == "y":
						continue
					else:
						continuation = False
				elif self.choice == "6":
					self.MFTcluster()
					more = input('Continue? y/n: ')
					if more == "y":
						continue
					else:
						continuation = False
				elif self.choice == "7":
					self.MFTMirrorCluster()
					more = input('Continue? y/n: ')
					if more == "y":
						continue
					else:
						continuation = False
				elif self.choice == "8":
					self.volumeSerial()
					more = input('Continue? y/n: ')
					if more == "y":
						continue
					else:
						continuation = False
				elif self.choice == "9":
					self.getAll()
					more = input('Continue? y/n: ')
					if more == "y":
						continue
					else:
						continuation = False
				elif self.choice == "10":
					self.getAll()
					more = input('Continue? y/n: ')
					if more == "y":
						self.MFTExtract()
					else:
						continuation = False
				else:
					print('No option exists for that value you provided!')
					exit()
		else:
			continuation = True
			while continuation:
				self.choice = self.menu()
				if self.choice == "1":
					self.getOEMID()
					more = input('Continue? y/n: ')
					if more == 'y':
						continue
					else:
						continuation = False
				elif self.choice == "2":
					self.getBPS()
					more = input('Continue? y/n: ')
					if more == 'y':
						continue
					else:
						continuation = False
				elif self.choice == "3":
					self.getSPC()
					more = input('Continue? y/n: ')
					if more == 'y':
						continue
					else:
						continuation = False
				elif self.choice == "4":
					self.getHPT()
					more = input('Continue? y/n: ')
					if more == 'y':
						continue
					else:
						continuation = False
				elif self.choice == "5":
					self.totalSectors()
					more = input('Continue? y/n: ')
					if more == 'y':
						continue
					else:
						continuation = False
				elif self.choice == "6":
					self.MFTcluster()
					more = input('Continue? y/n: ')
					if more == 'y':
						continue
					else:
						continuation = False
				elif self.choice == "7":
					self.MFTMirrorCluster()
					more = input('Continue? y/n: ')
					if more == 'y':
						continue
					else:
						continuation = False
				elif self.choice == "8":
					self.volumeSerial()
					more = input('Continue? y/n: ')
					if more == 'y':
						continue
					else:
						continuation = False
				elif self.choice == "9":
					self.getAll()
					more = input('Continue? y/n: ')
					if more == 'y':
						continue
					else:
						continuation = False
				elif self.choice == "10":
					self.MFTExtract()
					more = input('Continue? y/n: ')
					if more == 'y':
						continue
					else:
						continuation = False
				else:
					print('No option exists for that value you provided!')
					exit()


	def getOEMID(self):
		# OEM ID
		# Open a file
		file = open(log_filename, "rb")
		# Set pointer to OEM ID
		file.seek(3, 0)
		OEMID = file.readline(8).decode('ansi')
		print ("OEM ID: %s" % (OEMID))
		# Close opend file
		file.close()
		return OEMID

	def getBPS(self):

		## BYTES PER SECTOR
		# Open a file
		file = open(log_filename, "rb")
		# Set pointer to OEM ID
		file.seek(11,0)
		bps = file.readline(2)
		#CONV DATA CONTAINS BYTES PER SECTOR. Convert to little endian
		convData = struct.unpack("<h", bps)[0]
		print(f'Bytes Per Sector: {convData}')
		# Close opend file
		file.close()
		return convData

	def getSPC(self):
		## SECTORS PER CLUSTER
		# Open a file
		file = open(log_filename, "rb")
		# Set pointer to OEM ID
		file.seek(13,0)
		bps = file.readline(2)
		#CONV DATA CONTAINS BYTES PER SECTOR
		convData = struct.unpack("<h", bps)[0]
		print(f'Sectors Per Cluster: {convData}')
		# Close opend file
		file.close()
		return convData

	def getSPT(self):
		## SECTORS PER TRACK
		# Open a file
		file = open(log_filename, "rb")
		# Set pointer to OEM ID
		file.seek(24,0)
		bps = file.readline(2)
		#CONV DATA CONTAINS BYTES PER SECTOR
		convData = struct.unpack("<h", bps)[0]
		print(f'Sectors per track: {convData}')
		# Close opend file
		file.close()
		return convData

	def getHPT(self):
		## HEADS PER TRACK
		# Open a file
		file = open(log_filename, "rb")
		# Set pointer to OEM ID
		file.seek(26,0)
		bps = file.readline(2)
		#CONV DATA CONTAINS BYTES PER SECTOR
		convData = struct.unpack("<h", bps)[0]
		print(f'Number of heads on drive: {convData}')
		# Close opend file
		file.close()

	def totalSectors(self):
		## Total Sectors
		# Open a file
		file = open(log_filename, "rb")
		# Set pointer to OEM ID
		file.seek(40,0)
		bps = file.readline(2)
		#CONV DATA CONTAINS BYTES PER SECTOR
		convData = struct.unpack("<h", bps)[0]
		print(f'Total Sectors: {convData}')
		# Close opend file
		file.close()
		return convData

	def MFTcluster(self):
		# Cluster containing MFT
		# Open a file
		file = open(log_filename, "rb")
		# Set pointer to OEM ID
		file.seek(48,0)
		bps = file.readline(4)
		#CONV DATA CONTAINS BYTES PER SECTOR
		convData = struct.unpack("<i", bps)[0]
		print(f'$MFT Cluster: {convData}')
		# Close opend file
		file.close()
		return convData


	def MFTMirrorCluster(self):
		# Cluster containing MFT Mirror
		# Open a file
		file = open(log_filename, "rb")
		# Set pointer to OEM ID
		file.seek(56,0)
		bps = file.readline(4)
		#CONV DATA CONTAINS BYTES PER SECTOR
		convData = struct.unpack("<i", bps)[0]
		print(f'$MFT Mirror Cluster: {convData}')
		# Close opend file
		file.close()
		return convData

	def volumeSerial(self):
		## VOLUME SERIAL NUMBER
		# Open a file
		file = open(log_filename, "rb")
		# Set pointer to OEM ID
		file.seek(72,0)
		bps = file.readline(2)
		# CONV DATA CONTAINS BYTES PER SECTOR
		convData = struct.unpack("<h", bps)[0]
		print(f'Volume Serial Number: {convData}')
		# Close opend file
		file.close()

	def getAll(self):
		file = open(log_filename, "rb")
		file.seek(3, 0)
		OEMID = file.readline(8).decode('ansi')
		file.seek(11,0)
		bps = file.readline(2)
		bytespersec = struct.unpack("<h", bps)[0]
		file.seek(13,0)
		spc = file.readline(2)
		sectorspercluster = struct.unpack("<h", spc)[0]
		file.seek(24,0)
		spt = file.readline(2)
		secpertrack = struct.unpack("<h", spt)[0]
		file.seek(26,0)
		hpt = file.readline(2)
		headsPerTrack = struct.unpack("<h", hpt)[0]
		file.seek(40,0)
		ts = file.readline(2)
		totalSectorCount = struct.unpack("<h", ts)[0]
		file.seek(48,0)
		mft = file.readline(4)
		mftCluster = struct.unpack("<i", mft)[0]
		file.seek(56,0)
		mftM = file.readline(4)
		mftMirror = struct.unpack("<i", mftM)[0]
		file.seek(72,0)
		volSer = file.readline(2)
		volSerialNum = struct.unpack("<h", volSer)[0]
		alldata = {
		'OEMID':OEMID,
		'Bytes Per Sector':bytespersec,
		'Sectors Per Cluster':sectorspercluster,
		'Sectors Per Track':secpertrack,
		'Heads Per Track':headsPerTrack,
		'Total Sectors':totalSectorCount,
		'MFT Cluster Location':mftCluster,
		'MFT Mirror Cluster':mftMirror,
		'Volume Serial Number':volSerialNum
		}
		return alldata

	def MFTExtract(self):


		convertedMFTsize = 0
		size = open(MFT_SIZE, 'r')
		for data in size:
			## solution to convert to bytes found online @ stackoverflow by user: ojii
			regex = re.compile(r'(\d+(?:\.\d+)?)\s*([kmgtp]?b)', re.IGNORECASE)

			order = ['b', 'kb', 'mb', 'gb']

			for value, unit in regex.findall(data):
				print(int(float(value) * (1024**order.index(unit.lower()))))
				convertedMFTsize = int(float(value) * (1024**order.index(unit.lower())))

			############################################################################

		self.results.append(convertedMFTsize)
		

		count = 0
		length = 0
		MFTrecords = []

		# GET FIRST MFT FILE POSITION
		# Open volume dump or file
		file = open("C:/scriptlog/volumeDump.txt", "rb")
		# Read full file
		s = file.read()
		# Find first 'FILE0' string, contains offset position
		firstMFToffset = s.find(b'FILE')
		#Close the file
		file.close()
		# print(firstMFToffset)
		self.results.append(firstMFToffset)
		#Re-Open the file, but now locate the records
		MFT = open("C:/scriptlog/volumeDump.txt", "rb")
		# Read from the offset
		MFT.seek(firstMFToffset,0)
		# Read the first 1024 bytes then iterate by
		while True:
			if length >= convertedMFTsize:
				break
			else:
				record = MFT.read(1024)
				if not record:
					break

				MFTrecords.append(record)
				length += 1024
				count += 1

		MFT.close()

		self.results.append(count)

		MFTdump = open("C:/scriptlog/MFTrecord.txt", "wb")
		for MFTfile in tqdm(MFTrecords):
			MFTdump.write(MFTfile)

		MFTdump.close()
		
		print('Findings:')	
		print(f'The MFT Size: {self.results[0]} bytes. The Offset for the first MFT record: {self.results[1]}. There are currently {self.results[2]} records in the MFT')
		print('You can find the file in the c:/scriptlog directory on your machine')
		

	def menu(self):
		print('================ Chris Troys NTFS File system data collector ===============')
		print('Please follow the instructions carefully:')
		print('1). Get OEM ID')
		print('2). Get Bytes Per Sector')
		print('3). Get sectors per cluster')
		print('4). Get heads per track')
		print('5). Total sectors')
		print('6). MFT Cluster')
		print('7). MFT Mirror cluster')
		print('8). Volume Serial')
		print('9). Get all')
		print('10). Extract MFT Records')
		print('=======================================================================')
		user = input('Please pick a number from the list: ')
		return user



NTFSinfo()

