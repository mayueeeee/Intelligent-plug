import random
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import Adafruit_DHT
SAMPLING =300
VOFFSET  =512 
ADC_PIN = 'A0'
AMPLITUDE =350
REAL_VAC  =225
# Software SPI configuration:
CLK  = 11
MISO = 9
MOSI = 10
CS   = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

sensor = Adafruit_DHT.DHT22
pin = 14

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
def read_VAC():  
  adc_max = 0
  adc_min = 1023  
  for x in range(SAMPLING):  
    adc = mcp.read_adc(2)
    if(adc > adc_max):    
        adc_max = adc    
    if(adc < adc_min):
        adc_min = adc   
  return adc_max-adc_min;   

def getVoltage():
    v=0
    read = read_VAC()
    mapp = map(read,0,AMPLITUDE,0,REAL_VAC*100.00)/100.00    
    return mapp

def getCurrent():
    a = 0
    for x in range(1000):
        a = a + (0.025 * mcp.read_adc(1) -13.51) / 10000
    return a

def getDHT():
    humid, temp = Adafruit_DHT.read_retry(sensor, pin)
    return humid, temp

def getLDR():
    return ((mcp.read_adc(0)-100)/(1023))*100