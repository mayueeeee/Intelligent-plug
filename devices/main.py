from handler import Util
from providers import Firebase,Line
from providers import GPIO,LCD,Sensor
from threading import Thread
from datetime import datetime
import time
import requests
fallback_mode = False
outlet1 = True # Active Low relay
outlet2 = True # Active Low relay
temp = 26
light = 50
humid = 50
time = '20:00,23:00'
power = 10

outlet1_data = None
outlet2_data = None

isTimeSet1=False
isTimeSet2=False
def init():
    # Check internet connection and get saved data from Firebase    
    if Util.checkConnection():        
        global outlet1_data,outlet2_data
        outlet1_data,outlet2_data = Firebase.getPlugData()
        print('Init data:', outlet1_data,outlet2_data)

def connection_thread():
    global fallback_mode
    while True:
        #Check Internet connection before enable online features
        try:            
            if not Util.checkConnection():
                print('Running in fallback mode')
                fallback_mode = True
        except requests.ConnectionError:
            raise
            
def read_sensor_thread():
    global fallback_mode,outlet1,outlet2
    global temp,humid,light,power
    while True:
        humid, temp = Sensor.getDHT()
        # print('DHT: ',humid, temp)
        current = Sensor.getCurrent()
        voltage = Sensor.getVoltage()
        power = Sensor.getVoltage()*Sensor.getCurrent()
        # print('Power: ',power,'From',current,voltage)
        # print('LDR',Sensor.getLDR())
        light = Sensor.getLDR()
        if not GPIO.readSwitch1():
            outlet1= not outlet1
            Firebase.updatePlugStatus(1,outlet1) 
        if not GPIO.readSwitch2():
            outlet2= not outlet2
            Firebase.updatePlugStatus(2,outlet2) 
        # print('SW1',GPIO.readSwitch1(),'SW2',GPIO.readSwitch2())        

def display_thread():
    global temp,humid,light,power
    while True:        
        line2 = 'Temp{0:0.1f} Humid{1:0.1f}%'.format(temp, humid)
        # print(line2)
        line3 = 'Light{0:0.1f}% Volt{1:0.1f}%'.format(light, Sensor.getVoltage())
        LCD.print('IntelliPlug^_^',line2,line3,'    ')
        

def main_thread():
    global fallback_mode,outlet1,outlet2,outlet1_data,outlet2_data
    global humid,light,temp,time,isTimeSet1,isTimeSet2
    while True:
        # Online features
        if fallback_mode is False: 
            # Manual - Outlet1
            if outlet1_data['mode'] == 1:    
                if outlet1 is not outlet1_data['status']:
                    outlet1 = outlet1_data['status']
                    # Firebase.updatePlugStatus(1,outlet1)    
                    Line.send('เต้ารับ1ถูก'+Util.boolToString(True,outlet1)+'ผ่านเว็บละจ้า')                                                            
                    # print('1 manual control')
            # Manual - Outlet2
            if outlet2_data['mode'] == 1:    
                if outlet2 is not outlet2_data['status']:
                    outlet2 = outlet2_data['status']
                    # Firebase.updatePlugStatus(2,outlet1)    
                    Line.send('เต้ารับ2ถูก'+Util.boolToString(True,outlet2)+'ผ่านเว็บละจ้า')                                                            
                    # print('2 manual control')                  
            
            # Temperature condition - Outlet1           
            if outlet1_data['mode'] == 2:                
                if outlet1_data['setting'][0:1] == '+':
                    if temp >= float(outlet1_data['setting'][1:9]):
                        #Set GPIO to On  
                        outlet1 = False
                        if outlet1 is not outlet1_data['status']:
                            Firebase.updatePlugStatus(1,outlet1)    
                            Line.send('เต้ารับ1ถูก'+Util.boolToString(True,outlet1)+'เนื่องจากอุณหภูมิห้องสูงกว่า'+outlet1_data['setting'][1:9]+'°C\nฉันร้อนจังเลยพี่ชาย')                                                            
                            # print(temp,'More than',outlet1_data['setting'][1:9])
                    else:
                        #Set GPIO Off
                        outlet1 = True                                                                                                                                                                                                                                                                                                  
                        if outlet1 is not outlet1_data['status']:
                            Firebase.updatePlugStatus(1,outlet1)    
                            Line.send('เต้ารับ1ถูก'+Util.boolToString(True,outlet1)+'เนื่องจากอุณหภูมิห้องต่ำกว่า'+outlet1_data['setting'][1:9]+'°C\nฉันหนาวจน(ตัว)จะแข็งล้าวววว')                                                            
                            # print(temp,'less than',outlet1_data['setting'][1:9])            
            # Temperature condition - Outlet2           
            if outlet2_data['mode'] == 2:                
                if outlet2_data['setting'][0:1] == '+':
                    if temp >= float(outlet2_data['setting'][1:9]):
                        #Set GPIO to On  
                        outlet2 = False
                        if outlet2 is not outlet2_data['status']:
                            Firebase.updatePlugStatus(2,outlet2)    
                            Line.send('เต้ารับ2ถูก'+Util.boolToString(True,outlet2)+'เนื่องจากอุณหภูมิห้องสูงกว่า'+outlet2_data['setting'][1:9]+'°C\nฉันร้อนจังเลยพี่ชาย😓')                                                      
                            # print(temp,'More than',outlet2_data['setting'][1:9])
                    else:
                        outlet2 = True
                        if outlet2 is not outlet2_data['status']:
                            Firebase.updatePlugStatus(2,outlet2)    
                            Line.send('เต้ารับ2ถูก'+Util.boolToString(True,outlet2)+'เนื่องจากอุณหภูมิห้องต่ำกว่า'+outlet2_data['setting'][1:9]+'°C\nฉันหนาวจน(ตัว)จะแข็งล้าวววว😝')                                                         
                            # print(temp,'less than',outlet2_data['setting'][1:9])
            
            # Light condition - Outlet1           
            if outlet1_data['mode'] == 3:           
                if outlet1_data['setting'][0:1] == '+':
                    if light >= float(outlet1_data['setting'][1:9]):
                        #Set GPIO to On  
                        outlet1 = False
                        if outlet1 is not outlet1_data['status']:
                            Firebase.updatePlugStatus(1,outlet1)    
                            Line.send('เต้ารับ 1 ถูก'+Util.boolToString(True,outlet1)+'เนื่องจากแสงสว่างภายในห้องมากกว่า'+outlet1_data['setting'][1:9]+'%')                                                            
                            # print(light,'More than',outlet1_data['setting'][1:9])
                    else:
                        outlet1 = True
                        if outlet1 is not outlet1_data['status']:
                            Firebase.updatePlugStatus(1,outlet1)    
                            Line.send('เต้ารับ 1 ถูก'+Util.boolToString(True,outlet1)+'เนื่องจากแสงสว่างภายในห้องน้อยกว่า'+outlet1_data['setting'][1:9]+'%')                                                            
                            # print(light ,'less than',outlet1_data['setting'][1:9])            
            # Light condition - Outlet2           
            if outlet2_data['mode'] == 3:                
                if outlet2_data['setting'][0:1] == '+':
                    if light >= float(outlet2_data['setting'][1:9]):
                        #Set GPIO to On  
                        outlet2 = False
                        if outlet2 is not outlet2_data['status']:
                            Firebase.updatePlugStatus(2,outlet2)    
                            Line.send('เต้ารับ 2 ถูก'+Util.boolToString(True,outlet2)+'เนื่องจากแสงสว่างภายในห้องมากกว่า'+outlet2_data['setting'][1:9]+'%')                                                            
                            # print(light,'More than',outlet2_data['setting'][1:9])
                    else:
                        outlet2 = True
                        if outlet2 is not outlet2_data['status']:
                            Firebase.updatePlugStatus(2,outlet2)    
                            Line.send('เต้ารับ 2 ถูก'+Util.boolToString(True,outlet2)+'เนื่องจากแสงสว่างภายในห้องน้อยกว่า'+outlet2_data['setting'][1:9]+'%')                                                            
                            # print(light,'less than',outlet2_data['setting'][1:9])        
            
            # Time - Outlet1
            if outlet1_data['mode'] == 4:
            # if True:
                time_array = [x.strip() for x in outlet1_data['setting'].split(',')]
                # print(time_array)
                now = datetime.now()  
                if not isTimeSet1:             
                    on_time = datetime.strptime(time_array[0], "%H:%M")
                    on_time = now.replace(hour=on_time.time().hour, minute=on_time.time().minute, second=on_time.time().second, microsecond=0)
                    off_time = datetime.strptime(time_array[1], "%H:%M")
                    off_time = now.replace(hour=off_time.time().hour, minute=off_time.time().minute, second=off_time.time().second, microsecond=0)
                # print('ON:',on_time)
                # print('Off:',off_time)
                if (now > on_time and outlet1 is True):
                    outlet1 = False
                    on_time = now.replace(day = on_time.date().day+1)
                    isTimeSet1 = True
                    if outlet1 is not outlet1_data['status']:                                                
                        Firebase.updatePlugStatus(1,outlet1)    
                        Line.send('กริ๊งๆ ช่อง 1 ถึงเวลา'+Util.boolToString(True,outlet1)+'แล้วจ้า⏰')   
                if (now > off_time and outlet1 is False):
                    outlet1 = True
                    off_time = now.replace(day = off_time.date().day+1)
                    isTimeSet1 = True
                    if outlet1 is not outlet1_data['status']:                                                 
                        Firebase.updatePlugStatus(1,outlet1)    
                        Line.send('กริ๊งๆ ช่อง 1 ถึงเวลา'+Util.boolToString(True,outlet1)+'แล้วจ้า🕜')          
            # Time - Outlet2
            if outlet2_data['mode'] == 4:
            # if True:
                time_array = [x.strip() for x in outlet2_data['setting'].split(',')]
                print(time_array)
                now = datetime.now()  
                if not isTimeSet2:             
                    on_time = datetime.strptime(time_array[0], "%H:%M")
                    on_time = now.replace(hour=on_time.time().hour, minute=on_time.time().minute, second=on_time.time().second, microsecond=0)
                    off_time = datetime.strptime(time_array[1], "%H:%M")
                    off_time = now.replace(hour=off_time.time().hour, minute=off_time.time().minute, second=off_time.time().second, microsecond=0)
                # print('ON:',on_time)
                # print('Off:',off_time)
                if (now > on_time and outlet2 is True):
                    outlet2 = False
                    on_time = now.replace(day = on_time.date().day+1)
                    isTimeSet2 = True
                    if outlet1 is not outlet2_data['status']:                                                
                        Firebase.updatePlugStatus(1,outlet2)    
                        Line.send('กริ๊งๆ ช่อง 2 ถึงเวลา'+Util.boolToString(True,outlet1)+'แล้วจ้า⏰')   
                if (now > off_time and outlet2 is False):
                    outlet2 = True
                    off_time = now.replace(day = off_time.date().day+1)
                    isTimeSet2 = True
                    if outlet2 is not outlet1_data['status']:                                                 
                        Firebase.updatePlugStatus(1,outlet1)    
                        Line.send('กริ๊งๆ ช่อง 1 ถึงเวลา'+Util.boolToString(True,outlet1)+'แล้วจ้า🕜')

            # Load data from firebase
            outlet1_data,outlet2_data = Firebase.getPlugData()
            # humid,light,temp,time = Firebase.getData()
            # print('Update data:', outlet1_data,outlet2_data)
            # print('Mock: ',humid,light,temp,time)
            GPIO.setSwitch(1,outlet1)
            GPIO.setSwitch(2,outlet2)


thread1 = Thread( target=connection_thread )
thread2 = Thread( target=main_thread )
thread3 = Thread( target=display_thread )
thread4 = Thread( target=read_sensor_thread)

try:
    #Try to get data from Firebase first time
    init()
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    
except KeyboardInterrupt:        
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    print ("threads successfully closed")
    