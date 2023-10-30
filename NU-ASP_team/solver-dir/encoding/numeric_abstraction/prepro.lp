%%% Numeric Abstraction: prepossessing
%%% Time-stamp: <2023-04-04 12:15:48 banbara>

% colors
color(1..4).

cnode(V,1) :- node(V), start(V), goal(V).
cnode(V,2) :- node(V), start(V), not goal(V).
cnode(V,3) :- node(V), not start(V), goal(V).
cnode(V,4) :- node(V), not start(V), not goal(V).

num_of_cnodes(C,N) :- N = { cnode(V, C) }, color(C).

% start/goal states
start_snode((W,X,Y,Z)) :-
		W = #sum { 1,V : start(V),cnode(V,1) },
		X = #sum { 1,V : start(V),cnode(V,2) },
		Y = #sum { 1,V : start(V),cnode(V,3) },
		Z = #sum { 1,V : start(V),cnode(V,4) }.
goal_snode((W,X,Y,Z)) :-
		W = #sum { 1,V : goal(V),cnode(V,1) },
		X = #sum { 1,V : goal(V),cnode(V,2) },
		Y = #sum { 1,V : goal(V),cnode(V,3) },
		Z = #sum { 1,V : goal(V),cnode(V,4) }.
