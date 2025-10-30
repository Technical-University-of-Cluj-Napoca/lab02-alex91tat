import os
import datetime

def smart_log(*args, **kwargs) -> None:
    colors = {
        'INFO': '\033[94m',      # Blue
        'DEBUG': '\033[90m',     # Gray
        'WARNING': '\033[93m',   # Yellow
        'ERROR': '\033[91m',     # Red
        'RESET': '\033[0m'       # Reset color
    }

    level = kwargs.get('level', 'info').upper()
    timestamp = kwargs.get('timestamp', True)
    date = kwargs.get('date', False)
    save_to = kwargs.get('save_to', None)
    color = kwargs.get('colored', True)

    message = ' '.join(str(arg) for arg in args)
    timestamp_message = ''
    if timestamp:
        now = datetime.datetime.now()
        if date:
            timestamp_message = now.strftime("%d-%m-%Y %H:%M:%S")
        else:
            timestamp_message = now.strftime("%H:%M:%S")

        timestamp_message = f"{timestamp_message} "

    level_message = f"{level} "
    log_message = f"{timestamp_message}{level_message}{message}"

    if color:
        color_code = colors.get(level, colors['RESET'])
        console_message = f"{timestamp_message}{color_code}{level_message}{message}{colors['RESET']}"
    else:
        console_message = log_message

    print(console_message)
    
    if save_to:
        directory = os.path.dirname(save_to)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(save_to, 'a') as file:
            file.write(log_message + '\n')

# if __name__ == "__main__":
#     smart_log("System started successfully.", level="info")
#     smart_log("User alice logged in", level="debug")
#     smart_log("Low disk space detected!", level="warning", save_to="logs/system.log")
#     smart_log("Model", "training", "failed!", level="error", color=True, save_to="logs/errors.log")
#     smart_log("Process end", level="info", color=False, save_to="logs/errors.log")