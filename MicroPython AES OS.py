import _thread
import machine
import utime
import uos
from ucryptolib import aes
from time import sleep

baton = _thread.allocate_lock()

freq = 200000000
printfreq = int(str(freq)[:3])
MODE_CBC = 2
aestype = 128
datasize = 16

plain = ""
plain16 = "sixteenbytetext"
plain32 = "sixteenbytetextsixteenbytestext"
plain64 = "sixteenbytetextsixteenbytestextsixteenbytestextsixteenbytestext"
plain128 = "sixteenbytetextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestext"
plain256 = "sixteenbytetextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestext"
plain512 = "sixteenbytetextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestext"

key = bytearray([])
key128 = bytearray([
    0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 
    0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10
])
key256 = bytearray([
    0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 
    0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 
    0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
    0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10
])
iv = bytearray([
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F
])
encryptedString = ""
encryptStartTime = 0
encryptEndTime = 0
encryptElapsedMicros = 0
decryptStartTime = 0
decryptEndTime = 0
decryptElapsedMicros = 0

machine.freq(freq)
print("With OS || ", printfreq, "mhz || ", "AES", aestype, " || datasize ", datasize)

def encryptData(data):
    data_bytes = bytes(data, 'utf-8')
    cipher = aes(key, MODE_CBC, iv)
    paddedData = bytearray(data_bytes + b" " * (16 - len(data_bytes) % 16))
    encryptedData = cipher.encrypt(paddedData)
    return encryptedData

def decryptData(encryptedData):
    decipher = aes(key, MODE_CBC, iv)
    decryptedData = decipher.decrypt(encryptedData)
    return decryptedData.strip().decode('utf-8')

def core0_enc_thread():
    baton.acquire()
    encryptStartTime = utime.ticks_us()
    global encryptedString
    encryptedString = encryptData(plain)
    encryptEndTime = utime.ticks_us()
    encryptElapsedMicros = encryptEndTime - encryptStartTime
    baton.release()
    return encryptedString

def core0_dec_thread():
    baton.acquire()
    decryptStartTime = utime.ticks_us()
    global encryptedString
    decryptedString = decryptData(encryptedString)
    decryptEndTime = utime.ticks_us()
    decryptElapsedMicros = decryptEndTime - decryptStartTime
    baton.release()
    return decryptedString
    
while True:
    if aestype == 128:
        key = key128
    elif aestype == 256:
        key = key256
    
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
    
    core0_enc_thread()
    
    core0_dec_thread()
    
#    print(decryptedString)
    print('E', encryptElapsedMicros, 'D', decryptElapsedMicros)
    utime.sleep_ms(3000)
