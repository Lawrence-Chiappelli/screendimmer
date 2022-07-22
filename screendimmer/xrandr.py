import subprocess
import sys

def invoke_shell_command(base_commands, redirection_commands=[], return_output=False):

    """Invoke a command to the linux shell. Optionally return the result.
    @param base_commands (list): a list of commands seperated by word
    @param redirection_commands (list): a list of commands for redirection: 'grep', 'awk' etc
    @return output (string): The (parsed) output
    """
    result = subprocess.Popen(
        base_commands,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if redirection_commands:
        result = subprocess.check_output(
            redirection_commands,
            stdin=result.stdout
        )

    if return_output:
        # Differing output structures if fed "piped" commands
        if redirection_commands:
            # <class 'bytes'>
            output = str(result).split('\\n')
        else:
            # <class 'subprocess.Popen'>
            output = str(result.communicate())[1:-1].split('\\n')

        return output
    else:
        return None

def get_all_monitors():
    xrandr_command = ['xrandr', '--listactivemonitors']
    command_output = invoke_shell_command(xrandr_command, return_output=True)
    relevant_lines = command_output[1:-1]
    monitors = [line.split(" ").pop(-1) for line in relevant_lines]
    return monitors

def get_all_resolutions():
    return ['1920x1080']

def get_all_brightnesses():
    xrandr_command = ['xrandr', '--verbose']
    pipe_commands = ['grep', 'Brightness']
    command_output = invoke_shell_command(
        xrandr_command,
        redirection_commands=pipe_commands,
        return_output=True,
    )
    del command_output[-1]
    brightnesses = [line.split(" ").pop(-1) for line in command_output]

    return brightnesses

def set_brightness(monitor_name: str, brightness_value: str):
    xrandr_command = [
        'xrandr',
        '--output',
        monitor_name,
        '--brightness',
        brightness_value
    ]
    invoke_shell_command(xrandr_command)

if __name__ == '__main__':
    print("This should not be the main module.")
