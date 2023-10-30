import argparse
from pathlib import Path
import subprocess
from sys import stdout
import tempfile
from typing import TextIO
from IO import read_ISR_DIMACS, read_graph_DIMACS

from LoggerConfig import basicConfig
from MeasureTime import measure_time

from Paths import *


def compile():
    subprocess.run(
        ['make'],
        cwd=DD_RECONF_HOME
    )


def reordered_edges(edges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    NDS_CUT = SRC_HOME / 'ndscut/ndscut.py'

    cmd = ['python', NDS_CUT]

    input_text = '\n'.join(f'{u} {v}' for u, v in edges)

    return [
        tuple(map(int, edge_str.split()))
        for edge_str in subprocess.run(
            args=cmd,
            input=input_text,
            stdout=subprocess.PIPE,
            text=True
        ).stdout.strip().split('\n')
    ]


def reorder_vertices_mapping(edges: list[tuple[int, int]]) -> tuple[dict[int, int], dict[int, int]]:
    mapping = dict()
    for a, b in edges:
        if a not in mapping:
            id_a = len(mapping) + 1
            mapping[a] = id_a
        if b not in mapping:
            id_b = len(mapping) + 1
            mapping[b] = id_b

    inverse_mapping = dict()
    for fr, to in mapping.items():
        inverse_mapping[to] = fr
    return mapping, inverse_mapping


def solve(
    col_file: Path,
    dat_file: Path,
    *,
    out: Path | TextIO=stdout,
    reorder_edges: bool,
    reorder_vertices: bool
):
    V, edges = read_graph_DIMACS(col_file)
    source, target = read_ISR_DIMACS(dat_file)

    inv_mapping = { i: i for i in range(1, V + 1) }

    if reorder_edges:
        edges = measure_time(lambda: reordered_edges(edges), "reorder")
        if reorder_vertices:
            mapping, inv_mapping = reorder_vertices_mapping(edges)
            edges = [
                (mapping[u], mapping[v])
                for u, v in edges
            ]
            source = [mapping[u] for u in source]
            target = [mapping[u] for u in target]
    
    with tempfile.NamedTemporaryFile(mode='w+') as col, tempfile.NamedTemporaryFile(mode='w+') as dat:
        col.writelines(
            [f'p {V} {len(edges)}\n'] +
            [f'e {u} {v}\n' for u, v in edges]
        )
        dat.writelines([
            f's {" ".join(map(str, source))}\n',
            f't {" ".join(map(str, target))}\n',
        ])
        col.seek(0)
        dat.seek(0)

        cmd = [
            DD_RECONF_BIN,
            col.name,
            '--indset',
            '--st',
            f'--stfile={dat.name}',
            '-q',
        ]

        output_str = measure_time(lambda: subprocess.run(
            args=cmd,
            stdin=open(col.name, mode='r'),
            stdout=subprocess.PIPE,
            text=True,
        ).stdout.strip().split('\n'), "reconf")

        output_str = [
            f's {" ".join(map(str, source))}',
            f't {" ".join(map(str, target))}',
        ] + output_str

        if reorder_edges and reorder_vertices:
            def is_YesNo(s: str):
                return s.casefold() == 'Yes'.casefold() or s.casefold() == 'No'.casefold()

            output_str_original = []
            for line in output_str:
                if line.startswith('s') or line.startswith('t') or (line.startswith('a') and not is_YesNo(line[1:].strip())):
                    mapped = list(map(int, line[1:].split()))
                    original = sorted(map(inv_mapping.get, mapped)) # type: ignore
                    output_str_original.append(f'{line[0]} {" ".join(map(str, original))}')
                    # output_str_original.append(f'c {" ".join(map(str, mapped))}')
                else:
                    output_str_original.append(line)
            output_str = output_str_original
        
        if isinstance(out, Path):
            print(out)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.touch()
            with out.open(mode='w+') as out_file:
                for line in output_str:
                    out_file.write(line)
                    out_file.write('\n')
        else:
            for line in output_str:
                out.write(line)
                out.write('\n')


if __name__ == '__main__':
    basicConfig()

    parser = argparse.ArgumentParser()
    parser.add_argument('col', type=str)
    parser.add_argument('dat', type=str)
    parser.add_argument('-o', '--out', type=str)
    parser.add_argument('--reorder-edges', action='store_true')
    parser.add_argument('--reorder-vertices', action='store_true')
    parser.add_argument('--nocompile', action='store_true')

    args = parser.parse_args()

    col = Path(args.col)
    dat = Path(args.dat)
    out = args.out
    reorder_edges = args.reorder_edges
    reorder_vertices = args.reorder_vertices

    nocompile = args.nocompile

    if not col.is_absolute():
        col = TEST_HOME / col.with_suffix('.col')

    if not dat.is_absolute():
        dat = TEST_HOME / dat.with_suffix('.dat')

    out = stdout if out is None else Path(out)

    if not nocompile:
        compile()

    solve(
        col_file=col,
        dat_file=dat,
        out=out,
        reorder_edges=reorder_edges,
        reorder_vertices=reorder_vertices
    )
