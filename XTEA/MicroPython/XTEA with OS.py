import pyRTOS
import machine
import utime
import uos
from xtea_cipher import *
from time import sleep
baton = pyRTOS.mutex()
freq = 200000000
printfreq = int(str(freq)[:3])
datasize = 16
plain = ""
plain16 = "sixteenbytetext"
plain32 = "sixteenbytetextsixteenbytestext"
plain64 = "sixteenbytetextsixteenbytestextsixteenbytestextsixteenbytestext"
plain128 = "sixteenbytetextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestext"
plain256 = "sixteenbytetextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestext"
plain512 = "sixteenbytetextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestext"

key = bytearray([
    0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 
    0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10
])

iv = bytearray([
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07
])
encryptedString = ""
encryptFuncStartTime = 0
encryptTaskStartTime = 0
encryptFuncEndTime = 0
encryptTaskEndTime = 0
encryptFuncElapsedMicros = 0
encryptTaskElapsedMicros = 0
encryptElapsedMicros = 0
machine.freq(freq)
print("With OS || ", printfreq, "mhz || ", "XTEA", " || datasize ", datasize)

def encryptData(data):
	global encryptFuncStartTime, encryptFuncEndTime, encryptFuncElapsedMicros
	encryptFuncStartTime = utime.ticks_us()
    data_bytes = bytes(data, 'utf-8')
    cipher = aes(key, MODE_ECB, iv)
    encryptedData = cipher.encrypt(data_bytes)
	encryptFuncEndTime = utime.ticks_us()
	encryptFuncElapsedMicros = encryptFuncEndTime - encryptFuncStartTime
    return encryptedData

def decryptData(encryptedData):
    decipher = xtea(key, MODE_ECB, iv)
    decryptedData = decipher.decrypt(encryptedData)
    return decryptedData.strip().decode('utf-8')

def enc_task(self):
	global encryptedString, encryptTaskStartTime, encryptTaskEndTime, encryptTaskElapsedMicros
    baton.lock()
    encryptTaskStartTime = utime.ticks_us()
    global encryptedString
    encryptedString = encryptData(plain)
    encryptTaskEndTime = utime.ticks_us()
    encryptTaskElapsedMicros = encryptTaskEndTime - encryptTaskStartTime
    baton.unlock()
    return encryptedString
	yield

def dec_task(self):
    baton.lock()
    global encryptedString
    baton.unlock()
    return decryptedString
	yield
        
if datasize == 16:
    plain = plain16
elif datasize == 32:
    plain = plain32
elif datasize == 64:
    plain = plain64
elif datasize == 128:
    plain = plain128
elif datasize == 256:
    plain = plain256
elif datasize == 512:
    plain = plain512		

while True:
	yield [pyRTOS.timeout(0.5)]
		if self.name == "enc_task":
			target = "dec_task"
		else:
			target = "enc_task"
		
	yield [pyRTOS.wait_for_message(self)]
	
	pyRTOS.add_task(pyRTOS.Task(enc_task, name="encryption",mailbox=True))
	pyRTOS.add_task(pyRTOS.Task(dec_task, name="encryption",mailbox=True))
	pyRTOS.start()

    encryptElapsedMicros = encryptTaskElapsedMicros + encryptFuncElapsedMicros
#    print(decryptedString)
    print('E', encryptElapsedMicros)
    utime.sleep_ms(3000)
