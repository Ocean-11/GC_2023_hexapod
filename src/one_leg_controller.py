
#Libraries
import json
import sympy as sp

x,y,z,roll,pitch,yaw = sp.symbols('x y z roll pitch yaw')
hip_angle,knee_angle,ankle_angle = sp.symbols('hip_angle knee_angle ankle_angle')

#define hexapod geometry and leg lengths
body_height = 10
leg_length = 15

#define equations for inverse kinematics
hip_equation=sp.atan2(y,x)
knee_equation=sp.pi/2 - (roll+pitch)
ankle_equation = -yaw

#calculate joint angles symbolically
hip_angle_solution = sp.solve(hip_equation - hip_angle, hip_angle)
knee_angle_solution = sp.solve(knee_equation - knee_angle, knee_angle)
ankle_angle_solution = sp.solve(ankle_equation - ankle_angle, ankle_angle)

#specify the desired end effector pose
desired_x_value = 20.0
desired_y_value = 10.0
desired_z_value = -5.0
desired_roll_value = 0.0
desired_pitch_value = 0.0
desired_yaw_value = sp.rad(45.0)

#substitute values into the solutions
hip_angle_value = hip_angle_solution[0].evalf(subs={x:desired_x_value, y: desired_y_value})
knee_angle_value = knee_angle_solution[0].evalf(subs={roll:desired_roll_value, pitch: desired_pitch_value})
ankle_angle_value = ankle_angle_solution[0].evalf(subs={yaw:desired_yaw_value})

#print the joint angles for the desired pose
print(f"Hip Angle:{hip_angle_value} radians")
print(f"Knee Angle:{knee_angle_value} radians")
print(f"Ankle Angle:{ankle_angle_value} radians")





