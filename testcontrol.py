import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import serial
import serial.tools.list_ports
import threading
import json
import os
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import keyboard
import subprocess
import time
import re
import datetime
import clock  # Import our clock module

class ArduinoControlPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Arduino Control Panel")
        self.root.geometry("800x600")
        
        self.serial_connection = None
        self.is_connected = False
        self.config_file = "arduino_config.json"
        
        # Time tracking for sending time updates
        self.last_minute = -1
        
        # Load configuration
        self.button_mappings = self.load_config()
        
        # Initialize audio system
        self.init_audio_system()
        
        # Create GUI
        self.create_gui()
        
        # Start serial monitoring thread
        self.monitoring = False
        
    def init_audio_system(self):
        """Initialize Windows audio system for volume control"""
        try:
            # Get default audio device
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume_control = cast(interface, POINTER(IAudioEndpointVolume))
            
            # Get all audio sessions for per-app volume control
            self.audio_sessions = {}
            self.refresh_audio_sessions()
        except Exception as e:
            print(f"Audio system initialization error: {e}")
            self.volume_control = None
    
    def refresh_audio_sessions(self):
        """Refresh list of audio sessions for per-app volume control"""
        try:
            sessions = AudioUtilities.GetAllSessions()
            self.audio_sessions = {}
            for session in sessions:
                if session.Process and session.Process.name():
                    self.audio_sessions[session.Process.name()] = session
        except Exception as e:
            print(f"Error refreshing audio sessions: {e}")
    
    def check_and_send_time(self):
        """Check if the minute has changed and send time to Arduino if connected"""
        if self.is_connected and self.serial_connection:
            current_time = datetime.datetime.now()
            current_minute = current_time.minute
            
            if current_minute != self.last_minute:
                try:
                    clock.on_time_change(self.serial_connection)
                    self.last_minute = current_minute
                    self.log_to_monitor(f"Time sent to Arduino: {current_time.strftime('%H:%M')}")
                except Exception as e:
                    self.log_to_monitor(f"Error sending time to Arduino: {str(e)}")
    
    def create_gui(self):
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Connection tab
        self.create_connection_tab(notebook)
        
        # Button mapping tab
        self.create_mapping_tab(notebook)
        
        # Monitor tab
        self.create_monitor_tab(notebook)
    
    def create_connection_tab(self, parent):
        connection_frame = ttk.Frame(parent)
        parent.add(connection_frame, text="Connection")
        
        # Serial port selection
        ttk.Label(connection_frame, text="Serial Port:").pack(pady=5)
        
        port_frame = ttk.Frame(connection_frame)
        port_frame.pack(pady=5)
        
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(port_frame, textvariable=self.port_var, width=20)
        self.port_combo.pack(side='left', padx=5)
        
        ttk.Button(port_frame, text="Refresh", command=self.refresh_ports).pack(side='left', padx=5)
        
        # Baud rate
        ttk.Label(connection_frame, text="Baud Rate:").pack(pady=5)
        self.baud_var = tk.StringVar(value="115200")  # Changed default to match Arduino code
        ttk.Entry(connection_frame, textvariable=self.baud_var, width=10).pack(pady=5)
        
        # Connect/Disconnect button
        self.connect_btn = ttk.Button(connection_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.pack(pady=10)
        
        # Status
        self.status_var = tk.StringVar(value="Disconnected")
        ttk.Label(connection_frame, textvariable=self.status_var, foreground="red").pack(pady=5)
        
        # Time sync status
        self.time_status_var = tk.StringVar(value="Time sync: Inactive")
        ttk.Label(connection_frame, textvariable=self.time_status_var, foreground="gray").pack(pady=5)
        
        # Refresh ports on startup
        self.refresh_ports()
    
    def create_mapping_tab(self, parent):
        mapping_frame = ttk.Frame(parent)
        parent.add(mapping_frame, text="Button Mapping")
        
        # Create scrollable frame
        canvas = tk.Canvas(mapping_frame)
        scrollbar = ttk.Scrollbar(mapping_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Button mappings
        self.mapping_widgets = {}
        
        for i in range(16):
            button_num = str(i + 1)
            frame = ttk.LabelFrame(scrollable_frame, text=f"Button {button_num}")
            frame.pack(fill='x', padx=5, pady=5)
            
            # Action type selection
            action_frame = ttk.Frame(frame)
            action_frame.pack(fill='x', padx=5, pady=5)
            
            ttk.Label(action_frame, text="Action:").pack(side='left')
            action_var = tk.StringVar(value=self.button_mappings.get(button_num, {}).get('action', 'none'))
            action_combo = ttk.Combobox(action_frame, textvariable=action_var, 
                                      values=['none', 'master_volume', 'app_volume', 'keyboard_shortcut', 'run_command'],
                                      state='readonly', width=15)
            action_combo.pack(side='left', padx=5)
            
            # Parameter entry
            param_frame = ttk.Frame(frame)
            param_frame.pack(fill='x', padx=5, pady=5)
            
            ttk.Label(param_frame, text="Parameter:").pack(side='left')
            param_var = tk.StringVar(value=self.button_mappings.get(button_num, {}).get('parameter', ''))
            param_entry = ttk.Entry(param_frame, textvariable=param_var, width=30)
            param_entry.pack(side='left', padx=5, fill='x', expand=True)
            
            # Help text
            help_text = ttk.Label(frame, text="", foreground="gray", font=("Arial", 8))
            help_text.pack(fill='x', padx=5)
            
            self.mapping_widgets[button_num] = {
                'action': action_var,
                'parameter': param_var,
                'help': help_text
            }
            
            # Update help text when action changes
            action_var.trace('w', lambda *args, btn=button_num: self.update_help_text(btn))
            self.update_help_text(button_num)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Save button
        ttk.Button(mapping_frame, text="Save Configuration", command=self.save_config).pack(pady=10)
    
    def create_monitor_tab(self, parent):
        monitor_frame = ttk.Frame(parent)
        parent.add(monitor_frame, text="Monitor")
        
        ttk.Label(monitor_frame, text="Arduino Data:").pack(pady=5)
        
        self.monitor_text = scrolledtext.ScrolledText(monitor_frame, height=20, width=70)
        self.monitor_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Clear button
        ttk.Button(monitor_frame, text="Clear", command=self.clear_monitor).pack(pady=5)
    
    def update_help_text(self, button_num):
        action = self.mapping_widgets[button_num]['action'].get()
        help_widget = self.mapping_widgets[button_num]['help']
        
        help_texts = {
            'none': 'No action assigned',
            'master_volume': 'Parameter: volume level (0-100) or +5/-5 for relative',
            'app_volume': 'Parameter: application_name.exe:volume_level (e.g., chrome.exe:50)',
            'keyboard_shortcut': 'Parameter: key combination (e.g., ctrl+c, alt+tab, win+d)',
            'run_command': 'Parameter: command to execute (e.g., notepad.exe, calc)'
        }
        
        help_widget.config(text=help_texts.get(action, ''))
    
    def refresh_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo['values'] = ports
        if ports:
            self.port_combo.set(ports[0])
    
    def toggle_connection(self):
        if not self.is_connected:
            self.connect_arduino()
        else:
            self.disconnect_arduino()
    
    def connect_arduino(self):
        try:
            port = self.port_var.get()
            baud = int(self.baud_var.get())
            
            self.serial_connection = serial.Serial(port, baud, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            
            self.is_connected = True
            self.status_var.set("Connected")
            self.time_status_var.set("Time sync: Active")
            self.connect_btn.config(text="Disconnect")
            
            # Send initial time immediately after connection
            try:
                clock.on_time_change(self.serial_connection)
                self.last_minute = datetime.datetime.now().minute
                self.log_to_monitor("Initial time sent to Arduino")
            except Exception as e:
                self.log_to_monitor(f"Error sending initial time: {str(e)}")
            
            # Start monitoring thread
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self.monitor_serial, daemon=True)
            self.monitor_thread.start()
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
    
    def disconnect_arduino(self):
        self.monitoring = False
        if self.serial_connection:
            self.serial_connection.close()
            self.serial_connection = None
        
        self.is_connected = False
        self.status_var.set("Disconnected")
        self.time_status_var.set("Time sync: Inactive")
        self.connect_btn.config(text="Connect")
    
    def monitor_serial(self):
        while self.monitoring and self.serial_connection:
            try:
                # Check and send time updates
                self.check_and_send_time()
                
                if self.serial_connection.in_waiting:
                    line = self.serial_connection.readline().decode('utf-8').strip()
                    if line:
                        self.process_arduino_data(line)
                        self.log_to_monitor(line)
                time.sleep(0.1)  # Check every 100ms for time updates
            except Exception as e:
                self.log_to_monitor(f"Error: {str(e)}")
                break
    
    def process_arduino_data(self, data):
        # Parse button press data - looking for the last number in the line
        try:
            # Split the data by comma and get the last value (button press)
            values = data.split(',')
            if len(values) >= 22:  # Expected format with 22 values
                button_value = values[-1].strip()  # Last value is button press
                if button_value and button_value != '0':
                    self.handle_button_press(button_value)
        except Exception as e:
            # Fallback: look for "Button Pressed:" format
            if "Button Pressed:" in data:
                button_num = data.split("Button Pressed: ")[-1].strip()
                self.handle_button_press(button_num)
    
    def handle_button_press(self, button_num):
        if button_num in self.button_mappings:
            mapping = self.button_mappings[button_num]
            action = mapping.get('action', 'none')
            parameter = mapping.get('parameter', '')
            
            try:
                if action == 'master_volume':
                    self.handle_master_volume(parameter)
                elif action == 'app_volume':
                    self.handle_app_volume(parameter)
                elif action == 'keyboard_shortcut':
                    self.handle_keyboard_shortcut(parameter)
                elif action == 'run_command':
                    self.handle_run_command(parameter)
                    
                self.log_to_monitor(f"Executed: Button {button_num} -> {action}({parameter})")
            except Exception as e:
                self.log_to_monitor(f"Error executing button {button_num}: {str(e)}")
    
    def handle_master_volume(self, parameter):
        if not self.volume_control:
            return
            
        if parameter.startswith('+') or parameter.startswith('-'):
            # Relative volume change
            current_volume = self.volume_control.GetMasterScalarVolume()
            change = float(parameter) / 100.0
            new_volume = max(0.0, min(1.0, current_volume + change))
        else:
            # Absolute volume
            new_volume = float(parameter) / 100.0
            
        self.volume_control.SetMasterScalarVolume(new_volume, None)
    
    def handle_app_volume(self, parameter):
        if ':' not in parameter:
            return
            
        app_name, volume_str = parameter.split(':', 1)
        volume = float(volume_str) / 100.0
        
        self.refresh_audio_sessions()
        if app_name in self.audio_sessions:
            session = self.audio_sessions[app_name]
            if session.SimpleAudioVolume:
                session.SimpleAudioVolume.SetMasterVolume(volume, None)
    
    def handle_keyboard_shortcut(self, parameter):
        keyboard.send(parameter)
    
    def handle_run_command(self, parameter):
        subprocess.Popen(parameter, shell=True)
    
    def log_to_monitor(self, message):
        if hasattr(self, 'monitor_text'):
            self.monitor_text.insert(tk.END, f"{time.strftime('%H:%M:%S')}: {message}\n")
            self.monitor_text.see(tk.END)
    
    def clear_monitor(self):
        self.monitor_text.delete(1.0, tk.END)
    
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def save_config(self):
        config = {}
        for button_num, widgets in self.mapping_widgets.items():
            config[button_num] = {
                'action': widgets['action'].get(),
                'parameter': widgets['parameter'].get()
            }
        
        self.button_mappings = config
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")

def main():
    root = tk.Tk()
    app = ArduinoControlPanel(root)
    
    def on_closing():
        app.disconnect_arduino()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()