%%% Independent Set Reconfiguration (token jumping)
%%% Multi-shot version
%%%
%%% @author Nagoya university ASP team
%%% @mail yuya.yamada@nagoya-u.jp
%%% @mail banbara@nagoya-u.jp

#program base.

% start configuration
:- not in(X,0), start(X).

#program step(t).

% independent set constraints
K { in(X,t): node(X) } K :- k(K).
:- in(X,t), in(Y,t), edge(X,Y).

% transition constraints (at-most-one)
moved_from(X,t) :- in(X,t-1), not in(X,t), t > 0.
:- not { moved_from(X,t) } 1, t > 0.

#program check(t).

% goal configuration
:- not in(X,t), goal(X), query(t).
