#include <Crypto.h>
#include <Arduino.h>
#include "hardware/clocks.h"
#include "pico/bootrom.h"
#include "pico.h"
#include <FreeRTOS.h>
#include <semphr.h>
#include <string.h>

#define AES_KEY_LENGTH_256 32
#define AES_KEY_LENGTH_128 16
#define AES_BLOCK_SIZE 16

SemaphoreHandle_t doneEncryptingSemaphore;
SemaphoreHandle_t doneDecryptingSemaphore;

int aes_type = 256;
int data_size = 256;
unsigned long encryptFuncStartTime;
unsigned long encryptTaskStartTime;
unsigned long encryptFuncEndTime;
unsigned long encryptTaskEndTime;
unsigned long encryptFuncElapsedMicros;
unsigned long encryptTaskElapsedMicros;
unsigned long encryptElapsedMicros;

unsigned long decryptFuncStartTime;
unsigned long decryptTaskStartTime;
unsigned long decryptFuncEndTime;
unsigned long decryptTaskEndTime;
unsigned long decryptFuncElapsedMicros;
unsigned long decryptTaskElapsedMicros;
unsigned long decryptElapsedMicros;

char packet[512];
char packet16[] = "sixteenbytetext";
char packet32[] = "sixteenbytetextsixteenbytestext";
char packet64[] = "sixteenbytetextsixteenbytestextsixteenbytestextsixteenbytestext";
char packet128[] = "sixteenbytetextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestext";
char packet256[] = "sixteenbytetextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestext";
char packet512[] = "sixteenbytetextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestext";

int packetSize = 0;
int padSize = 0;
int encryptedSize = 0;
uint8_t *encrypted;
uint8_t *decrypted;
uint8_t *keyEncrypt;
uint8_t iv[] = {
  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
  0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F
};
uint8_t key128[AES_KEY_LENGTH_128] = {
  0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
  0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10
};
uint8_t key256[AES_KEY_LENGTH_256] = {
  0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
  0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10,
  0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
  0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10
};

void decrypted_output(){
    Serial.print("Decrypted: ");
    for (int i = 0; i < encryptedSize - padSize; i++) { 
        Serial.print((char)decrypted[i]);
    }
    Serial.println();
}

void EncryptTask( void *pvParameters ){    
     if (xSemaphoreTake(doneDecryptingSemaphore, portMAX_DELAY) == pdTRUE){  
        encryptFuncStartTime = micros();  
        AES aesEncrypt(keyEncrypt, iv, aes_type == 128 ? AES::AES_MODE_128 : AES::AES_MODE_256, AES::CIPHER_ENCRYPT);
        aesEncrypt.process((uint8_t*)packet, encrypted, packetSize);
        xSemaphoreGive(doneEncryptingSemaphore);
        encryptFuncEndTime = micros();
        encryptFuncElapsedMicros = encryptFuncEndTime - encryptFuncStartTime;
        vTaskDelete(NULL);
    }
}

void DecryptTask( void *pvParameters ){
    if (xSemaphoreTake(doneEncryptingSemaphore, portMAX_DELAY) == pdTRUE) {
        decryptFuncStartTime = micros();
        AES aesDecrypt(keyEncrypt, iv, aes_type == 128 ? AES::AES_MODE_128 : AES::AES_MODE_256, AES::CIPHER_DECRYPT);
        aesDecrypt.process(encrypted, decrypted, encryptedSize);
        xSemaphoreGive(doneDecryptingSemaphore);
        decryptFuncEndTime = micros();
        decryptFuncElapsedMicros = decryptFuncEndTime - decryptFuncStartTime;
        //decrypted_output();
        vTaskDelete(NULL);
    }
}

void setup() {
    doneEncryptingSemaphore = xSemaphoreCreateBinary();
    doneDecryptingSemaphore = xSemaphoreCreateBinary();
    delay(10000);
    if (data_size == 16) {
        strcpy(packet, packet16);
    } else if (data_size == 32) {
        strcpy(packet, packet32);
    } else if (data_size == 64) {
        strcpy(packet, packet64);
    } else if (data_size == 128) {
        strcpy(packet, packet128);
    } else if (data_size == 256) {
        strcpy(packet, packet256);
    } else if (data_size == 512) {
        strcpy(packet, packet512);
    }

    Serial.println(" ");
    Serial.print("With OS || ");
    Serial.print(clock_get_hz(clk_sys) / 1000000);
    Serial.print("mhz || ");
    Serial.print("AES");
    Serial.print(aes_type);
    packetSize = strlen(packet);
    Serial.print(" || datasize ");
    Serial.println(packetSize + 1);

    padSize = (AES_BLOCK_SIZE - (packetSize % AES_BLOCK_SIZE)) % AES_BLOCK_SIZE;
    encryptedSize = packetSize + padSize;

    encrypted = new uint8_t[encryptedSize];
    decrypted = new uint8_t[encryptedSize];

    if (aes_type == 128) {
        keyEncrypt = key128;
    } else if (aes_type == 256) {
        keyEncrypt = key256;
    }
    
    memset(encrypted, 0, encryptedSize);
    memset(decrypted, 0, encryptedSize);
    xSemaphoreGive(doneDecryptingSemaphore);
}

void loop() {
    encryptTaskStartTime = micros();
    xTaskCreate(
    EncryptTask
    ,  "encrypt"   
    ,  10000
    ,  NULL
    ,  1  
    ,  NULL );
    encryptTaskEndTime = micros();
    delay(1000);
    encryptTaskElapsedMicros = encryptTaskEndTime - encryptTaskStartTime;
    encryptElapsedMicros = encryptTaskElapsedMicros + encryptFuncElapsedMicros;
    Serial.print("E ");
    Serial.print(encryptElapsedMicros);

    decryptTaskStartTime = micros();
    xTaskCreate(
    DecryptTask
    ,  "decrypt"   
    ,  10000
    ,  NULL
    ,  1  
    ,  NULL );
    decryptTaskEndTime = micros();
    delay(1000);
    decryptTaskElapsedMicros = decryptTaskEndTime - decryptTaskStartTime;
    decryptElapsedMicros = decryptTaskElapsedMicros + decryptFuncElapsedMicros;
    Serial.print("  D ");
    Serial.println(decryptElapsedMicros);

}
