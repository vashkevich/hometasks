#Import some modules for gathering computer stats by our application
import datetime, time, configparser, schedule, psutil, json

#Import config file
ini_file = configparser.ConfigParser()
ini_file.read('appconf.ini')
output = ini_file.get('common', 'output')
interval = ini_file.get('common', 'interval')
#Special variable for counting snapshots
snap_count = 0

#Parent class, gathering information
class system_info:
    def __init__(self):
        tm = time.time()
        self.cpu = ('CPU load: '+str(psutil.cpu_percent(0, 0))+' %')
        self.vm = ('Virtual memory usage: '+str((psutil.virtual_memory().used/1024/1024).__round__(1))+' MB')
        self.swap = ('SWAP usage: '+str((psutil.swap_memory().used/1024/1024).__round__(1))+' MB')
        self.io_read = ('I/O info (read): '+str((psutil.disk_io_counters()[3]/1024/1024).__round__(1))+' MB')
        self.io_write = ('I/O info (write): '+str((psutil.disk_io_counters()[4]/1024/1024).__round__(1))+' MB')
        self.net_sent = ('Network data (sent): '+str((psutil.net_io_counters(pernic=False)[0]/1024/1024).__round__(2))+' MB')
        self.net_received = ('Network data (received): ' + str((psutil.net_io_counters(pernic=False)[1]/1024/1024).__round__(2))+' MB')
        self.timestamp = datetime.datetime.fromtimestamp(tm).strftime('%Y-%m-%d %H:%M:%S')

#Child class, writing information into files
class txt_output (system_info):

    def __init__(self):
        super().__init__()

    def sum_data(self, filename = 'system_monitoring.txt'):
#Snapshot number counter
        global snap_count
        snap_count += 1
        data = open(filename, 'a+')
        data.write('SNAPSHOT # ' + str(snap_count) + ': ' + str(self.timestamp))
        data.write('\n' + self.cpu)
        data.write('\n' + self.vm)
        data.write('\n' + self.swap)
        data.write('\n' + self.io_read)
        data.write('\n' + self.io_write)
        data.write('\n' + self.net_sent)
        data.write('\n' + self.net_received+ '\n'+'\n')


class json_output (system_info):

    def __init__(self):
        super().__init__()

    def jsonfile(self, filename='system_monitoring.json'):
        global snap_count
        snap_count += 1
# creating dictionary to store monitoring information
        jmonitoring = [self.cpu, self.vm, self.swap, self.io_read, self.io_write, self.net_sent, self.net_received]
# setting information format
        data = ['SNAPSHOT # ' + str(snap_count) + ': ' + str(self.timestamp), jmonitoring]
# writing data to json
        with open(filename, 'a+') as js:
            json.dump(data, js, indent=4, sort_keys=True)

def out():
    if output == 'txt':
        out_text = txt_output()
        out_text.sum_data()
    elif output == 'json':
        out_json = json_output()
        out_json.jsonfile()
    else:
        quit()

#Set up schedule for our application
schedule.every(int(interval)).minutes.do(out)

while True:
    schedule.run_pending()
