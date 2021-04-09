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



