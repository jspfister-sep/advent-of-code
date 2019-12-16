import sys

INPUTS = [
        '12345678',
        '80871224585914546619083218645595',
        '19617804207202209144916044189917',
        '69317163492948606335995924319873',
        '59796332430280528211060657577039744056609636505111313336094865900635343682296702094018432765613019371234483818415934914575717134617783515237300919201989706451524069044921384738930172026234872525254689609787752401342687098918804210494391161531008341329016626922990938854681575317559821067933058630688365067790812341475168200215494963690593873250884807840611487288560291748414160551508979374335267106414602526249401281066501677212002980616711058803845336067123298983258010079178111678678796586176705130938139337603538683803154824502761228184209473344607055926120829751532887810487164482307564712692208157118923502010028250886290873995577102178526942152'
        ]
EXPECTED_OUTPUTS = [
        (4, '01029498'),
        (100, '24176176'),
        (100, '73745418'),
        (100, '52432133'),
        (100, '36627552')
        ]

class FFT:
    BASE_PATTERN = [0, 1, 0, -1]

    def __init__(self, input_data):
        self.input_data = input_data

    def calculate(self, num_phases):
        patterns = self._generate_patterns()
        data = self.input_data
        for i in range(0, num_phases):
            output = []
            for j in range(0, len(data)):
                value = list(map(lambda a, b: a * b, data, patterns[j]))
                value = sum(value)
                value = int(str(value)[-1])
                output.append(value)
            assert len(data) == len(output)
            data = output
        return ''.join([str(digit) for digit in data])

    def _generate_patterns(self):
        patterns = []
        for i in range(len(self.input_data)):
            pattern = []
            base_pattern_index = 0
            while len(pattern) <= len(self.input_data):
                num_copies = min(i + 1, len(self.input_data) - len(pattern) + 1)
                copies = [self.BASE_PATTERN[base_pattern_index]] * num_copies
                pattern.extend(copies)
                base_pattern_index += 1
                base_pattern_index %= len(self.BASE_PATTERN)
            pattern.pop(0)
            patterns.append(pattern)
        return patterns

def get_output(input_index, num_phases):
    input_data = [int(digit) for digit in INPUTS[input_index]]
    fft = FFT(input_data)
    return fft.calculate(num_phases)

def main():
    if sys.argv[1] == 'test':
        success = True
        for i in range(len(INPUTS)):
            expected_output = EXPECTED_OUTPUTS[i][1]
            output = get_output(i, EXPECTED_OUTPUTS[i][0])
            output = output[:len(expected_output)]
            if output != expected_output:
                success = False
                print(f'Test {i} failed Expected: {expected_output} '
                    f'Actual: {output}')
        if success:
            print(f'{len(INPUTS)} tests passed')
    else:
        input_index = int(sys.argv[1])
        num_phases = int(sys.argv[2])
        output = get_output(input_index, num_phases)
        print(f'The output after {num_phases} phases is {output}')

if __name__ == '__main__':
    main()

