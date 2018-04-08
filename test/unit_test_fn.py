from chess.move import Move


def assert_contains(actual_move_list, expected_move_list):
    if len(actual_move_list) != len(expected_move_list):
        raise AssertionError("Length " + str(len(actual_move_list)) + " != " + str(len(expected_move_list)))
    for expectedMove in expected_move_list:
        for actualMove in actual_move_list:
            if actualMove == expectedMove:
                break
        else:
            raise AssertionError(str(expectedMove) + " expected, but was not present in " + str(actual_move_list))


def assert_length(input_list, length):
    if len(input_list) != length:
        raise AssertionError("Expected list of length " + str(length) + " but was " + str(len(input_list)))


def assert_true(msg, boolean):
    if not boolean:
        raise AssertionError(msg)


def assert_false(msg, boolean):
    if boolean:
        raise AssertionError(msg)


def create_list_of_moves(move_type, start_coord, end_coord_list):
    to_return = []
    for end_coord in end_coord_list:
        to_return.append(Move(move_type, start_coord, end_coord))
    return to_return


def assert_row_contain_same_type_elements(expected_row, actual_row):
    assert_true("Unexpected home row length", len(actual_row) == len(expected_row))
    for col in range(0, 8):
        assert_true("Rows types different."
                    + "\nExpected=" + str(expected_row)
                    + "\nActual  =" + str(actual_row), expected_row[col].type == actual_row[col].type)
