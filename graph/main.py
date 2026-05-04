import json
from collections import defaultdict
from enum import Enum, auto
import itertools
import os
import multiprocessing

class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()

turing_machine_alphabet = frozenset(["1", "B"])
tape_alphabet = turing_machine_alphabet

class State:
    def __init__(self, name="", accept=False):
        self.name = name
        self.accept = accept
        self.transition_function = defaultdict(lambda: (self, "B", Direction.RIGHT))

    def set_character_transition(self, key=None, action=None) -> None:
        if key is None:
            return

        if action is None:
            action = (self, "B", Direction.RIGHT)

        if not isinstance(action, tuple) or len(action) != 3 or not isinstance(action[0], State) or action[1] not in tape_alphabet or not isinstance(action[2], Direction):
            raise ValueError(f"Invalid action passed to state {self.name} for key {key}")
        
        self.transition_function[key] = action

class TuringMachine:
    def __init__(self, states: set, start_state: State = None, name: str = ""):
        self.tape = defaultdict(lambda: "B")
        self.pointer = 0
        self.states = states
        self.start_state = start_state
        self.curr_state = self.start_state
        self.running = False
        self.name = name

    def set_start_state(self, start_state: State = None):
        self.start_state = start_state
        if self.running:
            self.curr_state = self.start_state

    def get_tape_string(self) -> str:
        if not self.tape:
            return "B"
        min_idx = min(self.tape.keys())
        max_idx = max(self.tape.keys())
        return "".join(self.tape[i] for i in range(min_idx, max_idx + 1))

    def run(self, arg: str = None, step: int = None) -> bool:
        if self.start_state is None:
            raise ValueError("Start state is None.")

        if self.start_state not in self.states:
            raise ValueError("Start state is not in the set of machine states.")

        self.tape.clear()
        self.pointer = 0
        self.curr_state = self.start_state
        self.running = True

        if arg:
            for i, char in enumerate(arg):
                self.tape[i] = char

        count = 0
        while not step or (step and count < step):
            if self.curr_state.accept:
                self.running = False
                return True

            current_char = self.tape[self.pointer]
            next_state, write_char, direction = self.curr_state.transition_function[current_char]

            if next_state not in self.states:
                raise ValueError(f"Machine attempted to move to unknown state: {next_state.name}")

            self.tape[self.pointer] = write_char
            
            if direction == Direction.LEFT:
                self.pointer -= 1
            elif direction == Direction.RIGHT:
                self.pointer += 1

            self.curr_state = next_state
            count += 1
            
        self.running = False
        return self.curr_state.accept


def load_turing_machines_from_json(json_str: str) -> dict[str, TuringMachine]:
    data = json.loads(json_str)
    machines = {}
    
    for machine_data in data:
        machine_name = machine_data.get("name", "Unnamed_Machine")
        
        states_dict = {}
        for state_data in machine_data["states"]:
            new_state = State(name=state_data["name"], accept=state_data.get("accept", False))
            states_dict[new_state.name] = new_state
        
        for trans in machine_data["transitions"]:
            curr_state = states_dict[trans["state"]]
            next_state = states_dict[trans["next_state"]]
            
            direction = Direction.RIGHT if trans["direction"].upper() == "RIGHT" else Direction.LEFT
            action = (next_state, trans["write"], direction)
            
            curr_state.set_character_transition(key=trans["read"], action=action)
            
        start_state = states_dict[machine_data["start_state"]]
        machines[machine_name] = TuringMachine(
            states=set(states_dict.values()), 
            start_state=start_state,
            name=machine_name
        )
        
    return machines

def load_turing_machines_from_file(file_path: str) -> dict[str, TuringMachine]:
    json_string = None
    with open(file_path, 'r') as file:
        json_string = file.read()
    
    if json_string == None:
    	return None

    return load_turing_machines_from_json(json_string)

def decode_string_to_machine(encoded_str: str, name: str = "Decoded_TM") -> TuringMachine:
    alphabet = ["1", "B"]
    transitions = encoded_str.split("_")
    num_working_states = len(transitions) // len(alphabet)
    
    states_dict = {}
    for i in range(num_working_states):
        state_name = f"q{i}"
        states_dict[state_name] = State(name=state_name, accept=False)

    states_dict["qa"] = State(name="qa", accept=True) 
    
    for i, trans_code in enumerate(transitions):
        state_index = i // len(alphabet)
        char_index = i % len(alphabet)
        
        curr_state_name = f"q{state_index}"
        read_char = alphabet[char_index]
        
        next_state_char = trans_code[0]
        write_char = trans_code[1]
        dir_char = trans_code[2]
        
        next_state_name = "qa" if next_state_char == "H" else f"q{next_state_char}"
        direction = Direction.RIGHT if dir_char == "R" else Direction.LEFT
        
        curr_state_obj = states_dict[curr_state_name]
        next_state_obj = states_dict[next_state_name]
        
        curr_state_obj.set_character_transition(
            key=read_char, 
            action=(next_state_obj, write_char, direction)
        )
        
    return TuringMachine(
        states=set(states_dict.values()),
        start_state=states_dict["q0"],
        name=name
    )


BB_BOUNDS = {
    1: 1,
    2: 6,
    3: 21,
    4: 107,
    5: 47176870
}

def evaluate_machine_worker(args):
    dna_tuple, n, step_limit = args
    
    working_states = [f"q{i}" for i in range(n)]
    all_states = working_states + ["qa"]
    alphabet = ["1", "B"]
    ordered_questions = list(itertools.product(working_states, alphabet))
    
    states_dict = {name: State(name=name, accept=(name=="qa")) for name in all_states}
    rulebook = dict(zip(ordered_questions, dna_tuple))
    
    for condition, action in rulebook.items():
        curr_state_name, read_char = condition
        next_state_name, write_char, direction = action
        states_dict[curr_state_name].set_character_transition(
            key=read_char, action=(states_dict[next_state_name], write_char, direction)
        )
        
    machine = TuringMachine(states=set(states_dict.values()), start_state=states_dict["q0"])
    
    did_halt = machine.run(arg="", step=step_limit)
    
    if did_halt:
        encoded_rules = []
        for action in dna_tuple:
            next_state_str = "H" if action[0] == "qa" else action[0].replace("q", "")
            write_char = action[1]
            dir_str = "R" if action[2] == Direction.RIGHT else "L"
            encoded_rules.append(f"{next_state_str}{write_char}{dir_str}")
            
        machine_dna_string = "_".join(encoded_rules)
        tape_output = machine.get_tape_string()
        return f"{machine_dna_string},{tape_output}"
        
    return None

def generate_tasks(n: int, step_limit: int, start_index: int = 0):
    working_states = [f"q{i}" for i in range(n)]
    all_states = working_states + ["qa"]
    alphabet = ["1", "B"] 
    directions = [Direction.LEFT, Direction.RIGHT]

    ordered_questions = list(itertools.product(working_states, alphabet))
    possible_answers = list(itertools.product(all_states, alphabet, directions))
    
    gen = itertools.product(possible_answers, repeat=len(ordered_questions))

    if start_index > 0:
        print(f"Fast-forwarding generator by {start_index} machines to resume... (This is C-level fast!)")
        next(itertools.islice(gen, start_index, start_index), None)
    
    for dna_tuple in gen:
        yield (dna_tuple, n, step_limit)

def create_all_turing_machines_n(n: int, folder_base_name: str = "halting_machines"):
    step_limit = BB_BOUNDS.get(n, 47176870)
    cores = os.cpu_count()
    
    target_folder = f"bb{n}_{folder_base_name}"
    os.makedirs(target_folder, exist_ok=True)
    
    checkpoint_file = os.path.join(target_folder, "checkpoint.json")
    
    total_tested = 0
    halting_count = 0
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            data = json.load(f)
            total_tested = data.get("total_tested", 0)
            halting_count = data.get("halting_count", 0)
            print(f"--- RESUMING FROM CHECKPOINT ---")
            print(f"Already tested: {total_tested} | Already found: {halting_count}\n")
    else:
        print(f"Starting fresh generation for n={n} working states.")
    
    task_generator = generate_tasks(n, step_limit, start_index=total_tested)
    
    file_limit = 100000
    current_file_idx = (halting_count // file_limit) + 1
    current_file_count = halting_count % file_limit
    current_file = None

    batch_size = 100000

    with multiprocessing.Pool(processes=cores) as pool:
        while True:
            batch = list(itertools.islice(task_generator, batch_size))
            
            if not batch:
                break
                
            for result in pool.imap_unordered(evaluate_machine_worker, batch, chunksize=1000):
                if result is not None:
                    if current_file is None:
                        file_path = os.path.join(target_folder, f"bb{n}_halting_machines_{current_file_idx}.txt")
                        current_file = open(file_path, 'a')

                    current_file.write(f"{result}\n")
                    current_file_count += 1
                    halting_count += 1
                    
                    if current_file_count >= file_limit:
                        current_file.close()
                        current_file = None
                        current_file_idx += 1
                        current_file_count = 0

            total_tested += len(batch)
            
            with open(checkpoint_file, 'w') as f:
                json.dump({
                    "total_tested": total_tested, 
                    "halting_count": halting_count
                }, f)
                
            print(f"Checkpoint saved: Tested {total_tested} | Found {halting_count} halting machines...")

    if current_file is not None and not current_file.closed:
        current_file.close()

    print(f"\n--- COMPLETION ---")
    print(f"Fully tested all {total_tested} machines.")
    print(f"Saved {halting_count} halting machines across {current_file_idx} files.")

if __name__ == "__main__":
    for i in range(2, 4):
        create_all_turing_machines_n(i)
