import pytest
from functions import count_words, find_unique, is_palindrome, are_anagrams, combine_dicts

# --- Тесты для задачи 1: Подсчет слов ---
def test_count_words_basic():
    assert count_words("Hello world") == 2

def test_count_words_many():
    assert count_words("Python is fun and powerful") == 5

def test_count_words_empty():
    assert count_words("") == 0

def test_count_words_spaces():
    # Проверка на лишние пробелы
    assert count_words("   Hello   world   ") == 2


# --- Тесты для задачи 2: Уникальные элементы ---
def test_find_unique_numbers():
    assert find_unique([1, 2, 3, 2, 1, 4]) == [3, 4]

def test_find_unique_strings():
    assert find_unique(["apple", "banana", "apple", "cherry"]) == ["banana", "cherry"]

def test_find_unique_all_unique():
    assert find_unique([1, 2, 3]) == [1, 2, 3]

def test_find_unique_none():
    assert find_unique([1, 1, 2, 2]) == []


# --- Тесты для задачи 3: Палиндром ---
def test_is_palindrome_word():
    assert is_palindrome("radar") is True

def test_is_palindrome_mixed_case():
    assert is_palindrome("Anna") is True

def test_is_palindrome_sentence():
    # "А роза упала на лапу Азора" (без пробелов читается одинаково)
    assert is_palindrome("A man a plan a canal Panama") is True

def test_is_palindrome_number():
    assert is_palindrome(12321) is True
    assert is_palindrome(123) is False


# --- Тесты для задачи 4: Анаграммы ---
def test_are_anagrams_basic():
    assert are_anagrams("listen", "silent") is True

def test_are_anagrams_diff_case():
    assert are_anagrams("Race", "Care") is True

def test_are_anagrams_phrase():
    assert are_anagrams("eleven plus two", "twelve plus one") is True

def test_not_anagrams():
    assert are_anagrams("hello", "world") is False


# --- Тесты для задачи 5: Слияние словарей ---
def test_combine_dicts_basic():
    d1 = {"a": 1, "b": 2}
    d2 = {"c": 3}
    expected = {"a": 1, "b": 2, "c": 3}
    assert combine_dicts(d1, d2) == expected

def test_combine_dicts_overlap():
    # Проверка перезаписи значений при совпадении ключей
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 3, "c": 4}
    expected = {"a": 1, "b": 3, "c": 4}
    assert combine_dicts(d1, d2) == expected

def test_combine_dicts_empty():
    d1 = {"a": 1}
    d2 = {}
    assert combine_dicts(d1, d2) == {"a": 1}