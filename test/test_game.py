import pytest

from spatle import game


@pytest.mark.parametrize('guess, expected', [
    ('abcd', [True, True, True, True]),
    ('abc_', [True, True, True, None]),
    ('ab__', [True, True, None, None]),
    ('abdc', [True, True, False, False]),
    ('a_dc', [True, None, False, False]),

])
def test_word_compare(guess, expected):
    word = game.Word('abcd')
    assert word.compare(guess) == expected


def test_game():
    this = game.Game('eeeee')
    assert this.solved is False
    assert this.guesses_remaining == 5
    assert this.solution == 'eeeee'
    for word in ['aaaaa', 'bbbbb', 'ccccc', 'edede']:
        assert this.guess(word) is False

    assert this.guesses_remaining == 1
    assert this._state == ['e', '', 'e', '', 'e']

    assert this.letter_state('a') is False
    assert this.letter_state('e') is True
    assert this.letter_state('z') is None

    assert this.guess('eeeee')
    assert this.solved
    assert this._state == ['e', 'e', 'e', 'e', 'e']
    assert this.guesses_remaining == 0

    # out of guesses
    assert this.guess('eeeee') is False
