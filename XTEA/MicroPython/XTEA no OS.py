import machine
import utime
import uos
from xtea_cipher import *

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
encryptStartTime = 0
encryptEndTime = 0
encryptElapsedMicros = 0
decryptStartTime = 0
decryptEndTime = 0
decryptElapsedMicros = 0

machine.freq(freq)
print("No OS || ", printfreq, "mhz || ", "XTEA", " || datasize ", datasize)

def decryptData(encryptedData):
    decipher = aes(key, MODE_CBC, iv)
    decryptedData = decipher.decrypt(encryptedData)
    return decryptedData.strip().decode('utf-8')
   
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
	data_bytes = bytes(data, 'utf-8')
    cipher = xtea(key, MODE_ECB, iv)
	encryptStartTime = utime.ticks_us()
    encryptedData = cipher.encrypt(data_bytes) 
    encryptEndTime = utime.ticks_us()
    encryptElapsedMicros = encryptEndTime - encryptStartTime
	decipher = xtea(key, MODE_ECB, iv)
	decryptStartTime = utime.ticks_us()
    decryptedData = decipher.decrypt(encryptedData)
    decryptEndTime = utime.ticks_us()
    decryptElapsedMicros = decryptEndTime - decryptStartTime
    
#     print(decryptedData)
    print('E', encryptElapsedMicros, 'D', decryptElapsedMicros)
    utime.sleep_ms(3000)
