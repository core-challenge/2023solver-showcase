%%% Independent Set Reconfiguration (token jumping)
%%% LCC version
%%%
%%% @author Nagoya university ASP team
%%% @mail yuya.yamada@nagoya-u.jp
%%% @mail banbara@nagoya-u.jp

#program base.

% start configuration
:- not in(X,0), start(X).
:- in(X,0), in(Y,0), edge(X,Y).

#program step(t).

% independent set constraints
K { in(X,t): node(X) } K :- k(K).
:- token_added(X,t), in(Y,t), edge(X,Y), t > 0.
:- token_added(X,t), in(Y,t), edge(Y,X), t > 0.

% transition constraints (at-most-one)
token_added(X,t) :- not in(X,t-1), in(X,t), t > 0.
:- not 1 { token_added(X,t) } 1, t > 0.

#program check(t).

% goal configuration
:- not in(X,t), goal(X), query(t).
