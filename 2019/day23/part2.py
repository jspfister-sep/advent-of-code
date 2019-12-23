from intcode import Computer
import copy

NUM_COMPUTERS = 50
NAT_ADDRESS = 255

class Packet:
    def __init__(self, destination, x, y):
        self.destination = destination
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.destination} {self.x} {self.y})'

def read_program():
    with open('data.txt', 'r') as f:
        program = f.read()
    program = program.strip().split(',')
    return [int(i) for i in program]

def run_network(computers):
    packet_queue = []
    previous_idle_y_value = None
    nat = None
    while True:
        idle = True
        for i in range(len(computers)):
            c = computers[i]
            if c.has_output():
                packet = Packet(c.get_output(), c.get_output(), c.get_output())
                if packet.destination == NAT_ADDRESS:
                    nat = packet
                elif packet.destination < NUM_COMPUTERS:
                    idle = False
                    packet_queue.append(packet)
            elif packet_queue and packet_queue[0].destination == i:
                idle = False
                packet = packet_queue.pop(0)
                c.set_input(packet.x)
                c.set_input(packet.y)
            else:
                c.set_input(-1)
            if idle and not packet_queue and nat:
                if nat.y == previous_idle_y_value:
                    return nat.y
                previous_idle_y_value = nat.y
                packet = copy.copy(nat)
                packet.destination = 0
                packet_queue.append(packet)

def shut_down_network(computers):
    for c in computers:
        c.terminate()

def main():
    program = read_program()

    computers = [Computer(program) for i in range(NUM_COMPUTERS)]
    for i in range(len(computers)):
        computers[i].start()
        computers[i].set_input(i)

    y_value = run_network(computers)
    shut_down_network(computers)
    print(f'The y value of the first repeated packet released to 0 is {y_value}')

if __name__ == '__main__':
    main()

