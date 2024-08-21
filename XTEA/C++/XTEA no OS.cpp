#include <Crypto.h>
#include <Arduino.h>
#include "hardware/clocks.h"
#include "pico/bootrom.h"
#include "pico.h"
#include <string.h>
#define XTEA_ROUNDS 48
#define XTEA_MAC_ROUNDS 24
#include "XTEA-Cipher.h"

#define XTEA_BLOCK_SIZE 8
#define XTEA_IV_SIZE 8
#define XTEA_KEY_SIZE 16

unsigned long encryptStartTime;
unsigned long encryptEndTime;
unsigned long encryptElapsedMicros;
unsigned long decryptStartTime;
unsigned long decryptEndTime;
unsigned long decryptElapsedMicros;

uint8_t iv[XTEA_IV_SIZE] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07};

uint8_t key[XTEA_KEY_SIZE] = {
    0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
    0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10};

int data_size = 16;
char packet[512];
char packet16[] = "sixteenbytetext";
char packet32[] = "sixteenbytetextsixteenbytestext";
char packet64[] = "sixteenbytetextsixteenbytestextsixteenbytestextsixteenbytestext";
char packet128[] = "sixteenbytetextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestext";
char packet256[] = "sixteenbytetextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestext";
char packet512[] = "sixteenbytetextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestextsixteenbytestext";
int packetSize = 0;

void time_output() {
    Serial.print("E ");
    Serial.print(encryptElapsedMicros);
    Serial.print("  D ");
    Serial.println(decryptElapsedMicros);
}

void decrypted_output(uint8_t* buffer, size_t size) {
    Serial.print("Decrypted message: ");
    for (size_t i = 0; i < size; ++i) {
        Serial.print((char)buffer[i]);
    }
    Serial.println();
}

void setup() {
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

    Serial.begin(9600);
    Serial.println(" ");
    Serial.print("No OS || ");
    Serial.print(clock_get_hz(clk_sys) / 1000000);
    Serial.print("mhz || ");
    Serial.print("XTEA");
    packetSize = strlen(packet);
    Serial.print(" || datasize ");
    Serial.println(packetSize + 1);
}

void loop() {
    uint8_t resultBuffer[data_size];
    memcpy(resultBuffer, packet, data_size);

    encryptStartTime = micros();
    xtea.ecbEncrypt(key, resultBuffer, data_size);
    encryptEndTime = micros();
    encryptElapsedMicros = encryptEndTime - encryptStartTime;

    decryptStartTime = micros();
    xtea.ecbDecrypt(key, resultBuffer, data_size);
    decryptEndTime = micros();
    decryptElapsedMicros = decryptEndTime - decryptStartTime;

    time_output();
    decrypted_output(resultBuffer, data_size);
    delay(3000);
}

