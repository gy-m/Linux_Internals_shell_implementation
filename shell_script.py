"""
Author: Genady Makievsky
"""
# import os.fork
# import os.execv
import os
import sys

DELIMITER = ' '


def wait_for_all_process_logic(flag_amp):
    """
    get to here for processes that need to wait untill the former process ("the child") will be terminated
    :param flag_amp: None
    :return:
    """
    if not flag_amp:
        os.wait()
    return


def check_amp(user_input):
    """
    check if the user uses &
    :param user_input: user input
    :return: flag which indicates the result
    """
    if not user_input.find('&') == -1:
        user_input = user_input[:-2]
        return True
    else:
        return False


def check_greater(user_input):
    """
    check if the user uses >
    :param user_input: user input
    :return: flag which indicates the result
    """
    if not user_input.find('>') == -1:
        return True
    else:
        return False


def do_command(user_input, path):
    """
    :param user_input: user input
    :param path: path list for the pissible destination of the user commands
    :return: None
    """

    user_input = user_input.strip()
    flag_greater = check_greater(user_input)

    flag_amp = False                            # initialize for the flag
    if user_input.split(DELIMITER)[-1] == '&':
        user_input = user_input[:-2]
        flag_amp = True

    if not flag_greater:
        # do not do redirection
        pid = os.fork()                              # make a new process
        if pid == 0:
            # this is new born child process (will get the "user command" as his program instance)
            user_command = user_input.split()[0]
            os.execv(path + user_command, user_input.split(DELIMITER))
            return
        else:
            # this is the father process: by default (continue to have "shell" as his program instance)
            wait_for_all_process_logic(flag_amp)

    else:
        # do redirection
        user_input_part_1 = user_input.split('>')[0].strip()
        user_command = user_input_part_1.split(DELIMITER)[0]
        path_to_redirect = user_input.split('>')[1]

        pid = os.fork()
        if pid == 0:
            # child
            fd_new = os.open(path_to_redirect, os.O_WRONLY | os.O_CREAT)        # make a new file descriptor, which represented by int (type = program instance for new file)
            os.close(1)
            # close file descriptor 1 (type = program instance for printing to the std output).
            os.dup2(fd_new, 1)
            os.execv(path + user_command, user_input_part_1.split(DELIMITER))
        else:
            # father
            wait_for_all_process_logic(flag_amp)


def my_shell():
    print("Welcome to your shell!")
    usr = input("please enter you user name: ")

    # initialite possible paths for the commands
    bin_path = '/bin/'
    usr_path = '/' + usr + bin_path
    shared_path = '/' + usr + '/share' + bin_path
    path = ['/usr/bin/', bin_path, usr_path, shared_path]

    # make the program "my_shell" a continuous program
    while True:
        user_input = input("$: ")
        i = 0
        # try to find the command in all the legal paths
        try:
            do_command(user_input, path[i])
        except FileNotFoundError as err:
            if i < 3:
                i += 1
                do_command(user_input, path[i])
            else:
                print(err)


def main():
    """
    description:
    the main runs 1 program names "my_shell" and operates like a minimal shell
    :return:
    """
    my_shell()


if __name__ == "__main__":
    main()
