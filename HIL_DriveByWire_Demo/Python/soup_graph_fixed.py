from pymodbus.client import ModbusTcpClient
import pygame
import time
import matplotlib.pyplot as plt

# --- 1. CONFIGURATION ---
PLC_IP = '192.168.0.165'
GAS_AXIS_INDEX = 2         # Your auto-detected axis
BTN_ECO_INDEX = 4          # Square
BTN_SPORT_INDEX = 5        # X
BTN_STOP_INDEX = 0         # <--- NEW: Button 0 (usually X or Circle) to Quit

# --- 2. SETUP ---
print("🔌 Connecting...")
try:
    client = ModbusTcpClient(PLC_IP, port=502)
    client.connect()
except:
    print("❌ PLC Failed.")

pygame.init()
pygame.joystick.init()
if pygame.joystick.get_count() == 0: exit()
wheel = pygame.joystick.Joystick(0)
wheel.init()

# Auto-Fix Axis Logic
if GAS_AXIS_INDEX >= wheel.get_numaxes():
    GAS_AXIS_INDEX = wheel.get_numaxes() - 1

# --- 3. GRAPH SETUP ---
plt.ion()
fig, ax = plt.subplots()
plt.title("Real-Time Drive-by-Wire Response")
plt.xlabel("Time")
plt.ylabel("Power (%)")
plt.ylim(-5, 105)
plt.grid(True) # Added grid for better readability

line_pedal, = ax.plot([], [], 'b-', label='Pedal Input (Foot)')
line_engine, = ax.plot([], [], 'r--', linewidth=2, label='Engine Output (PLC)')
plt.legend(loc='upper left')

window_width = 100
data_pedal = [0] * window_width
data_engine = [0] * window_width

print("✅ Running! Press BUTTON 0 to Stop.")

# --- 4. MAIN LOOP ---
try:
    running = True
    while running:
        pygame.event.pump()

        # A. READ PEDAL (FIXED INVERSION)
        raw_val = wheel.get_axis(GAS_AXIS_INDEX)
        
        # --- THE FIX IS HERE ---
        # Old Formula: ((raw_val + 1) / 2) * 100
        # New Formula: We multiply raw_val by -1 to flip it
        pedal_percent = int(((raw_val * -1) + 1) / 2 * 100)
        
        # Clamp 0-100
        if pedal_percent < 0: pedal_percent = 0
        if pedal_percent > 100: pedal_percent = 100

        # B. CHECK BUTTONS (Stop & Mode)
        num_buttons = wheel.get_numbuttons()
        mode_cmd = 0
        
        # STOP BUTTON CHECK
        if BTN_STOP_INDEX < num_buttons:
            if wheel.get_button(BTN_STOP_INDEX):
                print("🛑 Stop Button Pressed.")
                running = False 

        # MODE CHECK
        if BTN_ECO_INDEX < num_buttons and wheel.get_button(BTN_ECO_INDEX):
            mode_cmd = 1 # Eco
        if BTN_SPORT_INDEX < num_buttons and wheel.get_button(BTN_SPORT_INDEX):
            mode_cmd = 2 # Sport

        # C. PLC COMMUNICATION
        client.write_register(0, pedal_percent)
        client.write_register(1, mode_cmd)
        
        res = client.read_input_registers(0, count=1)
        engine_out = 0
        if not res.isError():
            engine_out = res.registers[0]

        # D. UPDATE GRAPH
        data_pedal.append(pedal_percent)
        data_engine.append(engine_out)
        data_pedal.pop(0)
        data_engine.pop(0)

        line_pedal.set_ydata(data_pedal)
        line_pedal.set_xdata(range(len(data_pedal)))
        line_engine.set_ydata(data_engine)
        line_engine.set_xdata(range(len(data_engine)))
        
        ax.set_xlim(0, len(data_pedal))
        plt.pause(0.01)

except KeyboardInterrupt:
    pass

print("🏁 Finished.")
client.close()
plt.close()