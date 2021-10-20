import sys
import time
i=0
while True:
    i += 1
    sys.stdout.write("\n"+str(i))
    time.sleep(1)
    print("\nreading ")

    print(str(sys.stdin.read()))