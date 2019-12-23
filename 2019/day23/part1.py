from intcode import Computer

NUM_COMPUTERS = 50

class Packet:
    def __init__(self, destination, x, y):
        self.destination = destination
        self.x = x
        self.y = y

def read_program():
    with open('data.txt', 'r') as f:
        program = f.read()
    program = program.strip().split(',')
    return [int(i) for i in program]

def run_network(computers):
    packet_queue = []
    while True:
        for i in range(len(computers)):
            c = computers[i]
            if c.has_output():
                packet = Packet(c.get_output(), c.get_output(), c.get_output())
                if packet.destination == 255:
                    return packet.y
                elif packet.destination < NUM_COMPUTERS:
                    packet_queue.append(packet)
            elif packet_queue and packet_queue[0].destination == i:
                packet = packet_queue.pop(0)
                c.set_input(packet.x)
                c.set_input(packet.y)
            else:
                c.set_input(-1)

def shut_down_network(computers):
    for c in computers:
        c.terminate()

def main():
    program = read_program()

    computers = [Computer(program) for i in range(NUM_COMPUTERS)]
    for i in range(len(computers)):
        computers[i].start()
        computers[i].set_input(i)

    y_value_255 = run_network(computers)
    shut_down_network(computers)
    print(f'The y value of the first packet sent to 255 is {y_value_255}')

if __name__ == '__main__':
    main()

