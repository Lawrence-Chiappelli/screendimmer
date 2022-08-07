import subprocess
import sys
import utils

def invoke_shell_command(base_commands, redirection_commands=[], return_output=False):

    """Invoke a command to the linux shell. Optionally return the result.
    @param base_commands (list): a list of commands seperated by word
    @param redirection_commands (list): an optional list of commands for redirection: 'grep', 'awk' etc
    @return output (string): Optionally return parsed output if needed
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

def parse_all_monitors():
    xrandr_command = ['xrandr', '--listactivemonitors']
    command_output = invoke_shell_command(xrandr_command, return_output=True)
    relevant_lines = command_output[1:-1]
    monitors = [line.split(" ").pop(-1) for line in relevant_lines]
    return monitors

def parse_all_resolutions():
    # TODO: parse the resolutions
    return ['1920x1080']

def parse_all_brightnesses():
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
    """Set brightness of monitor using xrandr.

    @param monitor_name (str): String representation of xrandr monitor name
    @param brightness_value (str): Valid range is "0.1"-"1.0" or "1"-"100"
    @return (None): None
    """

    if not type(brightness_value) is str:
        raise TypeError("Brightness values need to be strings. (Note: values retrieved from TK spinners/scales are strings)")

    if not type(brightness_value) is str:
        raise TypeError("Monitor names need to be strings.")

    if brightness_value.isnumeric():
        # Corner case: if the passed brightness_value string is a base 10 int,
        # we need to convert it to an xrandr-usable string input (not base 10).
        # We have no way of intercepting the Tk value beforehand so I'm forced
        # to convert it here.
        brightness_value = utils.convert_converted_brightness_to_xrandr(brightness_value)

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
