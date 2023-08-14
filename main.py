from intcode import IntCodeComputer
import logging
import itertools


def run_until_halted(phase_a, phase_b, phase_c, phase_d, phase_e):
    with open("input_7.txt") as program_code:
        code = program_code.readline()

        amp_A = IntCodeComputer(0)
        amp_A.load_program(code)
        amp_A.output_stop_mode = True
        amp_B = IntCodeComputer(1)
        amp_B.load_program(code)
        amp_B.output_stop_mode = True
        amp_C = IntCodeComputer(2)
        amp_C.load_program(code)
        amp_C.output_stop_mode = True
        amp_D = IntCodeComputer(3)
        amp_D.load_program(code)
        amp_D.output_stop_mode = True
        amp_E = IntCodeComputer(4)
        amp_E.load_program(code)
        amp_E.output_stop_mode = True

    done = False
    cycle = 1
    feedback = 0
    while not done:
        amp_A.input_queue.put(phase_a)
        amp_A.input_queue.put(feedback)
        amp_A.run()
        if amp_A.program_finished:
            done = True

        amp_B.input_queue.put(phase_b)
        amp_B.input_queue.put(amp_A.output_value)
        amp_B.run()
        if amp_B.program_finished:
            done = True

        amp_C.input_queue.put(phase_c)
        amp_C.input_queue.put(amp_B.output_value)
        amp_C.run()
        if amp_C.program_finished:
            done = True

        amp_D.input_queue.put(phase_d)
        amp_D.input_queue.put(amp_C.output_value)
        amp_D.run()
        if amp_D.program_finished:
            done = True

        amp_E.input_queue.put(phase_e)
        amp_E.input_queue.put(amp_D.output_value)
        amp_E.run()
        if amp_E.program_finished:
            done = True

        feedback = amp_E.output_value

        print(f"Cycle {cycle} finished...")
        cycle += 1
    print(f"Done: {feedback}")
    return feedback


def main():
    phases = [5, 6, 7, 8, 9]

    permutations = itertools.permutations(phases, 5)
    phases_permutations = list(permutations)
    highest_signal = 0
    for permutation in phases_permutations:
        signal = run_until_halted(*permutation)
        if signal > highest_signal:
            highest_signal = signal
    print(highest_signal)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    main()
