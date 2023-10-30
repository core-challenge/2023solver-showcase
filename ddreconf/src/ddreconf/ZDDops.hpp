#pragma once

#include "./ZBDD.h"
#include "./sbdd_helper/SBDD_helper.h"

namespace zdd_ops {
    namespace op_id {
        static constexpr unsigned char Rem = 128;
        static constexpr unsigned char Delta = 129;

        template <size_t k, std::enable_if_t<k <= 10, std::nullptr_t> = nullptr>
        static constexpr unsigned char Add = 130 + (k - 1); // 130, ..., 139

        template <size_t k, std::enable_if_t<k <= 10, std::nullptr_t> = nullptr>
        static constexpr unsigned char Dist = 140 + (k - 1); // 140, ..., 149

        template <size_t k, std::enable_if_t<k <= 10, std::nullptr_t> = nullptr>
        static constexpr unsigned char Restrict = 150 + (k - 1); // 150, ..., 159

        template <size_t k, std::enable_if_t<k <= 10, std::nullptr_t> = nullptr>
        static constexpr unsigned char IntersecSymK = 160 + (k - 1); // 160, ..., 169

        template <size_t k, std::enable_if_t<k <= 10, std::nullptr_t> = nullptr>
        static constexpr unsigned char HasIntersecSymK = 170 + (k - 1); // 170, ..., 179
    }

    template <
        unsigned char op_id_, typename Ret = ZBDD,
        std::enable_if_t<std::disjunction_v<std::is_same<Ret, ZBDD>, std::is_same<Ret, BDD>, std::is_same<Ret, bddword>>, std::nullptr_t> = nullptr
    >
    struct Cacher {
        static constexpr unsigned char op_id = op_id_;

        template <typename T, typename U = bddword>
        static Cacher search(const T& f, const U& g = 0) {
            bddword fp = to_bddword(f), gp = to_bddword(g);
            if constexpr (std::is_same_v<Ret, ZBDD>) {
                return Cacher{ fp, gp, BDD_CacheZBDD(op_id, fp, gp) };
            } else if constexpr (std::is_same_v<Ret, BDD>) {
                return Cacher{ fp, gp, BDD_CacheBDD(op_id, fp, gp) };
            } else {
                return Cacher{ fp, gp, BDD_CacheInt(op_id, fp, gp) };
            }
        }
        template <typename F, std::enable_if_t<std::is_invocable_r_v<Ret, F>, std::nullptr_t> = nullptr>
        Ret or_eval_cache(F func) {
            if (_result == ZBDD(-1)) {
                if constexpr (std::is_same_v<Ret, ZBDD> or std::is_same_v<Ret, BDD>) {
                    BDD_CacheEnt(op_id, _fp, _gp, (_result = func()).GetID());
                } else {
                    BDD_CacheEnt(op_id, _fp, _gp, (_result = func()));
                }
            }
            return _result;
        }
        operator bool() const {
            if constexpr (std::is_same_v<Ret, ZBDD>) {
                return _result == ZBDD(-1);
            } else if constexpr (std::is_same_v<Ret, BDD>) {
                return _result == BDD(-1);
            } else {
                return _result == BDD(-1).GetID();
            }
        }
    private:
        bddword _fp, _gp;
        Ret _result;
        Cacher(bddword fp, bddword gp, Ret F): _fp(fp), _gp(gp), _result(F) {}

        template <typename T>
        static bddword to_bddword(const T& f) {
            if constexpr (std::is_same_v<T, ZBDD> or std::is_same_v<T, BDD>) {
                return f.GetID();
            } else {
                return f;
            }
        }
    };

    ZBDD make(bddvar top, ZBDD f0, ZBDD f1) {
        return f0 + f1.Change(top);
    }

    template <size_t k>
    ZBDD Add(ZBDD f, ZBDD items) {
        if constexpr (k == 0) {
            return f;
        } else {
            if (sbddh::isTerminal(items)) return ZBDD(0);
            if (f == ZBDD(0)) return ZBDD(0);
            auto impl = [&] {
                bddvar top = BDD_LevOfVar(f.Top()) > BDD_LevOfVar(items.Top()) ? f.Top() : items.Top();

                ZBDD f0 = f.OffSet(top), f1 = f.OnSet0(top);
                if (top == items.Top()) {
                    items = sbddh::getChild0(items);
                    return make(top, Add<k>(f0, items), Add<k - 1>(f0, items) + Add<k>(f1, items));
                } else {
                    return make(top, Add<k>(f0, items), Add<k>(f1, items));
                }
            };
            return Cacher<op_id::Add<k>>::search(f, items).or_eval_cache(impl);
        }
    }

    template <size_t k>
    ZBDD Rem(ZBDD f) {
        if constexpr (k == 0) {
            return f;
        } else {
            if (sbddh::isTerminal(f)) return ZBDD(0);
            auto impl = [&] {
                ZBDD f0 = sbddh::getChild0(f);
                ZBDD f1 = sbddh::getChild1(f);

                ZBDD g0 = Rem<k>(f0) + Rem<k - 1>(f1);
                ZBDD g1 = Rem<k>(f1);

                return make(f.Top(), g0, g1);
            };
            return Cacher<op_id::Rem>::search(f, k).or_eval_cache(impl);
        }
    }

    ZBDD Delta(ZBDD f, ZBDD g) {
        if (sbddh::isTerminal(f)) return f == ZBDD(1) ? g : ZBDD(0);
        if (sbddh::isTerminal(g)) return g == ZBDD(1) ? f : ZBDD(0);
        if (f.GetID() > g.GetID()) std::swap(f, g);
        auto impl = [&] {
            bddvar top = BDD_LevOfVar(f.Top()) > BDD_LevOfVar(g.Top()) ? f.Top() : g.Top();

            ZBDD f0 = f.OffSet(top), f1 = f.OnSet0(top);
            ZBDD g0 = g.OffSet(top), g1 = g.OnSet0(top);

            ZBDD h0 = Delta(f0, g0) + Delta(f1, g1);
            ZBDD h1 = Delta(f0, g1) + Delta(f1, g0);

            return make(top, h0, h1);
        };
        return Cacher<op_id::Delta>::search(f, g).or_eval_cache(impl);
    }

    template <size_t k>
    ZBDD IntersecSymK(ZBDD f) {
        if constexpr (k == 0) {
            return f & ZBDD(1);
        } else {
            if (sbddh::isTerminal(f)) return ZBDD(0);
            auto impl = [&] {
                bddvar top = BDD_LevOfVar(f.Top());
                ZBDD f0 = f.OffSet(top), f1 = f.OnSet0(top);
                return make(top, IntersecSymK<k>(f0), IntersecSymK<k - 1>(f1));
            };
            return Cacher<op_id::IntersecSymK<k>>::search(f).or_eval_cache(impl);
        }
    }

    template <size_t k>
    bool HasIntersecSymK(ZBDD f) {
        if constexpr (k == 0) {
            return (f & ZBDD(1)) == ZBDD(1);
        } else {
            if (sbddh::isTerminal(f)) return false;
            auto impl = [&] {
                bddvar top = BDD_LevOfVar(f.Top());
                ZBDD f0 = f.OffSet(top), f1 = f.OnSet0(top);
                return bddword(HasIntersecSymK<k>(f0) or HasIntersecSymK<k - 1>(f1));
            };
            return Cacher<op_id::HasIntersecSymK<k>, bddword>::search(f).or_eval_cache(impl);
        }
    }

    template <size_t k>
    ZBDD Restrict(ZBDD f, ZBDD g) {
        if constexpr (k == 0) {
            return f & g;
        } else {
            if (sbddh::isTerminal(f)) return ZBDD(0);
            if (g == ZBDD(0)) return ZBDD(0);
            if (g == ZBDD(1)) return IntersecSymK<k>(f);
            auto impl = [&] {
                bddvar top = BDD_LevOfVar(f.Top()) > BDD_LevOfVar(g.Top()) ? f.Top() : g.Top();

                ZBDD f0 = f.OffSet(top), f1 = f.OnSet0(top);
                ZBDD g0 = g.OffSet(top), g1 = g.OnSet0(top);

                ZBDD h0 = Restrict<k>(f0, g0);
                ZBDD h1 = Restrict<k>(f1, g1) + Restrict<k - 1>(f1, g0);
                return make(top, h0, h1);
            };
            return Cacher<op_id::Restrict<k>>::search(f, g).or_eval_cache(impl);
        }
    }

    template <size_t k>
    ZBDD Dist(ZBDD f, ZBDD g) {
        if constexpr (k == 0) {
            return f & g;
        } else {
            if (g == ZBDD(0)) return ZBDD(0);
            if (g == ZBDD(1)) return IntersecSymK<k>(f);
            if (f == ZBDD(0)) return ZBDD(0);
            if (f == ZBDD(1)) return ZBDD(HasIntersecSymK<k>(g));

            auto impl = [&] {
                bddvar top = BDD_LevOfVar(f.Top()) > BDD_LevOfVar(g.Top()) ? f.Top() : g.Top();

                ZBDD f0 = f.OffSet(top), f1 = f.OnSet0(top);
                ZBDD g0 = g.OffSet(top), g1 = g.OnSet0(top);

                ZBDD h0 = Dist<k>(f0, g0) + Dist<k - 1>(f0, g1);
                ZBDD h1 = Dist<k>(f1, g1) + Dist<k - 1>(f1, g0);
                return make(top, h0, h1);
            };
            return Cacher<op_id::Dist<k>>::search(f, g).or_eval_cache(impl);
        }
    }
}