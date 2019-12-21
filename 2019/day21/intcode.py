import copy, threading

class Op:
    class Addr:
        RELATIVE = 0
        ABSOLUTE = 1
        
        def __init__(self, mode, value):
            self.mode = mode
            self.value = value

    def __init__(self, num_input_params, num_output_params):
        self.num_input_params = num_input_params
        self.num_output_params = num_output_params
    
    def execute(self):
        assert False, 'Must be implemented in derived class'

    def get_next_instruction_addr(self):
        ip_value = self.num_input_params + self.num_output_params + 1
        return Op.Addr(Op.Addr.RELATIVE, ip_value)

class Add(Op):
    def __init__(self):
        super().__init__(2, 1)

    def execute(self, param1, param2):
        return param1 + param2

class Multiply(Op):
    def __init__(self):
        super().__init__(2, 1)

    def execute(self, param1, param2):
        return param1 * param2

class Input(Op):
    def __init__(self, input_func):
        super().__init__(0, 1)
        self.input_func = input_func

    def execute(self):
        return self.input_func()

class Output(Op):
    def __init__(self, output_func):
        super().__init__(1, 0)
        self.output_func = output_func

    def execute(self, param):
        self.output_func(param)

class JumpIfTrue(Op):
    def __init__(self):
        super().__init__(2, 0)

    def execute(self, param1, param2):
        if param1 != 0:
            self.new_ip = Op.Addr(Op.Addr.ABSOLUTE, param2)
        else:
            self.new_ip = super().get_next_instruction_addr()
        
    def get_next_instruction_addr(self):
        return self.new_ip

class JumpIfFalse(Op):
    def __init__(self):
        super().__init__(2, 0)

    def execute(self, param1, param2):
        if param1 == 0:
            self.new_ip = Op.Addr(Op.Addr.ABSOLUTE, param2)
        else:
            self.new_ip = super().get_next_instruction_addr()
        
    def get_next_instruction_addr(self):
        return self.new_ip

class LessThan(Op):
    def __init__(self):
        super().__init__(2, 1)

    def execute(self, param1, param2):
        return 1 if param1 < param2 else 0

class Equals(Op):
    def __init__(self):
        super().__init__(2, 1)

    def execute(self, param1, param2):
        return 1 if param1 == param2 else 0

class AdjustRelativeBase(Op):
    def __init__(self):
        super().__init__(1, 0)

    def execute(self, param):
        return param

class Computer(threading.Thread):
    # Op Codes
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    ADJUST_REL_BASE = 9
    HALT = 99
    
    # Parameter Modes
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

    DEFAULT_OPS = {
        ADD: Add(),
        MULTIPLY: Multiply(),
        INPUT: None,
        OUTPUT: None,
        JUMP_IF_TRUE: JumpIfTrue(),
        JUMP_IF_FALSE: JumpIfFalse(),
        LESS_THAN: LessThan(),
        EQUALS: Equals(),
        ADJUST_REL_BASE: AdjustRelativeBase(),
    }

    def __init__(self, program):
        super().__init__()
        self.ops = copy.deepcopy(self.DEFAULT_OPS)
        self.ops[self.INPUT] = Input(self.__input_clbk)
        self.ops[self.OUTPUT] = Output(self.__output_clbk)
        self.memory = program.copy()
        self.__pause_event = threading.Event()
        self.__continue_event = threading.Event()
        self.__input = None
        self.__output = None
        self.__is_running = False

    def has_output(self):
        self.__pause_event.wait()
        output_available = self.__is_running and self.__output is not None
        return output_available

    def is_waiting_for_input(self):
        self.__pause_event.wait()
        input_needed = self.__is_running and self.__output is None
        return input_needed

    def is_terminated(self):
        self.__pause_event.wait()
        return not self.__is_running

    def set_input(self, input_param):
        self.__pause_event.wait()
        self.__pause_event.clear()
        assert self.__is_running, 'Not running!'
        assert self.__output is None, 'Not waiting for input! Output ready!'
        self.__input = input_param
        self.__continue_event.set()

    def get_output(self):
        self.__pause_event.wait()
        self.__pause_event.clear()
        assert self.__is_running, 'Not running!'
        assert self.__output is not None, 'No output ready! Waiting for input!'
        output_value = self.__output
        self.__continue_event.set()
        return output_value
        
    def terminate(self):
        self.__pause_event.wait()
        self.__pause_event.clear()
        self.__is_running = False
        self.__continue_event.set()
        self.join()

    def run(self):
        self.__is_running = True
        instruction_addr = 0
        relative_base = 0
        
        while instruction_addr < len(self.memory):
            opcode = self._get_opcode(instruction_addr)
            if opcode == self.HALT:
                break
            op = self._get_op(instruction_addr)
            param_addrs = self._get_param_addrs(instruction_addr, relative_base)
            input_param_addrs = param_addrs[:op.num_input_params]
            input_params = self._read_params(input_param_addrs)
            output_value = op.execute(*input_params)
            if not self.__is_running:
                break
            elif opcode == self.ADJUST_REL_BASE:
                relative_base += output_value
            elif op.num_output_params > 0:
                self._write_param(param_addrs[-1], output_value)
            instruction_addr = self._get_next_instr_addr(op, instruction_addr)
        else:
            assert False, 'Never encountered a terminate instruction'
        self.__is_running = False
        self.__pause_event.set()

    def __input_clbk(self):
        self.__pause_event.set()
        self.__continue_event.wait()
        self.__continue_event.clear()
        assert self.__input is not None, 'No input set!'
        input_value = self.__input
        self.__input = None
        return input_value

    def __output_clbk(self, param):
        assert self.__output is None, 'Previous output not read!'
        self.__output = param
        self.__pause_event.set()
        self.__continue_event.wait()
        self.__continue_event.clear()
        self.__output = None

    def _get_next_instr_addr(self, op, instruction_addr):
        next_instruction_addr = op.get_next_instruction_addr()
        if next_instruction_addr.mode == Op.Addr.RELATIVE:
           return instruction_addr + next_instruction_addr.value
        elif next_instruction_addr.mode == Op.Addr.ABSOLUTE:
            return next_instruction_addr.value
        else:
            assert False, ('Bad next instruction address mode'
                f'{next_instruction_addr.mode}')

    def _get_op(self, instruction_addr):
        return self.ops[self._get_opcode(instruction_addr)]

    def _get_opcode(self, instruction_addr):
        return int(str(self.memory[instruction_addr])[-2:])

    def _get_param_addrs(self, instruction_addr, relative_base):
        param_addrs = []
        op = self._get_op(instruction_addr)
        num_total_params = op.num_input_params + op.num_output_params
        instruction = self.memory[instruction_addr]
        param_modes = self._get_param_modes(instruction, num_total_params)
        for i in range(0, num_total_params):
            param_instruction_addr = instruction_addr + i + 1
            param_mode = param_modes[i]
            if param_mode == self.POSITION:
                param_addr = self.memory[param_instruction_addr]
            elif param_mode == self.RELATIVE:
                param_addr = relative_base + self.memory[param_instruction_addr]
            else:
                param_addr = param_instruction_addr
            param_addrs.append(param_addr)
        return param_addrs
    
    def _get_param_modes(self, instruction, num_params):
        instruction = str(instruction)
        parameter_modes = []
        for i in range(0, num_params):
            if i < len(instruction) - 2:
                parameter_modes.append(int(instruction[-3 - i]))
            else:
                parameter_modes.append(self.POSITION)
        return parameter_modes

    def _read_param(self, param_addr):
        if param_addr >= len(self.memory):
            return 0
        return self.memory[param_addr]

    def _read_params(self, param_addrs):
        params = []
        for a in param_addrs:
            params.append(self._read_param(a))
        return params

    def _write_param(self, param_addr, value):
        if param_addr >= len(self.memory):
            self.memory.extend([0] * (param_addr - len(self.memory) + 1))
        self.memory[param_addr] = value

