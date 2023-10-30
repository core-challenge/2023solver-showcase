from pathlib import Path

def read_graph_DIMACS(input_file: Path | str) -> tuple[int, list[tuple[int, int]]]:
    if isinstance(input_file, str):
        input_file = Path(input_file)
    
    V = 0
    E = []
    
    for line in input_file.open(mode='r'):
        line = line.strip()
        if line.startswith('c'):
            continue
        if line.startswith('p'):
            V, _ = map(int, line[1:].split())
        if line.startswith('e'):
            u, v = map(int, line[1:].split())
            E.append((u, v))

    return V, E

def read_ISR_DIMACS(input_file: Path | str) -> tuple[list[int], list[int]]:
    if isinstance(input_file, str):
        input_file = Path(input_file)
    
    source = []
    target = []
    for line in input_file.open(mode='r'):
        line = line.strip()
        if line.startswith('c'):
            continue
        if line.startswith('s'):
            source = list(map(int, line[1:].split()))
        if line.startswith('t'):
            target = list(map(int, line[1:].split()))
    
    return source, target

