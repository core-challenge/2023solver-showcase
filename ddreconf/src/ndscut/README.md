# ndscut

A heuristic algorithm for ordering edges of a graph.

The algorithm is based on graph cuts. If the input graph is small, it uses NDS.

## Requirement

It requires [networkx](https://networkx.org/) library.
To install networkx, run the following command:

```
pip3 install networkx
```

## Usage

```
python3 ndscut.py < edge_list.txt
```

It outputs to the standard output.

## Format

The format of the input graph file is a so-called edge list.
One line corresponds to an edge and consists of two integers
representing the vertex numbers of the endpoints.
In the following example, there are four vertices 1, 2, 3 and 4,
and four edges connecting 1 with 2, 1 with 3, 2 with 3 and 2 with 4.

Example:

```
1 2
1 3
2 3
2 4
```

The program can read/write the input in the DIMACS format if you run it with '-d' option.
