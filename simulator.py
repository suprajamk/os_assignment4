'''
CS5250 Assignment 4, Scheduling policies simulator
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
'''
import sys
import copy

input_file = 'input.txt'

class Process:

    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
        self.last_scheduled_time = arrive_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrive_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def find_unique_process(to_be_processed):
    ids = set()
    for process in to_be_processed:
        ids.add(process.id)
    return ids

def find_max_simulation_time(process_list):
    n = len(process_list)
    last_process = process_list[n-1]
    max_time = last_process.arrive_time + last_process.burst_time
    return max_time+30

def init_expected_burst_time(to_be_processed, initial_guess):
    expected_burst_time = {}
    for process in to_be_processed:
        expected_burst_time[process.id] = initial_guess
    return expected_burst_time


def find_expected_burst_time(alpha,actual_burst_time,prev_expected):
    expected_burst = (alpha * actual_burst_time) + (1 - alpha) * prev_expected
    return expected_burst

def insert_into_wait_list_queue(wait_list, curr_process):
    ids = set()
    for process in wait_list:
        ids.add(process.id)
    print (ids)
    index = len(ids) - 1
    prev_process = wait_list[index]
    if(prev_process.arrive_time >= curr_process.arrive_time):
        wait_list.insert(index+1, curr_process)
    else:
        wait_list.insert(index, curr_process)
    return wait_list

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum):
    current_time = 0
    waiting_time = 0
    processing_queue = []
    to_be_processed = copy.deepcopy(process_list)
    schedule = []

    max_time = find_max_simulation_time(process_list)

    while current_time < max_time:
        while to_be_processed.__len__() > 0:
            tbd_process = to_be_processed[0]
            arrival = tbd_process.arrive_time
            if arrival <= current_time+time_quantum:
                processing_queue.append(tbd_process)
                to_be_processed.pop(0)
            else:
                break

        if processing_queue.__len__() > 0:
            current_process = processing_queue[0]
            arrival = current_process.arrive_time
            if arrival <= current_time:
                current_process = processing_queue.pop(0)
                if current_time < current_process.last_scheduled_time:
                    current_time = current_process.last_scheduled_time
                waiting_time = waiting_time + (current_time - current_process.last_scheduled_time);
                schedule.append((current_time, current_process.id))  # processing
                if current_process.burst_time > time_quantum:
                    current_time += time_quantum
                    current_process.burst_time -= time_quantum
                    current_process.last_scheduled_time = current_time
                    processing_queue.append(current_process)
                else:
                    current_time += current_process.burst_time
                    current_process.burst_time = 0
                    current_process.last_scheduled_time = current_time
            else:
                current_time += 1
        else:
            current_time += 1

    average_waiting_time = waiting_time / float(len(process_list))
    return schedule, average_waiting_time

def SRTF_scheduling(process_list):
    current_time = 0
    waiting_time = 0
    processing_queue = []
    to_be_processed = copy.deepcopy(process_list)
    schedule = []

    max_time = find_max_simulation_time(process_list)

    while current_time < max_time:
        if to_be_processed.__len__() > 0:
            tbd_process = to_be_processed[0]
            if tbd_process.arrive_time == current_time:
                processing_queue.append(tbd_process)
                to_be_processed.pop(0)

        if processing_queue.__len__() > 0:
            processing_queue = sorted(processing_queue, key=lambda x: x.burst_time)
            curr_process = processing_queue.pop(0)
            schedule.append((current_time, curr_process.id))  # processing
            if curr_process.burst_time > 1:
                curr_process.burst_time -= 1
                waiting_time = waiting_time + (current_time - curr_process.last_scheduled_time)
                current_time += 1
                curr_process.last_scheduled_time = current_time
                processing_queue.append(curr_process)
            else:
                curr_process.burst_time = 0
                waiting_time = waiting_time + (current_time - curr_process.last_scheduled_time)
                current_time += 1
                curr_process.last_scheduled_time = current_time
        else:
            current_time += 1

    average_waiting_time = waiting_time / float(len(process_list))
    return schedule, average_waiting_time

def SJF_scheduling(process_list, alpha):
    current_time = 0
    waiting_time = 0
    processing_queue = []
    to_be_processed = copy.deepcopy(process_list)
    schedule = []

    max_time = find_max_simulation_time(process_list)

    expected_burst_time = init_expected_burst_time(to_be_processed, initial_guess=5)

    while current_time < max_time:
        while to_be_processed.__len__() > 0:
            tbd_process = to_be_processed[0]
            arrival = tbd_process.arrive_time
            if arrival <= current_time:
                process_id = tbd_process.id
                tbd_process.expected_btime = expected_burst_time[process_id]
                processing_queue.append(tbd_process)
                to_be_processed.pop(0)
            else:
                break

        if processing_queue.__len__() > 0:
            processing_queue = sorted(processing_queue, key=lambda x: x.expected_btime)
            current_process = processing_queue.pop(0)
            waiting_time = waiting_time + (current_time - current_process.last_scheduled_time);
            schedule.append((current_time, current_process.id))  # processing
            current_time += current_process.burst_time
            process_id = current_process.id
            expected_burst_time[process_id] = find_expected_burst_time(alpha, current_process.burst_time, current_process.expected_btime)
        else:
            current_time += 1

    average_waiting_time = waiting_time / float(len(process_list))
    return schedule, average_waiting_time


def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])
