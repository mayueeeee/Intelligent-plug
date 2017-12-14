import requests
def checkConnection():
    print('chk')
    try:
        r = requests.get('https://google.com', timeout=15)
        # print(True)
        return True        
    except requests.ConnectionError:
        # print(False)
        return False
    except requests.exceptions.Timeout:
        # print(False)
        return False

def wattCalculate(voltage,current):
    return voltage*current
def boolToString(bool1,bool2):
    if bool1 is True and bool2 is False:
        return 'เปิด'
    return 'ปิด'