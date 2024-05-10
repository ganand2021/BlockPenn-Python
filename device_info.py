import subprocess

def get_device_data():
    
    # Extract the IP address of the host
	cmd = "hostname -I | cut -d\' \' -f1"
	IP = subprocess.check_output(cmd, shell = True)
	# Retrieves CPU load information using the top -bn1 command, filters the output to 
	# include only lines with "load" using grep, and then uses awk to print the CPU load 
	# value in a formatted manner.
	cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
	CPU_load = subprocess.check_output(cmd, shell = True)
	# Retrieves memory usage information using the free -m command, then processes 
	# the output using awk to calculate and print the used memory, total memory, and usage percentage
	cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
	memory_usage = subprocess.check_output(cmd, shell = True)
	# Retrieves disk usage information using the df -h command and then processes the 
 	# output using awk to print the used and total disk space along with the usage percentage
	cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
	disk_usage = subprocess.check_output(cmd, shell = True)
 
	device_data = {
		"IP Address": str(IP.decode('utf-8')), 
        "CPU Load": CPU_load.decode('utf-8').split(': ')[1],
        "Memory Usage": memory_usage.decode('utf-8').split(': ')[1],
        "Disk Usage": disk_usage.decode('utf-8').split(': ')[1]
	}
	
	return device_data