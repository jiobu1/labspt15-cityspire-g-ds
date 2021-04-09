import unittest

def parse_grades(grades_string):
    GRADES = ['PK', 'K', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'Ungraded']

    # Remove & for grades list
    grades_string = grades_string.replace(' &', ',')

    # Grades list - will add to separated grade string to grades
    grades = []

    # split strings based on ','
    string_list = grades_string.split(',')

    # look for sections of list with '-'
    dash = "-"
    for i in range(len(string_list)):
        clean_string = string_list[i].strip()
        if dash in clean_string:
            #  split using '-', loop and add to grades variable
            start_grade, end_grade = clean_string.split(dash)
            grades += GRADES[GRADES.index(start_grade) : GRADES.index(end_grade)+ 1]
        else:
            # add string to grades
            grades.append(clean_string)

    return grades

unique_grades_combination = ['9-12', '6-8', 'K-4', '5-8', '4-5', 'K-5', '4-6', '7-12', 'K-6',
       '4-8', 'K-8', '1-6', 'PK-3', '6-12', 'K-3', 'PK-K', 'PK', 'PK-8',
       'PK-6', '4-12', 'PK-6 & Ungraded', '1-8', 'K', 'PK-5', 'PK-12',
       '7-11', '3-6', 'K-12', '3-8', '2-10', 'K-1, 5-8', 'PK-4',
       'Ungraded', '1-12', '2-5', '3-5', '10-12', 'PK-1 & Ungraded',
       'K-11', 'K-2', 'K-1', '9-10', 'K-7', '1-5', 'PK-1', 'PK-K, 2',
       'PK-2', '7-8', 'PK-11', '9', 'K-9', '2-11', '2-12', '2-9', '8-12',
       'K-10', 'PK & Ungraded', '7-9', '6', '5-6', '2, 5-6, 8-9, 11-12',
       '11-12', '3-12', 'K-1, 3-4, 6-7, 9, 11', '1-11', '5-12', '6-10',
       '11', '3-7', '7-10', 'PK-10', 'PK-12 & Ungraded', 'PK-9', '6-9',
       '4-9', '9-11', '6-7', '5-12 & Ungraded', '8-11', '2-8',
       '3, 5, 7-11', 'PK, 8', 'PK-7', '6, 9-12', '1-3', 'K-3, 5-10, 12',
       'PK-8 & Ungraded', '5', '12', 'K-8, 10-12', '1-9', '1-5, 7-8',
       '9, 12', '5-7', '8', '3-10', '1-12 & Ungraded', '5, 7-8, 10-12',
       'PK, 1-4', '1-4', '3, 6-7, 10, 12', '3-4, 6, 9-12', '1-2', '8-9',
       '4', 'PK-3, 5-7', 'K-1, 4, 6, 8', '5-10', '6-12 & Ungraded',
       '6-11', 'K, 5-12', 'K-6, 8', 'PK-4 & Ungraded', 'PK-1, 3-5',
       'PK-1, 3', '10-12 & Ungraded', 'K-3, 5-9, 11-12', 'PK-K, 2-4, 6-8',
       'PK, 3-4', '1-7', '1-10', 'PK, 2', '2, 4, 7, 9-10, 12', 'PK, 1',
       '1-3, 5, 8', '1-3, 5-6, 8', 'K, 3, 5-12', '4-11', 'K-4, 7-8',
       '7-8, 10-12', 'PK, 1, 3-12', '7, 9-12', 'PK-2, 6, 8', '2-6',
       'PK-8, 10-11', '2-3', '3-4', 'PK, 3-5', '3-9', 'PK-4, 6',
       'PK, 1-6', 'PK-4, 8', 'PK-K, 9-12', '3-11', 'PK-3 & Ungraded',
       'PK-3, 5-6', '2-7', '2-12 & Ungraded', 'PK-K, 2-7', '8-10', '2-4',
       'PK-4, 6-8', 'PK-K, 3-5, 7', '7, 11', 'K-5, 7, 9-10, 12',
       'PK-K, 2-4, 6 & Ungraded', '2', 'PK-7, 11', 'K, 2, 4-9, 12',
       'PK-1, 4, 6', '9-12 & Ungraded', '4-6, 8', '2-4, 6, 9-12', '4-7',
       'PK-3, 5-8', '1-2, 4-8', 'PK, 12', '10', '3-5, 9-10, 12', '5-11',
       '2-3, 5, 10-12', '3-10, 12', 'K-12 & Ungraded', '4-10',
       'PK-1, 3, 5', 'PK-1, 5, 7, 9', 'PK-K, 2-5', 'K, 2-7, 9',
       'K-7, 9-12', '2, 6-7', '6-10, 12', 'K-5, 7-9, 11',
       '2, 4, 6, 8, 10, 12', 'K-2, 4-12', 'PK, 7-12', '1, 3-4, 6-12',
       'K-6, 8-11', '2-5, 7-12', '1, 4-10, 12', 'PK-2, 4, 6, 8',
       'K-10, 12', '9 & Ungraded', 'PK-5 & Ungraded', 'PK-3, 5',
       '1, 3-5, 7', 'PK, 2, 4-7, 9-10, 12', 'K, 2, 5-12', 'PK-4, 6-12',
       '3', '4, 10', '2, 5-6, 8-12', 'K-6, 8-12', 'PK, 3-6, 8, 10, 12',
       'K-3, 6-8', '3-9, 11-12', 'PK-5, 7-12', 'K, 2-4, 7-12', '1-4, 6-8',
       'PK-3, 5-12', '1-3, 5-9', '1, 3-8', '9-11 & Ungraded', '5-9',
       'K, 4-5, 7-8', 'PK, 1-5', '3-12 & Ungraded', 'K-8 & Ungraded',
       '2-3, 5-8', '1-6, 9-12', 'PK-8, 10-12', 'PK-K, 4-8', 'K-1, 7-12',
       'K-4, 6-7, 9-12', '9-10, 12', 'K-5, 7', 'K, 2-8', '1, 4, 7, 10-11',
       'K, 2-3, 5-6', 'K-5, 7, 11-12', '7', 'PK-4, 7-12', 'K-9, 11-12',
       'K-4, 6-8, 10', '1, 3-5, 7-12', 'K-2, 5-7', 'K, 3, 6-8, 10, 12',
       'K, 3, 7-8, 12', 'PK, 9-12', 'K-2, 4-10, 12', '12 & Ungraded',
       'PK-6, 8-10', 'PK-1, 3-8', '1, 3', 'K-8, 12', '3-4, 6-9, 12',
       '5, 7-8', 'PK-K, 2-3', 'K-1, 3-12', '1, 5-9, 12', '5, 7-8, 10-11',
       'PK-5, 7-8', '4, 7, 10-12', 'PK-1, 3-4', 'PK-2, 4-6', 'K-8, 10',
       '10-11', '6, 9', 'PK-2, 4', 'K-4, 6', 'K-2, 6-7, 12', 'PK-6, 8',
       '3-4, 7, 10-12', '1, 3-7', 'K-5, 8', '2, 4-5, 7, 9-11',
       '1-3, 5, 7-8', '1-2, 9-12', 'K-1, 3-5, 7-8', 'K, 2-8, 10',
       'PK, 1-3, 6', '7-8, 10-11', '7, 10-12', '3, 5, 8-9, 11-12',
       '1-3, 5', 'K-5, 7-12', '1-7, 9-10, 12', '2, 4-8', 'K-3, 6-12',
       'PK, 5-8', '6-8, 10', 'PK-5, 7', 'PK, 1, 5', 'PK, 1-4, 6',
       '3, 5, 10, 12', 'PK-6, 8-12', '4-5, 7-12', 'PK-1, 6-7, 9-11',
       '2-7, 9-11', 'K-1, 6, 8, 11', '7, 9, 11-12', '1-3, 5-10',
       'K-5, 7-9', '1', 'K-5, 7-11', '7-12 & Ungraded', '1-6 & Ungraded',
       '3, 12', 'PK-8, 11', 'K-5, 7-9, 12', 'K-1, 4, 7-9, 11',
       '1-2, 4-12', 'PK-9, 11-12']

class TestParseGrades(unittest.TestCase):
    def test_join_string_grades_success(self):
        actual = parse_grades('2, 4, 6, 8, 10, 12')
        expected = ['2','4','6','8','10','12']
        self.assertEqual(actual, expected)

    def test_parse_grades_success(self):
        actual = parse_grades('K-4')
        expected = ['K', '1', '2', '3', '4']
        self.assertEqual(actual, expected)

    def test_multiple_separators(self):
        actual = parse_grades('2-4, 6, 9-12')
        expected = ['2', '3', '4', '6', '9', '10', '11', '12']
        self.assertEqual(actual, expected)

    def test_grades_list_with_ampersand(self):
        actual = parse_grades('6-12 & Ungraded')
        expected = ['6', '7', '8', '9', '10', '11', '12', 'Ungraded']
        self.assertEqual(actual, expected)

    def test_small_lists(self):
        actual = parse_grades('PK-K')
        expected = ['PK', 'K']
        self.assertEqual(actual, expected)

    def test_multiple_separators2(self):
        actual = parse_grades('PK-K, 2-4, 6 & Ungraded')
        expected = ['PK', 'K', '2', '3', '4', '6', 'Ungraded']
        self.assertEqual(actual, expected)

    def test_multiple_separators3(self):
        actual = parse_grades('5-10')
        expected = ['5', '6', '7', '8', '9', '10']
        self.assertEqual(actual, expected)

    def test_multiple_separators4(self):
        actual = parse_grades('K, 5-12')
        expected = ['K', '5', '6', '7', '8', '9', '10', '11', '12']
        self.assertEqual(actual, expected)

    def test_multiple_separators5(self):
        actual = parse_grades( 'PK-3, 5-7')
        expected = ['PK', 'K', '1', '2', '3', '5', '6', '7']
        self.assertEqual(actual, expected)

    def test_complete_dataset(self):
        # create a loop that goes thru dataset and invoke parse_grades with each element
        # used this to create dictionary of grade combo and parsed_grades
        separated_grades_list = []
        for i in unique_grades_combination:
            separated_grades_list.append(parse_grades(i))

        return separated_grades_list