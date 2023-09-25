
#Libraries
import json
from time import sleep    #https://docs.python.org/fr/3/library/time.html
from adafruit_servokit import ServoKit    #https://circuitpython.readthedocs.io/projects/servokit/en/latest/

#Constants
nbPCAServo=16 
I2C_WAIT_TIME = 0.02
I2C_LEFT_ADDR = 0x40
I2C_RIGHT_ADDR = 0x41
LEFT_CONNECTED = 1
RIGHT_CONNECTED = 1

#Generic Parameters
#MIN_IMP  =[500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
#MAX_IMP  =[2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500]

#Parameters
MIN_IMP  =[600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]
MAX_IMP  =[2400, 2400, 2400, 2400, 2400, 2400, 2400, 2400, 2400, 2400, 2400, 2400, 2400, 2400, 2400, 2400]
MIN_ANG  =[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
MAX_ANG  =[180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180]

#Init servo controllers
if (LEFT_CONNECTED):
    pca_left = ServoKit(channels=16, address=I2C_LEFT_ADDR)
    for i in range(nbPCAServo):
        pca_left.servo[i].set_pulse_width_range(MIN_IMP[i] , MAX_IMP[i])         

if (RIGHT_CONNECTED):
    pca_right = ServoKit(channels=16, address=I2C_RIGHT_ADDR)
    for i in range(nbPCAServo):
        #pca.servo[i].set_pulse_width_range(MIN_IMP[i] , MAX_IMP[i]) 
        pca_right.servo[i].set_pulse_width_range(MIN_IMP[i] , MAX_IMP[i])    

#Create servos list
servos = list()
for i in range(9):
    servos.append(i)

#Operate multiple servos
def run_servos(x = 0.01): 
    for servo in range(9):
        pca.servo[servo].angle=0
        sleep(x)
    time.sleep(3)       
    for i in range(0,150,30):
        for servo in range(9):
            pca.servo[servo].angle=i
            sleep(x)
    

def run_servos2(i,x = 0.01):
    for servo in range(9):
        pca.servo[servo].angle=i
        sleep(x)



def run_servo(servo=0,x = 0.01): 
    pca.servo[servo].angle=0
    time.sleep(3)       
    for i in range(0,180,30):
        pca.servo[servo].angle=i
        sleep(x)
        
def run_right_servo(servo=0,x = 0.01): 
    pca_right.servo[servo].angle=0
    sleep(3)       
    for i in range(0,180,30):
        pca_right.servo[servo].angle=i
        sleep(x)

#pca.servo[15].angle = 0
class leg:
    def __init__(self, servo_list, left=True):
        # upper joint
        self.servos = list()
        if not left:
            pca = pca_left
        else:
            pca = pca_right
        for i, sid in enumerate(servo_list):
            self.servos.append(pca.servo[sid])
            self.servos[i].angle_0 = 30
            self.servos[i].min_ang = 0
            self.servos[i].max_ang = 60
            self.servos[i].target = self.servos[0].angle_0 
        
    def go0(self):
        for servo in self.servos:
            servo.angle = servo.angle_0   
            sleep(I2C_WAIT_TIME)
    
    def go_min(self):
        for servo in self.servos:
            servo.angle = servo.min_ang
            sleep(I2C_WAIT_TIME)
    
    def go_max(self):
        for servo in self.servos:
            servo.angle = servo.max_ang
            sleep(I2C_WAIT_TIME)
        
    def update_servo(self, i, min_ang, max_ang):
        self.servos[i].min_ang = min_ang
        self.servos[i].max_ang = max_ang
        #self.servos[i].angle_0 = min_ang+(max_ang-min_ang)/2
        self.servos[i].target = self.servos[1].angle_0 
    
    def set_servos_angles(self, angles):
        for i,ang in enumerate(angles):
            self.servos[i].angle = ang
            sleep(I2C_WAIT_TIME)
            
    def get_servos_angles(self):
        for i in range(3):
            print(self.servos[i].angle)
            sleep(I2C_WAIT_TIME)


class ant:
    def __init__(self, conf_file="conf.json"):
        self.right_front_leg = leg([0,1,2],left=False)        
        self.right_mid_leg = leg([4,5,6],left=False)        
        self.right_back_leg = leg([9,8,10],left=False)        
        self.left_front_leg = leg([9,8,10])        
        self.left_mid_leg = leg([4,5,6])        
        self.left_back_leg = leg([0,1,2])        
        self.legs = {
                "left":{
                    "front":self.left_front_leg,
                    "mid":self.left_mid_leg,
                    "back":self.left_back_leg,
                },
                "right":{
                    "front":self.right_front_leg,
                    "mid":self.right_mid_leg,
                    "back":self.right_back_leg,
            }
        }
        self.update_conf()
        self.move2pos("start_pos")
    
    def update_move2pos(self, pos):
        self.update_conf()
        self.move2pos(pos)

    def move2pos(self, pos):
        for side in self.conf[pos]:
            for _leg in self.conf[pos][side]:
                self.legs[side][_leg].set_servos_angles(self.conf[pos][side][_leg])
                
    def update_conf(self, conf_file="conf.json"):
        self.conf = json.load(open(conf_file))
        


#right_frot_leg.update_servo(0,120,180)

