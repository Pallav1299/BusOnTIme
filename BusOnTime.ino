#include <HTTPSRedirect.h>
#include <ESP8266WiFi.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>
/*
   This sample sketch demonstrates the normal use of a TinyGPS++ (TinyGPSPlus) object.
   It requires the use of SoftwareSerial, and assumes that you have a
   4800-baud serial GPS device hooked up on pins 4(rx) and 3(tx).
*/
static const int RXPin = 5, TXPin = 4;
static const uint32_t GPSBaud = 9600;

// The TinyGPS++ object
TinyGPSPlus gps;

// The serial connection to the GPS device
SoftwareSerial ss(RXPin, TXPin);

String latitude, longitude;

String lat_str, lng_str;
String location_tuple;

const char* ssid = "baba";
const char* password = "poiuytrewq";

// The ID below comes from Google Sheets, where the data will be posted

const char *GScriptId = "AKfycby0PSqsjIJskJucORycdCq-PkzTZS7Q9bv3giw5dxpt7xQymcQ";


// Push data on this interval
const int dataPostDelay = 2000;  // 1 minutes = 1 * 60 * 1000;

const char* host = "script.google.com";
const char* googleRedirHost = "script.googleusercontent.com";

const int httpsPort =     443;
HTTPSRedirect client(httpsPort);
String bus_no = "CH-04-AG-8512";

// Prepare the url (without the varying data)
String url = String("/macros/s/") + GScriptId + "/exec?";



void setup()
{
  Serial.begin(115200);
  ss.begin(GPSBaud);

Serial.println("BUS ON TIME");

connectToWifi();

}

void connectToWifi(){
  Serial.println("Connecting to wifi: ");
  Serial.println(ssid);
  Serial.flush();

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" IP address: ");
  Serial.println(WiFi.localIP());

  
  Serial.print(String("Connecting to "));
  Serial.println(host);

  bool flag = false;
  for (int i=0; i<5; i++){
    int retval = client.connect(host, httpsPort);
    if (retval == 1) {
       flag = true;
       break;
    }
    else
      Serial.println("Connection failed. Retrying...");
  }

  // Connection Status, 1 = Connected, 0 is not.
  Serial.println("Connection Status: " + String(client.connected()));
  Serial.flush();
  
  if (!flag){
    Serial.print("Could not connect to server: ");
    Serial.println(host);
    Serial.println("Exiting...");
    Serial.flush();
    return;
  }
}


// This is the main method where data gets pushed to the Google sheet
void postData(String tag, String Value)
//String tag, float value
{
  //float Latitude, float Longitude, float PPM, float Temperature, float Humidity
  if (!client.connected()){
    Serial.println("Connecting to client again..."); 
    client.connect(host, httpsPort);
  }
  String urlFinal = url + "&tag=" + String(bus_no) + "&Value=" + String(Value);
  client.printRedir(urlFinal, host, googleRedirHost);
  Serial.print("URL generated:-");
  Serial.println(urlFinal);
}

void collect_gps_data()
{
  Serial.print(F("Location: ")); 
  if (gps.location.isValid())
  {
    latitude = String(gps.location.lat(),4);
    longitude = String(gps.location.lng(),4);
    
    location_tuple = "(" + String(latitude) + "," + String(longitude) + ")";
    Serial.print(latitude);
    Serial.print(F(","));
    Serial.print(longitude);
    Serial.println(location_tuple);
    postData(bus_no,location_tuple);
    dataPostDelay;
  }
  else
  {
    Serial.print(F("INVALID"));
  }
}

void loop()
{
  // This sketch displays information every time a new sentence is correctly encoded.
  while (ss.available() > 0)
    if (gps.encode(ss.read()))
      collect_gps_data();

  if (millis() > 5000 && gps.charsProcessed() < 10)
  {
    Serial.println(F("No GPS detected: check wiring."));
    while(true);
  }

  /*
    latitude = 36.75;
    longitude = 76.76;
    location_tuple = "(" + String(latitude) + "," + String(longitude) + ")";
    
  Serial.println(location_tuple);

  Serial.println(latitude);
Serial.println(longitude);
Serial.println(lat_str);
Serial.println(lng_str);
*/
/*
Serial.println(location_tuple);
postData(bus_no,location_tuple);
dataPostDelay;
*/
  

}
