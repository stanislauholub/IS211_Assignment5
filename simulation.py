#!/usr/bin/env python
# coding: utf-8

# In[527]:


import time
import urllib
import argparse
import csv
import sys

# PART I (PULLING DOWN THE CSV FILE)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', 
                        by_default = 'http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv', 
                        type = str)
    args = parser.parse_args()
    if args.input == None:
        sys.exit()

def downloadData(url):
    dwnld = url
    urllib.request.urlretrieve(dwnld, 'requests.csv')

# PART II (MAIN QUEUE CLASS)

class Queue:
    def __init__(self):
            self.items = []
    def is_empty(self):
        return self.items == []
    def enqueue(self, item):
        self.items.insert(0, item)
    def dequeue(self):
        return self.items.pop()
    def size(self):
        return len(self.items)

# PART III (SERVER or PRINTER CLASS IN THE READINGS)

class Server:
    def __init__(self):        
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None
    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False
    def start_next(self,new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_length()

# PART IV (REQUEST or TASK CLASS IN THE READINGS)

class Request:
    def __init__(self, time, process_time):
        self.timestamp = time
        self.length = process_time
    def get_stamp(self):
        return self.timestamp
    def get_length(self):
        return self.length
    def wait_time(self, cur_time):
        return cur_time - self.timestamp

# PART V (ONE SERVER SIMULATION)

def simulateOneServer(datafile, servers_number):
    server_request = Server()
    server_queue = Queue()
    waiting_times = []

    with open(datafile) as data:
        datafile = csv.reader(data)

        for row in datafile:
            request_time = int(row[0])
            address_line = row[1]
            process_time = int(row[2])
            gen_request = Request(request_time, process_time)
            server_queue.enqueue(gen_request)

            if not server_request.busy() and not server_queue.is_empty():
                next_request = server_queue.dequeue()
                waiting_times.append(next_request.wait_time(request_time))
                server_request.start_next(gen_request)

            server_request.tick()

    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs %3d tasks remaining." 
          % (average_wait, server_queue.size()))
    """I'm not sure if it works properly, since 2k+ average wait time seems too much to me. 
    "Request" class probably needs some additional fixes."""
    
# PART VI (MANY SERVERS SIMULATION + ROUND-ROBIN FASHION)
    
def simulateManyServers(datafile, servers_number):
    servers_request = ([])
    servers_queue = ([])
    waiting_times = ([])
    for number in range(0, servers_number):
        servers_request.append(Server())
        servers_queue.append(Queue())
        waiting_times.append([])

    with open(datafile) as data:
        datafile = csv.reader(data)
        
        add = 0
        for row in datafile:
            request_time = int(row[0])
            address_line = row[1]
            process_time = int(row[2])
            gen_requests = Request(request_time, process_time)
            servers_queue[add].enqueue(gen_requests)
            if add < servers_number - 1:
                add += 1
            else:
                add = 0
            if not servers_request[add].busy() and not servers_queue[add].is_empty():
                next_request = servers_queue[add].dequeue()
                waiting_times[add].append(next_request.wait_time(request_time))
                servers_request[add].start_next(gen_requests)
                
            servers_request[add].tick()

        for number in range(0, servers_number):
            average_wait = sum(waiting_times[number]) / len(waiting_times[number])        
            print("Average Wait %6.2f secs %3d tasks remaining."
                  % (average_wait, servers_queue[number].size()))
    """I'm not sure if it works properly, since 2k+ average wait time seems too much to me. 
    "Request" class probably needs some additional fixes."""
        
# TESTS

if __name__ == "__main__":
    
    url = str(input("Enter Url: "))
    downloadData(url)
    servers_number = int(input("Enter number of network requests: "))
    if(servers_number <= 0):
        print("No connection")
    elif(servers_number == 1):
        load = simulateOneServer('requests.csv', servers_number)
    else:
        load = simulateManyServers('requests.csv', servers_number)
        
    #main('requests.csv', -1)
    #main('requests.csv', 0)
    #main('requests.csv', 1)
    #main('requests.csv', 5)


# In[ ]:
