# Linux_Internals_shell_implementation

This project uses a python script to implement the shell of Linux. For that, I used os.fork method, which creates a child process.


### Prerequisites

OS - Linux
Python - python3

### Supported functionality

- Running the program the user requested
- Searching the binary file within /bin/, /usr/bin and /usr/share/bin
- Passing command arguments
- Support output redirection via the ‘>’ character
- Running commands in the background, if the last character is ‘&’

### Unsupported functionality

- Changing current directories (the cd command)
- pipes
- comments

### Using the script

```
 python3 shell_script.py
Welcome to your shell!
please enter you user name: Genady
$: echo Hi!
Hi!
$: ls
shell_script.py
$: sleep 5 &
$: ls > ls_output
$: 
```
 