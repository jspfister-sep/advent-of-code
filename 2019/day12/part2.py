import math, re, sys

def get_lcm(numbers):
    lcm = numbers[0]
    for n in numbers[1:]:
        lcm = int(lcm * n / math.gcd(lcm, n))
    return lcm

class Axis:
    def __init__(self, position):
        self.__s0 = position
        self.__s = position
        self.__v = 0
        self.__v0 = 0

    def calculate_acceleration(self, others):
        acceleration = 0
        for o in others:
            if o.__s > self.__s:
                acceleration += 1
            elif o.__s < self.__s:
                acceleration -= 1
        return acceleration

    def update(self, acceleration):
        self.__v += acceleration
        self.__s += self.__v

    def is_at_initial_conditions(self):
        return (self.__s == self.__s0 and self.__v == self.__v0)

class Moon:
    def __init__(self, x, y, z):
        self.__axes = [Axis(x), Axis(y), Axis(z)]

    def calculate_acceleration(self, others):
        accelerations = []
        for i in range(len(self.__axes)):
            other_axes = [o.__axes[i] for o in others]
            accelerations.append(
                    self.__axes[i].calculate_acceleration(other_axes)
                    )
        return accelerations

    def update(self, accelerations):
        assert len(accelerations) == len(self.__axes)
        for i in range(len(self.__axes)):
            self.__axes[i].update(accelerations[i])

    def is_axis_at_initial_conditions(self, axis_index):
        return self.__axes[axis_index].is_at_initial_conditions()
            
POSITION_RE = re.compile('\<x=([\d-]+),\sy=([\d-]+),\sz=([\d-]+)\>')
AXIS_NAMES = ['x', 'y', 'z']

def main():
    moons = []
    with open(sys.argv[1], 'r') as f:
        for line in f:
            match = POSITION_RE.match(line.strip())
            assert match, 'No line match!'
            moons.append(Moon(
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3))))
    
    num_steps = 0
    axis_periods = [0, 0, 0] 
    period = 0
    while True:
        a = []
        for m1 in moons: 
            a.append(m1.calculate_acceleration([m2 for m2 in moons if m2 != m1]))
        for m in moons:
            m.update(a.pop(0))
        num_steps += 1
        for i in range(len(axis_periods)):
            if (axis_periods[i] == 0 and
                    all([m.is_axis_at_initial_conditions(i) for m in moons])):
                axis_periods[i] = num_steps
        if all(axis_periods):
            break

    print(f'Terminated after {num_steps} steps')

    for i in range(len(axis_periods)):
        print(f'{AXIS_NAMES[i]}-axis period: {axis_periods[i]}')

    print(f'It will take {get_lcm(axis_periods)} steps to reach a repeated state')

if __name__ == '__main__':
    main()

