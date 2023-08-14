import queue
import logging
from collections import defaultdict


class IntCodeComputer:

    # setup section

    def __init__(self, id: int) -> None:
        # base data
        self.id = id
        self.memory = defaultdict(int)

        # Registers
        self.__pc = 0
        self.relative_base = 0

        # Input
        self.input_queue = queue.SimpleQueue()

        # Output
        self.output_value = 0
        self.output_set = False
        self.output_stop_mode = False

        # Misc
        self.program_finished = False

    def __str__(self) -> str:
        return f"CPU [{self.id}] - pc:{self.pc_peek()} - memsize:{len(self.memory)}"

    def load_program(self, program_string: str) -> None:
        load_counter = 0
        for int_value in program_string.split(","):
            self.memory[load_counter] = int(int_value)
            load_counter += 1

    # registers section

    def pc_peek(self) -> int:
        return self.__pc

    def set_pc(self, new_pc_value) -> None:
        self.__pc = new_pc_value

    # memory section

    def next_value(self) -> int:
        value = self.memory[self.__pc]
        self.__pc += 1
        return value

    def get_mem(self, address: int) -> int:
        return self.memory[address]

    def set_mem(self, address: int, value: int) -> None:
        self.memory[address] = value

    def read(self, parameter: int, mode: int) -> int:
        match mode:
            case 0:
                return self.get_mem(parameter)
            case 1:
                return parameter
            case 2:
                return self.get_mem(self.relative_base + parameter)
            case _:
                raise Exception(f"[{self.id}] - Invalid addressing mode '{mode}'")

    def write(self, target, value, mode):
        match mode:
            case 0:
                self.set_mem(target, value)
            case 1:
                raise Exception(f"[{self.id}] - Direct mode for writing not allowed!")
            case 2:
                self.set_mem(self.relative_base + target, value)
            case _:
                raise Exception(f"[{self.id}] - Invalid addressing mode '{mode}'")

    # runtime section

    def run(self):
        stopped = False
        while not stopped:
            stopped = self.step()

    def step(self) -> bool:
        opcode_struct = self.next_value()

        # parse parameter modes
        opcode = (opcode_struct % 10) + ((opcode_struct % 100) // 10) * 10
        param1_mode = (opcode_struct % 1000) // 100
        param2_mode = (opcode_struct % 10000) // 1000
        param3_mode = (opcode_struct % 100000) // 10000

        match opcode:
            case 1:
                self.opcode_add(param1_mode, param2_mode, param3_mode)
            case 2:
                self.opcode_multiply(param1_mode, param2_mode, param3_mode)
            case 3:
                self.opcode_input(param1_mode)
            case 4:
                self.opcode_output(param1_mode)
                if self.output_stop_mode:
                    logging.info(f"[{self.id}] - stopping after output")
                    return True
            case 5:
                self.opcode_jump_if_true(param1_mode, param2_mode)
            case 6:
                self.opcode_jump_if_false(param1_mode, param2_mode)
            case 7:
                self.opcode_less_than(param1_mode, param2_mode, param3_mode)
            case 8:
                self.opcode_equals(param1_mode, param2_mode, param3_mode)
            case 9:
                self.opcode_set_relative_base(param1_mode)
            case 99:
                logging.info(f"[{self.id}] - program done")
                self.program_finished = True
                return True
            case _:
                raise Exception(f"[{self.id}] - Invalid opcode '{opcode}'")
        return False

    def opcode_add(self, param1_mode, param2_mode, param3_mode) -> None:
        source_1 = self.read(self.next_value(), param1_mode)
        source_2 = self.read(self.next_value(), param2_mode)
        target = self.next_value()
        self.write(target, source_1 + source_2, param3_mode)

    def opcode_multiply(self, param1_mode, param2_mode, param3_mode) -> None:
        source_1 = self.read(self.next_value(), param1_mode)
        source_2 = self.read(self.next_value(), param2_mode)
        target = self.next_value()
        self.write(target, source_1 * source_2, param3_mode)

    def opcode_input(self, param1_mode) -> None:
        target = self.next_value()
        if self.input_queue.empty():
            value = int(
                input(
                    f"[{self.id}] - Please enter an integer to be stored at {target}:"))
        else:
            value = self.input_queue.get()
            logging.info(
                f"[{self.id}] - Read {value} from input queue into {target}")
        self.write(target, value, param1_mode)

    def opcode_output(self, param1_mode) -> None:
        value = self.read(self.next_value(), param1_mode)
        logging.info(f"[{self.id}] - output: {value}")
        self.output_value = value
        self.output_set = True

    def opcode_jump_if_true(self, param1_mode, param2_mode) -> None:
        source_1 = self.read(self.next_value(), param1_mode)
        source_2 = self.read(self.next_value(), param2_mode)
        if source_1 != 0:
            self.set_pc(source_2)

    def opcode_jump_if_false(self, param1_mode, param2_mode) -> None:
        source_1 = self.read(self.next_value(), param1_mode)
        source_2 = self.read(self.next_value(), param2_mode)
        if source_1 == 0:
            self.set_pc(source_2)

    def opcode_less_than(self, param1_mode, param2_mode, param3_mode) -> None:
        source_1 = self.read(self.next_value(), param1_mode)
        source_2 = self.read(self.next_value(), param2_mode)
        target = self.next_value()
        if source_1 < source_2:
            self.write(target, 1, param3_mode)
        else:
            self.write(target, 0, param3_mode)

    def opcode_equals(self, param1_mode, param2_mode, param3_mode) -> None:
        source_1 = self.read(self.next_value(), param1_mode)
        source_2 = self.read(self.next_value(), param2_mode)
        target = self.next_value()
        if source_1 == source_2:
            self.write(target, 1, param3_mode)
        else:
            self.write(target, 0, param3_mode)

    def opcode_set_relative_base(self, param1_mode) -> None:
        adjustment = self.read(self.next_value(), param1_mode)
        self.relative_base += adjustment
