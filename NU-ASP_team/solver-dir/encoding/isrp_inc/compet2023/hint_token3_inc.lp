%%% Hint: Fobidden token addition
%%%
%%% @author Nagoya university ASP team
%%% @mail banbara@nagoya-u.jp

#program step(t).

:- token_added(X,t), 2 { in(Y,t-1): edge(X,Y) ; in(Y,t-1): edge(Y,X) }, t > 0.
