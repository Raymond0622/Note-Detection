import os

# Location of music sheets to be analyzed
path = r"/Volumes/ESD-USB/OMR/chopin_nocturne_48"

# Location of outputs ofother files (i.e bounding box, staff_lines.jpg, ...)
p1 = r"/Volumes/ESD-USB/OMR/"
os.chdir(path)

# List the files names of sheet music. Each file name is at most 4 numbers filled with
# zeros in the front of the name.. (i.e 0001.jpg' should be the first file name)
lis = os.listdir(path)
lis = [str(i).zfill(4) + '.jpg' for i in range(8, 11)]

# Prints the name of each file

print(lis)

for i in range(len(lis)):
    s = lis[i]

    # Must always change directory to the main directory before the start of every stage
    os.chdir(p1)
    first_step = "python3 first_step_windows.py " + s + ' ' + path
    os.system(first_step)

    os.chdir(p1)
    second_step = "python3 second_step_windows.py " + "first_step.jpg " + ' ' + path
    os.system(second_step)

    os.chdir(p1)
    third_step = "python3 third_step_windows.py " + path
    os.system(third_step)

    os.chdir(p1)
    fourth_step = "python3 fourth_step_windows.py " + s + ' ' + path
    os.system(fourth_step)

    fifth_step = "python3 fifth_step_windows_opt.py " + s + ' ' + path + ' ' + str(i+7)
    os.system(fifth_step)
