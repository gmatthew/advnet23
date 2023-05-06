import os

FLOW_TYPES = {
    "elephant": "elephant",
    "mouse": "mouse"
}

link_rate = 100000000
elefant_flow_size = 48000000000

mouse_flow_size = 4000000
sim_time = 0
use_mouse_flow_priority = False

class Flow:
    def __init__(self,flow_id, flow_type, size, start_time):    
        self.flow_id = flow_id
        self.size = int(size)
        self.transfer_count = 0
        self.flow_type = flow_type
        self.start_time = start_time
        self.end_time = 0

    def transfer(self,rate):
        self.size -= int(rate)
        self.transfer_count += 1

    def get_size(self):
        return self.size

    def set_end_time(self, end_time):
        self.end_time = end_time

    def get_flow_type(self):
        return self.flow_type

    def __str__(self):
        return "Flow ID: " + str(self.flow_id) + " Size: " + str(self.size) + " Transfer Count: " + str(self.transfer_count) + " FCT: " + str((self.end_time - self.start_time) +1)


class FlowTable:
    def __init__(self):
        self.active_flows = []
        self.completed_flows = []
        self.link_rate = link_rate

    def add_flow(self,flow):
        self.active_flows.append( flow)
    
    def get_flows(self):
        return self.active_flows

    def get_completed_flows(self):
        return self.completed_flows

    def get_active_flow_count(self):
        return len(self.active_flows)

    def get_completed_flow_count(self):
        return len(self.completed_flows)

    def transfer_completed_flows(self, sim_time):

        for flow in self.active_flows:
            if flow.get_size() <= 0:
                flow.set_end_time(sim_time)
                self.completed_flows.append(flow)

        self.active_flows = [flow for flow in self.active_flows if flow.get_size() > 0]

    def print_table(self):
        for flow in self.active_flows:
            print(flow)

    def get_mouse_flow_count(self):
        return len([flow for flow in self.active_flows if flow.flow_type == FLOW_TYPES["mouse"]])

    def has_mouse_flows(self):
        return self.get_mouse_flow_count() > 0

def do_flow_transfer(sim_time):
    if use_mouse_flow_priority == True:
        transfer_with_mouse_flow_priority(sim_time)
    else:
        transfer_all_flows(sim_time)

def transfer_all_flows(sim_time):
    if flow_table.get_active_flow_count() == 0:
        return 

    rate = (link_rate / flow_table.get_active_flow_count()) /1000

    # print("-------------------")
    # print("Transfering at rate: " + str(rate))
    # print("-------------------")


    # print("Transfering...")
    for flow in flow_table.get_flows():
        flow.transfer(rate)

    # print("Removing completed flows...")
    flow_table.transfer_completed_flows(sim_time)


def transfer_with_mouse_flow_priority(sim_time):
    rate = (link_rate / flow_table.get_active_flow_count()) /1000

    has_mouse_flows = flow_table.has_mouse_flows()
    if has_mouse_flows == True:
        rate = (link_rate / flow_table.get_mouse_flow_count()) /1000


    # print("-------------------")
    # print("Transfering at rate: " + str(rate))
    # print("-------------------")

   

    # print("Transfering...")
    for flow in flow_table.get_flows():
        if has_mouse_flows == True:
            if flow.flow_type == FLOW_TYPES["mouse"]:
                flow.transfer(rate)
        else:
            flow.transfer(rate)

    # print("Removing completed flows...")
    flow_table.transfer_completed_flows(sim_time)



def print_stats(sim_time):
    pass
    # print("Afte Time: " + str(sim_time) + " Active Flows: " + str(flow_table.get_active_flow_count()) + " Completed Flows: " + str(flow_table.get_completed_flow_count()))

    


# Create Elephant Flows

flow_table = FlowTable()
flow_table.add_flow(Flow("M1", FLOW_TYPES["elephant"], elefant_flow_size, sim_time))
flow_table.add_flow(Flow("M2", FLOW_TYPES["elephant"],elefant_flow_size, sim_time))
flow_table.add_flow(Flow("M3", FLOW_TYPES["elephant"],elefant_flow_size, sim_time))
flow_table.add_flow(Flow("M4", FLOW_TYPES["elephant"],elefant_flow_size, sim_time))


# First Minute
for tick in range(0, 60000):
    do_flow_transfer(sim_time)
    sim_time += 1

    # flow_table.print_table()
    # if (tick % 1000 == 0):
    #     print_stats(sim_time)
    print(sim_time)

flow_table.print_table()
# Next 25 minutes
mouse_count = 0

while (mouse_count < 300):
    if (sim_time % 5000 == 0):
        flow_table.add_flow(Flow("m" + str(mouse_count+1), FLOW_TYPES["mouse"],mouse_flow_size, sim_time))
        mouse_count += 1

    # transfer all flows that are in the table
    do_flow_transfer(sim_time)
    
    # if (sim_time > 79):
    #     exit(0)

    sim_time += 1
    print(sim_time)

    # if (sim_time % 1000 == 0):
    #     print_stats(sim_time)

    # flow_table.print_table()

while (flow_table.get_active_flow_count() > 0):
    do_flow_transfer(sim_time)
    sim_time += 1

    if (sim_time % 1000 == 0):
        print_stats(sim_time)

    flow_table.print_table()

print_stats(sim_time)


for flow in flow_table.get_completed_flows():
    print(flow)