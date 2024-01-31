import threading
import time
 
def print_cube():
    time.sleep(5)
    print("DONE CUBE")
 
 
def print_square():
    time.sleep(5.1)
    print("DONE SQUARE")
 
 
if __name__ =="__main__":
    t1 = threading.Thread(target=print_square)
    t2 = threading.Thread(target=print_cube)
 
    t1.start()
    t2.start()

    t1.join()
    t2.join()
 