%%% Numeric Abstraction: solving
%%% Time-stamp: <2023-04-07 16:04:48 banbara>

% generate abstract state
{ snode((W,X,Y,Z)) :
  K = W+X+Y+Z,
  W = 0..N1, num_of_cnodes(1,N1),
  X = 0..N2, num_of_cnodes(2,N2),
  Y = 0..N3, num_of_cnodes(3,N3),
  Z = 0..N4, num_of_cnodes(4,N4)
} :- k(K).

% check if each state can have an independent set
K { in(V,I): node(V) } K :- k(K), snode(I).
:- in(U,I), in(V,I), edge(U,V).
:- not W { in(V,I) : cnode(V,1) } W, I = (W,_,_,_), snode(I).
:- not X { in(V,I) : cnode(V,2) } X, I = (_,X,_,_), snode(I).
:- not Y { in(V,I) : cnode(V,3) } Y, I = (_,_,Y,_), snode(I).
:- not Z { in(V,I) : cnode(V,4) } Z, I = (_,_,_,Z), snode(I).

% generate edges between stats.
sedge(I,J) :- I = (W,X,Y,Z), J = (W+1,X-1,  Y,  Z), snode(I), snode(J), I<J.
sedge(I,J) :- I = (W,X,Y,Z), J = (W+1,  X,Y-1,  Z), snode(I), snode(J), I<J.
sedge(I,J) :- I = (W,X,Y,Z), J = (W+1,  X,  Y,Z-1), snode(I), snode(J), I<J.

sedge(I,J) :- I = (W,X,Y,Z), J = (W-1,X+1,  Y,  Z), snode(I), snode(J), I<J.
sedge(I,J) :- I = (W,X,Y,Z), J = (  W,X+1,Y-1,  Z), snode(I), snode(J), I<J.
sedge(I,J) :- I = (W,X,Y,Z), J = (  W,X+1,  Y,Z-1), snode(I), snode(J), I<J.

sedge(I,J) :- I = (W,X,Y,Z), J = (W-1,  X,Y+1,  Z), snode(I), snode(J), I<J.
sedge(I,J) :- I = (W,X,Y,Z), J = (  W,X-1,Y+1,  Z), snode(I), snode(J), I<J.
sedge(I,J) :- I = (W,X,Y,Z), J = (  W,  X,Y+1,Z-1), snode(I), snode(J), I<J.

sedge(I,J) :- I = (W,X,Y,Z), J = (W-1,  X,  Y,Z+1), snode(I), snode(J), I<J.
sedge(I,J) :- I = (W,X,Y,Z), J = (  W,X-1,  Y,Z+1), snode(I), snode(J), I<J.
sedge(I,J) :- I = (W,X,Y,Z), J = (  W,  X,Y-1,Z+1), snode(I), snode(J), I<J.

% check the reachability
reached(S) :- start_snode(S).
reached(I) :- reached(J), sedge(I,J).
reached(I) :- reached(J), sedge(J,I).
:- not reached(G), goal_snode(G).


