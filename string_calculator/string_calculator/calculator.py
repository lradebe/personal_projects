import re


def square_brackets_splitter(square_bracket_delimiter):
    for content in square_bracket_delimiter:
        split_by_square_brackets = re.split("\\[|\\]", content)
    return [delimiter for delimiter in split_by_square_brackets if delimiter != ""]


def sum_of_digits(digits=None):
    summed_numbers = 0
    for number in digits:
        try:
            number = int(number)
        except Exception:
            raise ValueError("ERROR: invalid input")
        if number >= 1000:
            continue
        summed_numbers += number
    return summed_numbers


def add(string):
    split_string = re.split("\n", string[2:])
    negatives = re.findall("-\\d{1,}", string)
    if len(negatives) > 0 and len(re.findall("//-", string)) == 0:
        raise ValueError(f"ERROR: negatives not allowed {', '.join(negatives)}")
    if "\n" in string:
        return with_newline(string, split_string)
    elif len(string) == 0:
        return 0
    elif len(string) == 1:
        return int(string)
    else:
        return sum_of_digits(string.split(","))


def only_newline(string):
    if (
        len(re.findall("\\d{1,}|\\s", string[: string.find("\n")][-1])) == 0
        or len(re.findall("\\d{1,}|\\s", string[-1])) == 0
    ):
        raise ValueError("ERROR: invalid input")
    return sum_of_digits(re.findall("\\d{1,}", repr(string)))


def check_undeclared_delimiters(split_string, string):
    if re.match("//", string) is not None:
        for item in re.findall("[^\\d]{1,}", split_string[1]):
            if item not in split_string[0]:
                raise ValueError("ERROR: invalid input")
    elif split_string[0] not in re.findall("[^\\d]{1,}", split_string[1]):
        raise ValueError("ERROR: invalid input")


def square_bracket_delimiters(split_string):
    delimiters = square_brackets_splitter(re.findall("\\[.+]", split_string[0]))
    if "[]" in split_string[0]:
        raise ValueError("ERROR: invalid input")
    for delimiter in delimiters:
        if delimiter in split_string[1]:
            split_string[1] = split_string[1].replace(delimiter, ",")
    return sum_of_digits(split_string[1].split(","))


def with_newline(string, split_string):
    if "//" not in string and "\n" in string:
        return only_newline(string)
    if len(split_string[1]) == 0:
        return 0

    check_undeclared_delimiters(split_string, string)
    number_identical_to_delimiter_beside_it(string, split_string)
    if re.findall("//\\[.+]", string) != []:
        return square_bracket_delimiters(split_string)
    if "[" in string or "]" in string:
        raise ValueError("ERROR: invalid input")
    split_string[1] = split_string[1].replace(split_string[0], ",")
    return sum_of_digits(split_string[1].split(","))


def check_each_delimiter(delimiter_item, split_string):
    for num in re.findall("\\d{1,}", split_string[1]):
        if delimiter_item in num:
            match = re.search(delimiter_item, num).span()
            before_delimiter = num[: match[0]]
            after_delimiter = num[match[1] :]
            if (
                len(before_delimiter) == 0 or
                before_delimiter[-1] == delimiter_item[0]
                or after_delimiter[0] == delimiter_item[-1]
            ):
                raise ValueError("ERROR: invalid input")
            elif before_delimiter in delimiter_item or after_delimiter in delimiter_item:
                raise ValueError("ERROR: invalid input")



def number_identical_to_delimiter_beside_it(string, split_string):
    if re.match("//", string) is not None:
        delimiter_item = re.findall("\\S{1,}", split_string[0])[0]
        if re.findall("\\[.+]", delimiter_item) != []:
            delimiter_items = square_brackets_splitter(
                re.findall("\\[.+]", delimiter_item)
            )
            for delimiter_item in delimiter_items:
                check_each_delimiter(delimiter_item, split_string)
        check_each_delimiter(delimiter_item, split_string)
