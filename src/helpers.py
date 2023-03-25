import threading
import time
import sys
import os

"""
Function that generates a thread with function return 
"""
class MyThread(threading.Thread):
    
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
 
    def run(self):
        time.sleep(2)
        self.result = self.func(*self.args)
 
    def get_result(self):
        threading.Thread.join(self) 
        try:
            return self.result
        
        except Exception:
            return None

"""
Applies a custom loader text to some process
"""
class Loader: 

    def run(self, _callback, info):
        t = MyThread(_callback)
        t.start()      
        
        while(t.is_alive()):
            for c in ['|', '/', '-', '\\']:
                sys.stdout.write(f'\r{info} ' + c)
                sys.stdout.flush()
                time.sleep(0.1)
                
        os.system('cls')       
        return t.get_result()
    
"""
Generates a progress bar for some process
"""
class ProgressBar:
    
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    def printProgressBar (  self,
                            iteration, 
                            total, prefix = '', 
                            suffix = '', 
                            decimals = 1, 
                            length = 100, 
                            fill = '█', 
                            printEnd = "\r"):

        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        
        if iteration == total: 
            print()

"""
Function that takes a all the componentes from a list to a string 
separated by commas 
"""
class StringBuilder: 

    def listString(self, lt):
        st = ""
        for i in lt: 
            st += i + ','

        st = st[:-1]
        return st
