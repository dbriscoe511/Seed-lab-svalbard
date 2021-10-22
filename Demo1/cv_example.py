import computer_vision as cv
import subprocess
import sys
cmd = [sys.executable, "-c", "import computer_vision as cv; gains = cv.camera_setup(); cv.cv_main(gains)"]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
while process.poll() is None:
    angle = process.stdout.readline()
    angle = angle.decode('utf-8')
    angle.strip('\n')
    print(angle)

