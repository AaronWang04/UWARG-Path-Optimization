# longitude = Script.GetParam("lat")
# latitude = Script.GetParam("lng")

# print(MAV.getWPCount())

# MAV.setWp

# print(longitude, latitude)
# Script.ChangeParam("lat", latitude+10)
# Script.ChangeParam("lng", longitude+10)

# print('Coordinates changed')  




import sys
import math
import clr
import time
import System
from System import Byte

clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") # includes the Utilities class
from MissionPlanner.Utilities import Locationwp
clr.AddReference("MAVLink") # includes the Utilities class
import MAVLink

idmavcmd = MAVLink.MAV_CMD.WAYPOINT
id = int(idmavcmd)

home = Locationwp().Set(-34.9805,117.8518,0, id)
to = Locationwp()
Locationwp.id.SetValue(to, int(MAVLink.MAV_CMD.TAKEOFF))
Locationwp.p1.SetValue(to, 15)
Locationwp.alt.SetValue(to, 50)

new_waypoint = Locationwp()
Locationwp.id.SetValue(new_waypoint, int(MAVLink.MAV_CMD.WAYPOINT))
Locationwp.alt.SetValue(new_waypoint, 20 )
Locationwp.lng.SetValue(new_waypoint,30)
Locationwp.lat.SetValue(new_waypoint,50)

landing_waypoint= Locationwp()
Locationwp.id.SetValue(landing_waypoint, int(MAVLink.MAV_CMD.LAND))
Locationwp.alt.SetValue(landing_waypoint, 0)
Locationwp.lng.SetValue(landing_waypoint, 10)
Locationwp.lat.SetValue(landing_waypoint, 10)

wp1 = Locationwp().Set(-35,117.8,50, id)
wp2 = Locationwp().Set(-35,117.89,50, id)
wp3 = Locationwp().Set(-35,117.85,20, id)

print(vars(Locationwp))


print ("set wp total")
time.sleep(4)
# Total waypoint
MAV.setWPTotal(6)
# setWP for each waypoint
print ("upload home - reset on arm")
MAV.setWP(home,0,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
print ("upload to")
MAV.setWP(to,1,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
print ("upload wp1")
MAV.setWP(new_waypoint, 2, MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
print("upload new_waypoint")
MAV.setWP(wp1,3,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
print ("upload wp2")
MAV.setWP(wp2,4,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
print ("upload wp3")
MAV.setWP(wp3,5,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
print ("final ack")
MAV.setWP(landing_waypoint,6,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
print ("upload landing waypoint")

# something u have to call 
MAV.setWPACK()

print ("done")



# https://mavlink.io/en/messages/common.html#MAV_CMD_NAV_WAYPOINT
# 1: Hold	Hold time. (ignored by fixed wing, time to stay at waypoint for rotary wing)	min:0	s
# 2: Accept Radius	Acceptance radius (if the sphere with this radius is hit, the waypoint counts as reached)	min:0	m
# 3: Pass Radius	0 to pass through the WP, if > 0 radius to pass by WP. Positive value for clockwise orbit, negative value for counter-clockwise orbit. Allows trajectory control.		m
# 4: Yaw	Desired yaw angle at waypoint (rotary wing). NaN to use the current system yaw heading mode (e.g. yaw towards next waypoint, yaw to home, etc.).		deg
# 5: Latitude	Latitude		
# 6: Longitude	Longitude		
# 7: Altitude
def create_waypoint(command_id, latitude, longitude, altitude, hold=0, accept_radius=0, pass_radius=0, yaw=0):
    waypoint = Locationwp()
    
    Locationwp.id.SetValue(waypoint, int(command_id))
    Locationwp.p1.SetValue(waypoint, hold)
    Locationwp.p2.SetValue(waypoint, accept_radius)
    Locationwp.p3.SetValue(waypoint, pass_radius)
    Locationwp.p3.SetValue(waypoint, yaw)
    Locationwp.lat.SetValue(waypoint, latitude)
    Locationwp.lng.SetValue(waypoint, longitude)
    Locationwp.alt.SetValue(waypoint, altitude)
    
    return waypoint