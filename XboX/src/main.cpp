#include <Arduino.h>
#include <ps2dev.h>

#define LOOP_DELAY_MS           33 // ~30 fps pedal pooling (1s / 30f = 0.033s (* 1000ms = 30ms))

#define PEDAL_ACCEL_PIN         A2
#define PEDAL_BRAEK_PIN         A0
#define PEDAL_CLUTH_PIN         A1

#define TOLERANCE_RAW_PC        2  // (2%) Pedal prev->curr value change in %, to "trigger" action
#define PEDAL_ACCEL_ACTION_PC   50
#define PEDAL_BRAEK_ACTION_PC   10
#define PEDAL_CLUTH_ACTION_PC   35 // how much +variance in cluth pedal to consider a "press"

#define KB_CLK_PIN DD2
#define KB_DAT_PIN DD3

unsigned long lastExecutedMillis = 0;
unsigned long currentMillis = 0;
char out_buf[256]; // holds the temp str for sprintf

int curr_accel_raw = 0, prev_accel_raw = 0;
float chg_accel_raw = 0.00F;
int chg_accel_pct = 0;

int curr_braek_raw = 0, prev_braek_raw = 0;
float chg_braek_raw = 0.00F;
int chg_braek_pct = 0;

int curr_cluth_raw = 0, prev_cluth_raw = 0;
float chg_cluth_raw = 0.00F;
int chg_cluth_pct = 0;

PS2dev keyboard(KB_CLK_PIN, KB_DAT_PIN); // clock, data
unsigned char leds;
bool kb_f3_pressed = false;

void setup()
{
  pinMode(PEDAL_ACCEL_PIN, INPUT);
  pinMode(PEDAL_BRAEK_PIN, INPUT);
  pinMode(PEDAL_CLUTH_PIN, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600);
  // while (!Serial.available())
  //   yield;
  Serial.println("Serial initialized!");
  Serial.flush();

  keyboard.keyboard_init();
  Serial.println("Keyboard initialized!");
}

void loop()
{
  currentMillis = millis();
  if (currentMillis - lastExecutedMillis >= LOOP_DELAY_MS)
  {
    lastExecutedMillis = currentMillis;
    // -----------------------------------------------------
    // We have saved from previous loop:
    // prev_accel_raw
    // prev_braek_raw
    // prev_cluth_raw

    // New readings ...
    curr_accel_raw = analogRead(PEDAL_ACCEL_PIN);
    curr_braek_raw = analogRead(PEDAL_BRAEK_PIN);
    curr_cluth_raw = analogRead(PEDAL_CLUTH_PIN);

    // Calculate change from prev. val. for change tolerance
    //     negative (-) values are for "retreating" the pedal, ...
    // ... positive (+) values are for stepping on the pedal
    // Ranges from -100%, 0%, +100%.
    if (prev_accel_raw < curr_accel_raw)
    {
      chg_accel_raw = (float)prev_accel_raw / (float)curr_accel_raw - 1.00F;
    }
    else
    {
      chg_accel_raw = 1.00F - (float)curr_accel_raw / (float)(prev_accel_raw);
    }
    chg_accel_pct = chg_accel_raw * 100;

    if (prev_braek_raw < curr_braek_raw)
    {
      chg_braek_raw = (float)prev_braek_raw / (float)curr_braek_raw - 1.00F;
    }
    else
    {
      chg_braek_raw = 1.00F - (float)curr_braek_raw / (float)(prev_braek_raw);
    }
    chg_braek_pct = chg_braek_raw * 100;

    if (prev_cluth_raw < curr_cluth_raw)
    {
      chg_cluth_raw = (float)prev_cluth_raw / (float)curr_cluth_raw - 1.00F;
    }
    else
    {
      chg_cluth_raw = 1.00F - (float)curr_cluth_raw / (float)(prev_cluth_raw);
    }
    chg_cluth_pct = chg_cluth_raw * 100;

    if ((abs(chg_accel_pct) > TOLERANCE_RAW_PC) || (abs(chg_braek_pct) > TOLERANCE_RAW_PC) || (abs(chg_cluth_pct) > TOLERANCE_RAW_PC))
    {
      sprintf(out_buf, "ACCEL: %4d (%+3d%%)\t|\tBREAK: %4d (%+3d%%)\t|\tCLUTH: %3d (%+2d%%)",
              curr_accel_raw, chg_accel_pct,
              curr_braek_raw, chg_braek_pct,
              curr_cluth_raw, chg_cluth_pct);
      Serial.println(out_buf);
    }

    if (chg_accel_pct > PEDAL_ACCEL_ACTION_PC)
    {
      keyboard.keyboard_press(PS2dev::LEFT_CONTROL);
      keyboard.keyboard_mkbrk(PS2dev::R);
      keyboard.keyboard_release(PS2dev::LEFT_CONTROL);
    }

    if (chg_braek_pct > PEDAL_BRAEK_ACTION_PC)
    {
      keyboard.keyboard_mkbrk(PS2dev::F4);
    }

    if (chg_cluth_pct > PEDAL_CLUTH_ACTION_PC)
    {
      keyboard.keyboard_mkbrk(PS2dev::F3);
    }

    // Save the current raw values for the next loop as prev_*
    prev_accel_raw = curr_accel_raw;
    prev_braek_raw = curr_braek_raw;
    prev_cluth_raw = curr_cluth_raw;
    // -----------------------------------------------------

    if (keyboard.keyboard_handle(&leds))
    {
      digitalWrite(LED_BUILTIN, leds);
    }
  }
}
