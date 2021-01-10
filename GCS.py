#!/usr/bin/env python3
import numpy as np
import asyncio
import sys
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw, VelocityNedYaw, VelocityBodyYawspeed)

##This IP address should be the TX2 IP address which already run the ./mavsdk_server -p 50051 serial:///ttyTHS2:921600

mavsdk_address = 'localhost'
p = '50051'

def updateGUI(label, value):
    label['text'] = value

'''def Bernoulli(t1,t2):
    List = []
    for i in np.linspace(0,2*np.pi,24):
        #theta = -3*(np.arctan(np.sin(i)))+np.pi/2
        v_theta = 3*np.cos(i)/((np.sin(i)*np.sin(i))+1)
        List.append(v_theta)
    return List'''

def Bernoulli():
    List = []
    for i in np.linspace(0,2*np.pi,24):
        #theta = -3*(np.arctan(np.sin(i)))+np.pi/2
        v_theta = 3*np.cos(i)/((np.sin(i)*np.sin(i))+1)
        List.append(v_theta)
    return List
async def ARM_TAKEOFF():

    drone = System(mavsdk_server_address=mavsdk_address, port=p)
    await drone.connect(system_address="udp://localhost:14581")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    # Start parallel tasks
    #print_altitude_task = asyncio.ensure_future(print_altitude(drone))
    #print_flight_mode_task = asyncio.ensure_future(print_flight_mode(drone))

    #running_tasks = [print_altitude_task, print_flight_mode_task]
    #termination_task = asyncio.ensure_future(observe_is_in_air(drone, running_tasks))

    # Execute the maneuvers
    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(5)

    #print("-- Landing")
    #await drone.action.land()

    # Wait until the drone is landed (instead of exiting after 'land' is sent)
    #await termination_task

async def print_altitude(drone):
    """ Prints the altitude when it changes """

    previous_altitude = None

    async for position in drone.telemetry.position():
        altitude = round(position.relative_altitude_m)
        if altitude != previous_altitude:
            previous_altitude = altitude
            print(f"Altitude: {altitude}")


async def print_flight_mode(drone):
    """ Prints the flight mode when it changes """

    previous_flight_mode = None

    async for flight_mode in drone.telemetry.flight_mode():
        if flight_mode is not previous_flight_mode:
            previous_flight_mode = flight_mode
            print(f"Flight mode: {flight_mode}")


async def observe_is_in_air(drone, running_tasks):
    """ Monitors whether the drone is flying or not and
    returns after landing """

    was_in_air = False

    async for is_in_air in drone.telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            for task in running_tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            await asyncio.get_event_loop().shutdown_asyncgens()
            return

async def REBOOT():

    drone = System(mavsdk_server_address='192.168.1.47',port='50051')
    await drone.connect(system_address="udp://localhost:14581")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    
    print("-- Rebooting")
    await drone.action.reboot()


async def ARM():

    drone = System(mavsdk_server_address=mavsdk_address, port=p)
    await drone.connect()

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print("Global position estimate ok")
            break
    #asyncio.ensure_future(print_is_armed(drone))
    #asyncio.ensure_future(print_is_in_air(drone))
    print("-- Arming")
    await drone.action.arm()


async def DISARM():

    drone = System(mavsdk_server_address=mavsdk_address, port=p)
    await drone.connect()

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print("Global position estimate ok")
            break
    #asyncio.ensure_future(print_is_armed(drone))
    #asyncio.ensure_future(print_is_in_air(drone))
    print("-- Disarming")
    await drone.action.disarm()

     
async def print_is_armed(drone):
    async for is_armed in drone.telemetry.armed():
        print("Is_armed:", is_armed)


async def print_is_in_air(drone):
    async for is_in_air in drone.telemetry.in_air():
        print("Is_in_air:", is_in_air)

async def LAND():

    drone = System(mavsdk_server_address=mavsdk_address, port=p)
    await drone.connect()

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break
    print("-- Landing")
    await drone.action.land()


async def SQUARE():

    """ Does Offboard control using position NED coordinates. """

    drone = System(mavsdk_server_address=mavsdk_address, port=p)
    await drone.connect()

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print("-- Go 0m North, 0m East, -5m Down within local coordinate system")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -3.0, 0.0))
    await asyncio.sleep(10)

    print("-- Go 5m North, 0m East, -5m Down within local coordinate system, turn to face East")
    await drone.offboard.set_position_ned(PositionNedYaw(2.0, 0.0, -3.0, 90.0))
    await asyncio.sleep(10)

    print("-- Go 5m North, 10m East, -5m Down within local coordinate system")
    await drone.offboard.set_position_ned(PositionNedYaw(2.0, 2.0, -3.0, 90.0))
    await asyncio.sleep(15)

    print("-- Go 0m North, 10m East, 0m Down within local coordinate system, turn to face South")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 2.0, -3.0, 180.0))
    await asyncio.sleep(10)

    print("-- Go 0m North, 10m East, 0m Down within local coordinate system, turn to face South")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 270.0))
    await asyncio.sleep(10)

    print("-- Landing")
    await drone.action.land()
    print("-- Stopping offboard")
    await asyncio.sleep(5)


async def CIRCLE():
    """ Does Offboard control using velocity body coordinates. """

    drone = System(mavsdk_server_address=mavsdk_address, port=p)
    await drone.connect()

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: \
              {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print("-- Turn clock-wise and climb")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, -1.0, 60.0))
    await asyncio.sleep(5)

    print("-- Turn back anti-clockwise")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, -60.0))
    await asyncio.sleep(5)

    print("-- Wait for a bit")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(2)

    print("-- Fly a circle")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(1.0, 0.0, 0.0, 30.0))
    await asyncio.sleep(15)

    print("-- Wait for a bit")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(5)

    print("-- Fly a circle sideways")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, -1.0, 0.0, 30.0))
    await asyncio.sleep(15)

    print("-- Wait for a bit")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(8)

    print("-- Landing")
    await drone.action.land()
    await asyncio.sleep(5)

async def HELIX():
    """ Does Offboard control using velocity body coordinates. """

    drone = System(mavsdk_server_address=mavsdk_address, port=p)
    await drone.connect()

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: \
              {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print("-- Turn clock-wise and climb")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, -1.0, 60.0))
    await asyncio.sleep(5)

    print("-- Wait for a bit")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(2)

    print("-- Fly a up helix")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(1.5, 0.0, -0.3, 30.0))
    await asyncio.sleep(15)


    print("-- Wait for a bit")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(5)

    print("-- Fly a down helix")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(1.5, 0.0, 0.3, 30.0))
    await asyncio.sleep(12)

    print("-- Landing")
    await drone.action.land()
    await asyncio.sleep(5)


async def LEMNISCATE():
    """ Does Offboard control using velocity body coordinates. """
    
    drone = System(mavsdk_server_address=mavsdk_address, port=p)
    await drone.connect()

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: \
              {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return


    print("-- climb")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, -1.0, 0))
    await asyncio.sleep(5)
    print("-- initial the lemniscate of Bernoulli formula")
    j = 0
    lob = Bernoulli()
    print("-- Execute the lemniscate of Bernoulli formula")
    for i in lob:
        # this can get the current yaw angle compare with before
        if j == 0:
            mid = lob[0]
            print(lob)
        else:
            mid = lob[j]-lob[j-1]

        #await drone.offboard.set_velocity_body(VelocityBodyYawspeed(1.0, 0.0, 0.0,  (mid*180/np.pi)))   
        await drone.offboard.set_velocity_body(VelocityBodyYawspeed(1.0, 0.0, 0.0,  (mid*180/np.pi)))  
        await asyncio.sleep(1)
        j += 1
        if j == 12:
            print("-- 50% Mission has completed!")
        elif j == 23:
            print("-- 100% Mission has completed!")


    print("-- Landing")
    await drone.action.land()
    await asyncio.sleep(5)



def process(function):
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(function)
    loop.close()

if __name__ == "__main__":
    
    Function = {
        'ARM':ARM(),
        'ARM_TAKEOFF':ARM_TAKEOFF(),
        'DISARM':DISARM(),
        'LAND':LAND(),
        'SQUARE':SQUARE(),
        'CIRCLE':CIRCLE(),
        'HELIX':HELIX(),
        'LEMNISCATE':LEMNISCATE()
    }
    command = sys.argv[1]

   
    if command in Function.keys():
        process(Function[command])



