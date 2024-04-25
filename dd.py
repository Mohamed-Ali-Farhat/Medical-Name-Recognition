import os
import subprocess

def run_chdoula():
    # Get the current directory
    current_directory = os.path.dirname(os.path.realpath(__file__))
    
    # Construct the full path to chdoula.py
    chdoula_path = os.path.join(current_directory, "C:/Users/MSI/Desktop/chdoula-ya-m3alem-main/chdoula.py")
    
    # Run chdoula.py using subprocess
    subprocess.Popen(["python", chdoula_path])

if __name__ == "__main__":
    run_chdoula()
