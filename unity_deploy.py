import os
import shutil

def run_linux(command):
    print "$ " + command
    os.system(command)

def fail_build():
    print "Build failed"
    exit(0)

def check_path(expected_path, expected_file):
    print "Checking path" + expected_path + "..."
    if not os.path.isfile(expected_path + "/" + expected_file):
        print "Resouce not at expected path."
        fail_build()
    else:
        print "Check passed."

if __name__ == '__main__':
    print "Moving the built project to the static folder."

    expected_path = "aimmo-unity/Build"
    check_path(expected_path, "index.html")

    unity_folder = "players/static/unity"
    print "Copying the build to the static resources folder:"
    run_linux("cp -r " + expected_path + " " + unity_folder)
    check_path(unity_folder, "index.html")

    dependencies_folder = "aimmo-unity/Dependencies"
    print "Copying the Dependencies folder: " + dependencies_folder
    run_linux("cp -r " + dependencies_folder + " " + unity_folder)
    check_path(unity_folder + "/Dependencies", "socket.io.js")
