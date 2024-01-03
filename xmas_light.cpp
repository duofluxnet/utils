#include <Arduino.h>
#include <ESP8266WiFi.h>

#define LED 13 // D7
#define MAX_BRIGHTNESS 255
#define MIN_BRIGHTNESS 0
#define INITIAL_FADE_STEP 5

#define BASE_DELAY_MS 1
#define OFF_DELAY_MS 100
#define DELAY_FACTOR 2
#define DELAY_DIVIDER 2
#define BLINK_CYCLE_COUNT 20

const char *ssid = "GVT-2229";
const char *password = "1207148355";

WiFiServer server(61000);

int base_delay_ms;
int off_delay_ms;
int delay_factor;
int delay_divider;
int fixed_blink_cycle_count;

int max_brightness;

bool fade;
bool no_fx;

bool onoff;

// internal control
int min_brightness;
int fadeAmount;
int inverted_brightness;
int brightness;
bool state = true;
int blink_cycle_count;

void turn_led(bool state)
{
  if (state)
    analogWrite(LED, max_brightness);
  else
    analogWrite(LED, min_brightness);
}

void init_setup()
{
  brightness = MIN_BRIGHTNESS;
  fadeAmount = INITIAL_FADE_STEP;
  off_delay_ms = OFF_DELAY_MS;
  base_delay_ms = BASE_DELAY_MS;
  min_brightness = MIN_BRIGHTNESS;
  max_brightness = MAX_BRIGHTNESS;
  delay_factor = DELAY_FACTOR;
  delay_divider = DELAY_DIVIDER;
  fixed_blink_cycle_count = BLINK_CYCLE_COUNT;
  blink_cycle_count = fixed_blink_cycle_count;

  fade = false; // fading X blinking
  no_fx = false;

  onoff = true;    // Turn led-tree on or off
  turn_led(onoff); // start with led-tree ON!
}

void setup()
{
  pinMode(LED, OUTPUT);
  init_setup();

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
    delay(200);

  server.begin();
  // Serial.begin(9600);
  // Serial.println(WiFi.localIP());
}

void loop()
{

  WiFiClient client = server.accept();
  if (!client)
  {
    delay(1);
  }
  else
  {
    // Wait until the client sends some data
    while (!client.available())
      delay(1);

    String request = client.readStringUntil('\r');
    // Serial.println(request);
    client.flush();

    if (request.indexOf("/desliga") != -1)
      onoff = false;

    if (request.indexOf("/liga") != -1)
      onoff = true;

    if (request.indexOf("/pisca") != -1)
    {
      onoff = true;
      no_fx = false;
      fade = false;
    }

    if (request.indexOf("/fixa") != -1)
    {
      onoff = true;
      no_fx = true;
      fade = false;
    }

    if (request.indexOf("/efeitinho") != -1)
    {
      onoff = true;
      no_fx = false;
      fade = true;
    }

    // Return the response
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println(""); //  do not forget this one
    client.println("<!DOCTYPE HTML>");
    client.println("<html>");
    client.println("<a href=\"/liga\">LIGAR!</a><br><br>");
    client.println("<a href=\"/desliga\">DESLIGAR!</a><br><br>");
    client.println("<a href=\"/fixa\">LUZINHA FIXA</a><br><br>");
    client.println("<a href=\"/pisca\">PISCA-PISCA</a><br><br>");
    client.println("<a href=\"/efeitinho\">EFEITINHO</a><br><br>");
    client.println("</html>");
  }

  if (onoff)
  {

    if (no_fx)
    {
      turn_led(true);
      delay(1000);
    }
    else
    {

      if (fade)
      {
        analogWrite(LED, brightness);

        brightness = brightness + fadeAmount;
        if (brightness <= min_brightness || brightness >= max_brightness)
          fadeAmount = -fadeAmount;

        if (brightness == min_brightness)
        {
          turn_led(false);
          delay(off_delay_ms);
        }
        inverted_brightness = max_brightness - brightness;
        delay(base_delay_ms + (int(inverted_brightness / delay_divider) * delay_factor));
      }
      else
      {
        turn_led(state);

        if ((blink_cycle_count == 0) && (!state))
        { // only delay on the off state...
          delay(off_delay_ms * (fixed_blink_cycle_count * 2));
          blink_cycle_count = fixed_blink_cycle_count;
        }

        // a cycle is composed by ON and OFF
        if (state)
          blink_cycle_count--;

        state = !state;
        delay(off_delay_ms);
      }
    }
  }

  else if (!onoff)
  {
    turn_led(MIN_BRIGHTNESS);
  }
}