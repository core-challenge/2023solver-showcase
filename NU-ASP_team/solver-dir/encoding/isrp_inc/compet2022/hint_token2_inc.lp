%%% Hint: Token jumping
%%% Multi-shot version
%%%
%%% @author Nagoya university ASP team
%%% @mail yuya.yamada@nagoya-u.jp
%%% @mail banbara@nagoya-u.jp

#program step(t).

% No double jumping
moved_to(X,t) :- not in(X,t-1), in(X,t), t > 0.
:- moved_to(X,t-1), not in(X,t), t > 1.
