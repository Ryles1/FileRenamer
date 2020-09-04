#! python3
"""FileRenamer.py - This script works by accepting a network directory from the user and renaming the files in that
directory with a user-selected prefix and a numerically ascending suffix while retaining the file extension."""

import os
from time import sleep
from sys import exit
from shutil import copyfile


def get_path():
    while True:
        print('Please enter the absolute network path to the directory containing the files you would like to rename:')
        raw_dir = input()
        if not os.path.exists(raw_dir):
            print('That directory does not exist, please try again.')
        elif not os.path.isabs(raw_dir):
            print('Please enter an absolute network path. (Absolute paths begin with a letter and :\\)')
        else:
            return raw_dir


def get_prefix():
    print('''The filename prefix can be any string you choose, but cannot contain any characters not allowed 
    in a filename.  Choose carefully.\n''')
    while True:
        prefix = input('Please enter the prefix to be used')
        not_allowed = ['\\', '/', '*', '?', '"', '|', '<', '>']
        for c in not_allowed:
            if c in prefix:
                print('The prefix entered contains a character that is not allowed in filenames.  Try again.')
                continue
        break
    while True:
        char = input('Please enter the character to use to join the prefix and suffix')
        if char in not_allowed:
            print('The character entered is not allowed in filenames.  Try again.')
            continue
        else:
            break
    return prefix, char


def get_suffix():
    print('''The filename will have an integer suffix (starting at 0) appended.  You can select the length of 
    this suffix.  The suffix will be padded to the left with zeros to match the requested length.\n''')
    while True:
        length = int(input('Please enter the required length of the numeric suffix:'))
        if not isinstance(length, int):
            print('Please enter an integer.')
        elif int(length) < 1 or int(length) > 10:
            print('Please enter a positive integer of reasonable length (10 or less).')
        else:
            length = int(length)
            break
    return length


def get_new_name(old_name, suf, length, pre, join_char):
    new_suffix = '0' * (length - len(str(suf))) + str(suf)
    filetype = '.' + old_name.split('.')[-1]
    new = join_char.join([pre, new_suffix, filetype])
    return new


def main():
    print('''This is the FileRenamer tool. This tool will rename all the files in your chosen directory with a prefix
    of your choice, and a numerically ascending suffix of your chosen length, separated by a character of 
    your choice.\n''')
    sleep(1)
    # Get directory from user and check it exists, then change cwd to this directory.

    working_dir = get_path()
    os.chdir(working_dir)
    sleep(1)

    # Get the filename prefix and separator character from the user
    prefix, joiner = get_prefix()
    print(f'File name prefix is {prefix}.')
    print(f' Joining character is {joiner}.')
    sleep(1)

    # Get suffix length - suffix will be front padded with zeros to required length
    suffix_len = get_suffix()
    print(f'Suffix length is {suffix_len}.')
    sleep(1)

    # Get list of files in the directory and print the first 5 filenames for user confirmation
    # If number of files is large (>50), warn user and get extra confirmation
    filenames = os.listdir()
    for i in range(5):
        print(sorted(filenames)[i])
    exit_flag = input('These are the first 5 files in the folder.  Please confirm you want to continue (y/n):')
    if len(filenames) > 50:
        exit_flag = input('There are many files in this directory (> 50).  Please confirm you want to continue (y/n):')
    if exit_flag.lower() == 'n':
        exit('Program aborted successfully.')

    # Create a backup directory
    os.makedirs('FileRenamerBackup', exist_ok=True)

    # For each file, save as is in the backup, open the file and save with new name
    # TODO: make a list of file types to ignore
    suffix = 1
    base_dir = os.path.abspath(os.getcwd())
    copy_dir = os.path.join(base_dir, 'FileRenamerBackup')
    failed_copies = []
    for file in filenames:
        try:
            print(f'Attempting to backup {file}')
            copyfile(os.path.join(base_dir, file), os.path.join(copy_dir, file))
            new_name = get_new_name(file, suffix, suffix_len, prefix, joiner)
            print(f'Backup successful, new file name is {new_name}')
            # os.rename(file, new_name)
        except:
            print(f'Error with backup of {file} - file not renamed.')
            failed_copies.append(file)

    if len(failed_copies) > 0:
        print(f'{len(failed_copies)} of {len(filenames)} files not renamed.')
        print('The following files were not renamed:\n')
        for name in failed_copies:
            print(name)
    else:
        print('All files renamed successfully.')


if __name__ == '__main__':
    main()
