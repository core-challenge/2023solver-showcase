%%% Independent Set of size k
%%%
%%% @author Nagoya university ASP team
%%% @mail yuya.yamada@nagoya-u.jp
%%% @mail banbara@nagoya-u.jp

% solution candidates & size constraints
%k { in(X): node(X) } k.
K { in(X): node(X) } K :- k(K).

% independent set constraints
:- in(X), in(Y), edge(X,Y).

#show in/1.
