%%% Hint: Token jumping
%%% Multi-shot version
%%%
%%% @author Nagoya university ASP team
%%% @mail yuya.yamada@nagoya-u.jp
%%% @mail banbara@nagoya-u.jp

#program step(t).

% No one back
:- moved_from(X,t-1), in(X,t), t > 1.
