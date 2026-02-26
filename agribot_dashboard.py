import serial
import tkinter as tk
from tkinter import *
from time import strftime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# ================= SERIAL SETUP =================
# Change COM4 if needed
ser = serial.Serial("COM4", 9600)

# ================= WINDOW SETUP =================
root = Tk()
root.title("AgriBot Smart Dashboard")
root.geometry("700x750")
root.configure(bg="#1e1e2f")

# ================= CLOCK =================
def update_time():
    string = strftime('%H:%M:%S')
    clock_label.config(text=string)
    clock_label.after(1000, update_time)

clock_label = Label(root, font=("Arial", 16, "bold"),
                    bg="#1e1e2f", fg="cyan")
clock_label.pack(pady=10)
update_time()

# ================= SENSOR LABELS =================
temp_label = Label(root, text="Temperature: --",
                   font=("Arial", 16, "bold"),
                   fg="white", bg="#1e1e2f")
temp_label.pack(pady=5)

humidity_label = Label(root, text="Humidity: --",
                       font=("Arial", 16, "bold"),
                       fg="white", bg="#1e1e2f")
humidity_label.pack(pady=5)

soil_label = Label(root, text="Soil Moisture: --",
                   font=("Arial", 16, "bold"),
                   fg="white", bg="#1e1e2f")
soil_label.pack(pady=5)

sprinkler_label = Label(root, text="Sprinkler: OFF",
                        font=("Arial", 16, "bold"),
                        fg="red", bg="#1e1e2f")
sprinkler_label.pack(pady=10)

# ================= BUTTON FUNCTIONS =================
def send_command(command):
    ser.write(command.encode())

def forward():
    send_command('F')

def backward():
    send_command('B')

def left():
    send_command('L')

def right():
    send_command('R')

def stop():
    send_command('S')

def sprinkler_on():
    send_command('O')
    sprinkler_label.config(text="Sprinkler: ON", fg="green")

def sprinkler_off():
    send_command('P')
    sprinkler_label.config(text="Sprinkler: OFF", fg="red")

# ================= BUTTONS =================
button_frame = Frame(root, bg="#1e1e2f")
button_frame.pack(pady=20)

Button(button_frame, text="Forward", width=15, height=2,
       bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
       command=forward).grid(row=0, column=1, pady=5)

Button(button_frame, text="Left", width=15, height=2,
       bg="#2196F3", fg="white", font=("Arial", 12, "bold"),
       command=left).grid(row=1, column=0, padx=5, pady=5)

Button(button_frame, text="Stop", width=15, height=2,
       bg="#f44336", fg="white", font=("Arial", 12, "bold"),
       command=stop).grid(row=1, column=1, pady=5)

Button(button_frame, text="Right", width=15, height=2,
       bg="#2196F3", fg="white", font=("Arial", 12, "bold"),
       command=right).grid(row=1, column=2, padx=5, pady=5)

Button(button_frame, text="Backward", width=15, height=2,
       bg="#FF9800", fg="white", font=("Arial", 12, "bold"),
       command=backward).grid(row=2, column=1, pady=5)

Button(root, text="Sprinkler ON", width=20, height=2,
       bg="green", fg="white", font=("Arial", 12, "bold"),
       command=sprinkler_on).pack(pady=5)

Button(root, text="Sprinkler OFF", width=20, height=2,
       bg="red", fg="white", font=("Arial", 12, "bold"),
       command=sprinkler_off).pack(pady=5)

# ================= GRAPH =================
plt.style.use("dark_background")
fig, ax = plt.subplots(figsize=(6,3))
ax.set_title("Live Sensor Data")
ax.set_xlabel("Time")
ax.set_ylabel("Value")

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=20)

x_data = []
temp_data = []
humidity_data = []
soil_data = []

def update_graph():
    # Simulated data (replace with serial data later)
    temp = random.randint(20, 35)
    humidity = random.randint(40, 80)
    soil = random.randint(300, 800)

    temp_label.config(text=f"Temperature: {temp} °C")
    humidity_label.config(text=f"Humidity: {humidity} %")
    soil_label.config(text=f"Soil Moisture: {soil}")

    x_data.append(len(x_data))
    temp_data.append(temp)
    humidity_data.append(humidity)
    soil_data.append(soil)

    ax.clear()
    ax.plot(x_data, temp_data, label="Temperature")
    ax.plot(x_data, humidity_data, label="Humidity")
    ax.plot(x_data, soil_data, label="Soil Moisture")
    ax.legend()
    ax.set_title("Live Sensor Data")
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")

    canvas.draw()

    root.after(2000, update_graph)

update_graph()

# ================= RUN APP =================
root.mainloop()