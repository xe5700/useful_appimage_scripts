#!/usr/bin/env python3
from os import path
import subprocess

class Kdotool:
    """
    A Python wrapper for kdotool, a window control utility for KDE 5 and 6.
    This class provides methods to interact with windows, desktops, and other KDE features.
    """

    def __init__(self, debug=False, dry_run=False, bin="kdotool"):
        """
        Initialize the Kdotool wrapper.

        :param debug: Enable debug output for kdotool.
        :param dry_run: Don't actually run the script, just print it to stdout.
        """
        self.debug = debug
        self.dry_run = dry_run
        self.bin = bin
    def _run_command(self, command):
        """
        Internal method to run a kdotool command.

        :param command: The kdotool command as a list of strings.
        :return: The output of the command as a string.
        """
        if self.debug:
            command.insert(0, "--debug")
        if self.dry_run:
            command.insert(0, "--dry-run")
        result = subprocess.run([self.bin] + command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"kdotool command failed: {result.stderr}")
        return result.stdout.strip()

    # Window Query Commands
    def search(self, pattern, options=None):
        """
        Search for windows matching a pattern.

        :param pattern: The regular expression pattern to match.
        :param options: A dictionary of options (e.g., {"--class": True, "--name": True}).
        :return: The output of the search command.
        """
        command = ["search"]
        if options:
            for opt, value in options.items():
                if value:
                    command.append(opt)
        command.append(pattern)
        return self._run_command(command)

    def get_active_window(self):
        """
        Get the currently active window.

        :return: The output of the getactivewindow command.
        """
        return self._run_command(["getactivewindow"])

    def get_mouse_location(self, shell=False):
        """
        Get the current mouse location.

        :param shell: If True, output shell data you can eval.
        :return: The output of the getmouselocation command.
        """
        command = ["getmouselocation"]
        if shell:
            command.append("--shell")
        return self._run_command(command)

    # Window Action Commands
    def get_window_name(self, window="%1"):
        """
        Get the name of a window.

        :param window: The window identifier (default is %1).
        :return: The output of the getwindowname command.
        """
        return self._run_command(["getwindowname", window])

    def get_window_class_name(self, window="%1"):
        """
        Get the class name of a window.

        :param window: The window identifier (default is %1).
        :return: The output of the getwindowclassname command.
        """
        return self._run_command(["getwindowclassname", window])

    def get_window_geometry(self, window="%1"):
        """
        Get the geometry of a window.

        :param window: The window identifier (default is %1).
        :return: The output of the getwindowgeometry command.
        """
        return self._run_command(["getwindowgeometry", window])

    def get_window_id(self, window="%1"):
        """
        Get the ID of a window.

        :param window: The window identifier (default is %1).
        :return: The output of the getwindowid command.
        """
        return self._run_command(["getwindowid", window])

    def get_window_pid(self, window="%1"):
        """
        Get the PID of the process owning a window.

        :param window: The window identifier (default is %1).
        :return: The output of the getwindowpid command.
        """
        return self._run_command(["getwindowpid", window])

    def window_activate(self, window="%1"):
        """
        Activate a window.

        :param window: The window identifier (default is %1).
        :return: The output of the windowactivate command.
        """
        return self._run_command(["windowactivate", window])

    def window_raise(self, window="%1"):
        """
        Raise a window to the top of the window stack (KDE 6 only).

        :param window: The window identifier (default is %1).
        :return: The output of the windowraise command.
        """
        return self._run_command(["windowraise", window])

    def window_minimize(self, window="%1"):
        """
        Minimize a window.

        :param window: The window identifier (default is %1).
        :return: The output of the windowminimize command.
        """
        return self._run_command(["windowminimize", window])

    def window_close(self, window="%1"):
        """
        Close a window.

        :param window: The window identifier (default is %1).
        :return: The output of the windowclose command.
        """
        return self._run_command(["windowclose", window])

    def window_size(self, window="%1", width="x", height="x"):
        """
        Resize a window.

        :param window: The window identifier (default is %1).
        :param width: The new width (use 'x' to keep current width).
        :param height: The new height (use 'y' to keep current height).
        :return: The output of the windowsize command.
        """
        return self._run_command(["windowsize", window, str(width), str(height)])

    def window_move(self, window="%1", x="x", y="y", relative=False):
        """
        Move a window.

        :param window: The window identifier (default is %1).
        :param x: The new x coordinate (use 'x' to keep current position).
        :param y: The new y coordinate (use 'y' to keep current position).
        :param relative: If True, move relative to the current position.
        :return: The output of the windowmove command.
        """
        command = ["windowmove"]
        if relative:
            command.append("--relative")
        command.extend([window, str(x), str(y)])
        return self._run_command(command)

    def window_state(self, window="%1", add=None, remove=None, toggle=None):
        """
        Change a property on a window.

        :param window: The window identifier (default is %1).
        :param add: A property to add (e.g., "ABOVE").
        :param remove: A property to remove (e.g., "FULLSCREEN").
        :param toggle: A property to toggle (e.g., "SHADED").
        :return: The output of the windowstate command.
        """
        command = ["windowstate"]
        if add:
            command.extend(["--add", add])
        if remove:
            command.extend(["--remove", remove])
        if toggle:
            command.extend(["--toggle", toggle])
        command.append(window)
        return self._run_command(command)

    def get_desktop_for_window(self, window="%1"):
        """
        Get the desktop number that a window is on.

        :param window: The window identifier (default is %1).
        :return: The output of the get_desktop_for_window command.
        """
        return self._run_command(["get_desktop_for_window", window])

    def set_desktop_for_window(self, window="%1", desktop_number=1):
        """
        Move a window to a different desktop.

        :param window: The window identifier (default is %1).
        :param desktop_number: The target desktop number.
        :return: The output of the set_desktop_for_window command.
        """
        return self._run_command(["set_desktop_for_window", window, str(desktop_number)])

    # Global Commands
    def get_desktop(self):
        """
        Get the current desktop number.

        :return: The output of the get_desktop command.
        """
        return self._run_command(["get_desktop"])

    def set_desktop(self, desktop_number):
        """
        Change the current desktop.

        :param desktop_number: The target desktop number.
        :return: The output of the set_desktop command.
        """
        return self._run_command(["set_desktop", str(desktop_number)])

    def get_num_desktops(self):
        """
        Get the current number of desktops.

        :return: The output of the get_num_desktops command.
        """
        return self._run_command(["get_num_desktops"])

    def set_num_desktops(self, num_desktops):
        """
        Change the number of desktops (KDE 5 only).

        :param num_desktops: The new number of desktops.
        :return: The output of the set_num_desktops command.
        """
        return self._run_command(["set_num_desktops", str(num_desktops)])


# Example usage
if __name__ == "__main__":
    kdotool = Kdotool(debug=True, bin=path.expanduser("~/.local/bin/kdotool"))
    print("Active window ID:", kdotool.get_active_window())
    print("Current desktop:", kdotool.get_desktop())
    print("Window name:", kdotool.get_window_name())