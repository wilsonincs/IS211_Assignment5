__author__ = 'wilsonincs'
import urllib2
import argparse
import csv


#Define the server class
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
        self.time_remaining = new_task.get_time()


#Define the request class
class Request:
    def __init__(self,request):
        self.timestamp = int(request[0])
        self.timeleft  = int(request[2])

    def get_stamp(self):
        return self.timestamp

    def get_time(self):
        return self.timeleft

    def wait_Time(self, current_time):
        return current_time - self.timestamp


# Define the Queue class

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self,item):
        self.items.insert(0,item)


    def dequeue(self):
        return self.items.pop()

    def pop(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)



#define a function that will simulate one server

def simulateOneServer(filename):
    server = Server()
    queue  = Queue()
    wait_time = []
    request_dict = {}

    for request in filename:
        n_time = int(request[0])
        queue.enqueue(request)

        if n_time in request_dict:
            request_dict[n_time].append(request)
        else:
            request_dict[n_time] = [request]

    for time_in_second in request_dict:
        for req in request_dict[time_in_second]:
            Request(req)
            queue.dequeue()

        if (not server.busy()) and (not queue.isEmpty()):
            nextreq = Request(queue.dequeue())
            wait_time.append(nextreq.wait_Time(nextreq))
            #breaks after this line
            server.startNext(nextreq)

        server.tick()

    average = sum(wait_time)/len(wait_time) * 0.001
    print(" The average Waiting time is %2.2f secs for %3d requests."%(average,queue.size()))


def main():
    url_parser = argparse.ArgumentParser()
    url_parser.add_argument("--file", help=' Please enter a valid URL CSV file', type=str)
    arguments = url_parser.parse_args()

    if arguments.file:
        try:
            filename = csv.reader(urllib2.urlopen(arguments.file))
            simulateOneServer(filename)

        except:
            print "please revise the URL it may not be valid."
    else:
        print "Please enter a valid URL CSV file --file. "


if __name__ == "__main__":
    main()



