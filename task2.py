from __future__ import division

import math
import sys
from collections import namedtuple


class SplitNumber:
    def __init__(self, number_str, divider):
        self.number_str = number_str
        self.divider = divider
        self.number_int = int(number_str)
        self.number_len = len(number_str)

    def __repr__(self):
        return '{number_str}({divider})'.format(number_str=self.number_str, divider=self.divider)


NumberShiftPair = namedtuple('NumberShiftPair', 'number_str shift')


# noinspection PyMethodMayBeStatic
class InfinitySequenceSolver:
    def complete_right_number(self, previous_split_number, right_split_number):
        right_number_free_positions = right_split_number.divider - right_split_number.number_len
        return (right_split_number.number_int * 10 ** right_number_free_positions +
                (previous_split_number.number_int + 1) % (10 ** right_number_free_positions))

    def check_left_number(self, next_number_int, left_split_number):
        left_number_int = left_split_number.number_int
        left_number_free_positions = left_split_number.divider - left_split_number.number_len
        number_difference = next_number_int - left_number_int - 1
        divisor = 10 ** left_split_number.number_len
        if number_difference % divisor == 0:
            free_positions_candidate = number_difference // divisor
            if ((free_positions_candidate == 0 and left_number_free_positions == 0) or
                (free_positions_candidate != 0 and
                    len(str(free_positions_candidate)) == left_number_free_positions)):
                return NumberShiftPair(str(next_number_int - 1), left_number_free_positions)

    def check_two_split_combination_length(self, left_split_number, right_split_number):
        right_number_int = self.complete_right_number(left_split_number, right_split_number)
        number_shift_pair = self.check_left_number(right_number_int, left_split_number)
        if number_shift_pair:
            return number_shift_pair

    def check_combination(self, split_combination):
        if len(split_combination) == 1:
            return NumberShiftPair(split_combination[0].number_str, 0)

        left_split_number = split_combination[0]
        left_ptr = 0 if len(left_split_number.number_str) == left_split_number.divider else 1

        right_split_number = split_combination[-1]
        if len(right_split_number.number_str) == right_split_number.divider:
            right_ptr = len(split_combination) - 1
        else:
            right_ptr = len(split_combination) - 2

        for i in range(left_ptr, right_ptr):
            if int(split_combination[i + 1].number_str) - int(split_combination[i].number_str) != 1:
                return
        if len(split_combination) == 2:
            return self.check_two_split_combination_length(left_split_number, right_split_number)

        # Проверка краевых обрезанных чисел когда чисел больше 3
        if (self.complete_right_number(split_combination[-2], right_split_number) -
                split_combination[-2].number_int != 1):
            return
        number_shift_pair = self.check_left_number(split_combination[1].number_int,
                                                   left_split_number)
        if number_shift_pair:
            return number_shift_pair

    def check_combination_to_zero_start_numbers(self, split_combination):
        left_split_number = split_combination[0]
        if (left_split_number.number_len == left_split_number.divider and
                left_split_number.number_str.startswith('0')):
            return False
        for i in range(1, len(split_combination)):
            if split_combination[i].number_str.startswith('0'):
                return False
        return True

    def get_good_number_shift_pairs(self, string, string_length, offset, base_divider):
        good_number_shift_pairs = []
        secondary_divider = base_divider + 1
        max_base_divider_count = math.ceil((string_length - offset) / base_divider)
        min_base_divider_count = 0 if offset else 1
        for base_divider_count in range(min_base_divider_count, max_base_divider_count + 1):
            split_combination = [SplitNumber(string[0: offset], base_divider)] if offset else []
            base_divider_end = offset + base_divider * base_divider_count
            for i in range(offset, base_divider_end, base_divider):
                split_combination.append(SplitNumber(string[i: i + base_divider], base_divider))
            for i in range(base_divider_end, string_length, secondary_divider):
                split_combination.append(
                    SplitNumber(string[i: i + secondary_divider], secondary_divider)
                )
            if self.check_combination_to_zero_start_numbers(split_combination):
                number_shift_pair = self.check_combination(split_combination)
                if number_shift_pair:
                    good_number_shift_pairs.append(number_shift_pair)
        return good_number_shift_pairs

    def get_closest_number_shift_pair(self, string):
        string_length = len(string)
        if string == '0' * string_length:
            return NumberShiftPair('1{string}'.format(string=string), 1)
        for base_divider in range(string_length + 1):
            good_number_shift_pairs = []
            for offset in range(base_divider):
                good_number_shift_pairs.extend(
                    self.get_good_number_shift_pairs(
                        string=string,
                        string_length=string_length,
                        offset=offset,
                        base_divider=base_divider
                    )
                )

            if good_number_shift_pairs:
                return min(good_number_shift_pairs, key=lambda x: int(x.number_str))

    def get_substring_index(self, number_shift_pair):
        number_str, shift = number_shift_pair
        number_length = len(number_str)
        index = (1 + sum(9 * i * 10 ** (i - 1) for i in range(1, number_length)) +
                 (int(number_str) - 10 ** (number_length - 1)) * number_length)
        return index + shift


def main():
    infinity_sequence_solver = InfinitySequenceSolver()
    for line in sys.stdin:
        line = line.rstrip()
        number_shift_pair = infinity_sequence_solver.get_closest_number_shift_pair(line)
        index = infinity_sequence_solver.get_substring_index(number_shift_pair)
        print(index)


if __name__ == '__main__':
    main()
