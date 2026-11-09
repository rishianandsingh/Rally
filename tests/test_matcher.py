from matcher import Candidate, form_teams, score_pair


def cand(i: int, skills: set[str], slots: set[str]) -> Candidate:
    return Candidate(i, frozenset(skills), frozenset(slots))


def test_score_is_symmetric():
    a = cand(1, {"git", "docker"}, {"weekend_night"})
    b = cand(2, {"sql"}, {"weekend_night", "weekday_night"})
    assert score_pair(a, b) == score_pair(b, a)


def test_disjoint_skills_beat_identical_skills():
    a = cand(1, {"git", "docker"}, {"weekend_night"})
    different = cand(2, {"sql", "backend"}, {"weekend_night"})
    same = cand(3, {"git", "docker"}, {"weekend_night"})
    assert score_pair(a, different) > score_pair(a, same)


def test_more_availability_overlap_scores_higher():
    a = cand(1, {"git"}, {"weekend_am", "weekend_pm"})
    overlapping = cand(2, {"sql"}, {"weekend_am", "weekend_pm"})
    disjoint = cand(3, {"sql"}, {"weekday_eve"})
    assert score_pair(a, overlapping) > score_pair(a, disjoint)


def test_even_split_assigns_everyone_once():
    pool = [cand(i, {f"s{i}"}, {"weekend_am"}) for i in range(1, 7)]
    teams = form_teams(pool, 3)
    assert [len(t) for t in teams] == [3, 3]
    assert sorted(i for t in teams for i in t) == [1, 2, 3, 4, 5, 6]


def test_leftover_goes_to_smaller_final_team():
    pool = [cand(i, {f"s{i}"}, {"weekend_am"}) for i in range(1, 8)]
    teams = form_teams(pool, 3)
    assert [len(t) for t in teams] == [3, 3, 1]
    assert sorted(i for t in teams for i in t) == list(range(1, 8))


def test_team_size_below_two_raises():
    import pytest

    with pytest.raises(ValueError):
        form_teams([cand(1, {"a"}, {"weekend_am"})], 1)