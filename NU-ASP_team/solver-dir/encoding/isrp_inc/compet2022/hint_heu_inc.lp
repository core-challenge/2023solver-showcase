%%% Hint: Maximal IS
%%% Multi-shot version
%%%
%%% @author Nagoya university ASP team
%%% @mail yuya.yamada@nagoya-u.jp
%%% @mail banbara@nagoya-u.jp

#program step(t).
#const level_max = 1000.

#heuristic in(Y,t): edge(X,Y), not in(X,t). [level_max-t,true]
#heuristic in(Y,t): edge(Y,X), not in(X,t). [level_max-t,true]
% #heuristic in(Y,T): edge(X,Y), not in(X,T), t(T). [1,sign]
% #heuristic in(Y,T): edge(Y,X), not in(X,T), t(T). [1,sign]

