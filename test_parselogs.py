import unittest
from parselogs import Measure, is_region_line, is_date_line, get_date, get_region_count, parselogs

class ParselogsTest(unittest.TestCase):
    def test_is_region_line(self):
        self.assertTrue(is_region_line('🔸Московская область - 460'))
        self.assertFalse(is_region_line('Stepan Kuznetsov, [13.04.20 12:21]'))
        self.assertFalse(is_region_line('За последние сутки в России подтверждено 2774 новых случая коронавируса в 51 регионе, зафиксировано 22 летальных исхода. За сутки по России полностью выздоровели 224 человека.'))

    def test_is_date_line(self):
        self.assertFalse(is_date_line('🔸Московская область - 460'))
        self.assertTrue(is_date_line('Stepan Kuznetsov, [13.04.20 12:21]'))
        self.assertFalse(is_date_line('За последние сутки в России подтверждено 2774 новых случая коронавируса в 51 регионе, зафиксировано 22 летальных исхода. За сутки по России полностью выздоровели 224 человека.'))

    def test_get_date(self):
        self.assertEqual('2020-04-13', get_date('Stepan Kuznetsov, [13.04.20 12:21]'))

    def test_get_region_and_count(self):
        (region, count) = get_region_count('🔸Московская область - 460')
        self.assertEqual('Московская область', region)
        self.assertEqual(460, count)
        # issue #4
        (region, count) = get_region_count('🔸Московская область -460')
        self.assertEqual(460, count)

    def test_parselogs(self):
        parse_result = parselogs('data/test.txt')
        expected = [
            Measure('Москва', '2020-04-15', 1355), Measure('Волгоградская область', '2020-04-15', 6),
            Measure('Москва', '2020-04-13', 1489), Measure('Московская область', '2020-04-13', 460)]
        self.assertCountEqual(parse_result, expected)


if __name__ == '__main__':
    unittest.main()