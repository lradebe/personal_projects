import pytest
from string_calculator.calculator import add


def test_empty_string():
    assert add("") == 0


one_integer = [("2", 2), ("11", 11), ("333", 333), ("999", 999), ("1050", 0)]


@pytest.mark.parametrize("one_integer, expected", one_integer)
def test_one_integer(one_integer, expected):
    assert add(one_integer) == expected


multiple_integers = [
    ("2,4", 2 + 4),
    ("1,1, 1500", 1 + 1 + 0),
    ("1,2,3,4", 1 + 2 + 3 + 4),
    ("12,14", 12 + 14),
    ("211,532,333", 211 + 532 + 333),
]


@pytest.mark.parametrize("multiple_integers, expected", multiple_integers)
def test_multiple_integers(multiple_integers, expected):
    assert add(multiple_integers) == expected


with_only_newline = [
    ("5,1\n2,5", 5 + 1 + 2 + 5),
    ("12,34\n53", 12 + 34 + 53),
    ("431\n111,2,998", 431 + 111 + 2 + 998),
    ("1\n2,3", 1 + 2 + 3),
]


@pytest.mark.parametrize("with_only_newline, expected", with_only_newline)
def test_with_only_newline(with_only_newline, expected):
    assert add(with_only_newline) == expected


single_delimiters = [
    ("//;\n1;2", 1 + 2),
    ("//;\n1000;1;2", 0 + 1 + 2),
    ("//***\n1***2***3", 1 + 2 + 3),
    ("//4\n142", 1 + 2),
    ("//-\n1-2", 1 + 2),
    ("//#\n6#3#7", 6 + 3 + 7),
    ("//4\n247147", 2 + 71 + 7),
    ("//[77]\n1772774", 1 + 2 + 4),
    ("//44\n24471447", 2 + 71 + 7),
    ("//[**]\n1**2**4", 1 + 2 + 4),
    ("//[ii]\n1ii2ii4", 1 + 2 + 4),
    ("//[,]\n1,2,5,7", 1 + 2 + 5 + 7),
    ("//88\n18820882", 1 + 20 + 2),
]


@pytest.mark.parametrize("single_delimiters, expected", single_delimiters)
def test_single_delimiters(single_delimiters, expected):
    assert add(single_delimiters) == expected


multiple_delimiters = [
    ("//[33][,]\n5,2332,8,2337", 5 + 2 + 2 + 8 + 2 + 7),
    ("//[:D][%]\n1:D2%3", 1 + 2 + 3),
    ("//[***][%%%]\n1***2%%%3", 1 + 2 + 3),
    ("//[(-_-')][%]\n1(-_-')2%3", 1 + 2 + 3),
    ("//[\\*][%]\n1\\*2%3", 1 + 2 + 3),
    ("//[11][**]\n3114**5", 3 + 4 + 5),
    ("//[***][%%%]\n11***22%%%33***54", 11 + 22 + 33 + 54),
    ("//[(-_-')][%]\n111(-_-')222%1000(-_-')22", 111 + 222 + 22),
    ("//[33][bb]\n243372bb493312338", 24 + 72 + 49 + 12 + 8),
    ("//[))][(((]\n5(((10))20(((33))7", 5 + 10 + 20 + 33 + 7),
    ("//[abc][777][:(]\n1abc27773:(1", 1 + 2 + 3 + 1),
    ("//[abc][tt][44]\n31abc2tt67449", 31 + 2 + 67 + 9),
]


@pytest.mark.parametrize(
    "multiple_delimiters, expected", multiple_delimiters,
)
def test_multiple_delimiters(multiple_delimiters, expected):
    assert add(multiple_delimiters) == expected


negative_values = [
    ("-1, -2,3,4", ValueError),
    ("50, 35\n-10", ValueError),
    ("//;\n5;10;-5", ValueError),
]


@pytest.mark.parametrize("negative_values, expected", negative_values)
def test_negative_values(negative_values, expected):
    with pytest.raises(ValueError):
        add(negative_values)


invalid_input = [
    ("//;\n1000;1;2;", ValueError),
    ("   //;\n1000,1;2", ValueError),
    ("1,2,3//;\n1000,1;2", ValueError),
    ("//]\n90]11]20", ValueError),
    ("//[[][[][&&]\n1[2[3&&4", ValueError),
    ("//44\n1444", ValueError),
    ("//[\n1[2", ValueError),
    ("//88\n18882", ValueError),
    ("//[**]\n1*4**4", ValueError),
    ("//[:D][%]\n1:D:D2%3", ValueError),
    ("//[44][][bb]\n334466215bb9844332157bc22", ValueError),
    ("//[**]\n1;4**4", ValueError),
    ("//[}\n1,2,3", ValueError),
    ("//[**][%%]\n1**2%%3%4", ValueError),
    ("//[**]\n1*4**5", ValueError),
    ("1,2,\n3", ValueError),
    ("1,2\n3,", ValueError),
    ("//[222][**][###]\n12222**1###1", ValueError),
    ("//[222][**][###]\n122222**1###1", ValueError),
    ("//441\n14412", ValueError),
    ("//4\n434343", ValueError)
]


@pytest.mark.parametrize("invalid_input, expected", invalid_input)
def test_invalid_input(invalid_input, expected):
    with pytest.raises(ValueError):
        add(invalid_input)
