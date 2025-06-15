import datetime

def send_time_to_arduino(ser):
    """Send current time to Arduino using the provided serial connection"""
    try:
        current_time = datetime.datetime.now()
        time_string = current_time.strftime("%H:%M")
        message = f"TIME:{time_string}\n"
        
        ser.write(message.encode())
        print(f"Sent time to Arduino: {time_string}")
        return True
        
    except Exception as e:
        print(f"Error sending time to Arduino: {e}")
        return False

def on_time_change(ser):
    """Function to call whenever the time changes (every minute)
    
    Args:
        ser: The serial connection object from main.py
    """
    return send_time_to_arduino(ser)