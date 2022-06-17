from typing import List

BOARD_SIZE = 4


def coords_outside_board(path):
    for coord_row, coord_col in path:
        if (not 0 <= coord_col < BOARD_SIZE) or (
                not 0 <= coord_row < BOARD_SIZE):
            return True
    return False


def next_move(cell):
    coords_set = set()
    x, y = cell
    coords_set.add((x + 1, y))
    coords_set.add((x, y + 1))
    coords_set.add((x + 1, y + 1))
    coords_set.add((x - 1, y))
    coords_set.add((x - 1, y - 1))
    coords_set.add((x, y - 1))
    coords_set.add((x + 1, y - 1))
    coords_set.add((x - 1, y + 1))
    return coords_set


def legal_path(path):
    for index in range(1, len(path)):
        if path[index] not in next_move(path[index - 1]):
            return False
    return True


def validate_path(path):
    if coords_outside_board(path):
        return False
    if len(path) != len(set(path)):
        return False
    if not legal_path(path):
        return False
    return True


def extract_word(board, path):
    word = ''
    for coord_row, coord_col in path:
        word += board[coord_row][coord_col]
    return word


def is_valid_path(board, path, words):
    if not validate_path(path):
        return None
    word = extract_word(board, path)
    if word in words:
        return word
    return None


def _board_cells():
    cell_lst = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            cell_lst.append((row, col))
    return cell_lst


def shrink_dict(words_dict, path, board):
    partial_word = extract_word(board, path)
    new_dict = {word for word in words_dict if
                word[:len(partial_word)] == partial_word}
    return new_dict


def find_all_paths(n, path: List, words_dict, board):
    if len(path) == n and is_valid_path(board, path, words_dict):
        return [path[:]]
    if not words_dict:
        return []
    result = []
    if len(path) == 0:
        for coord in _board_cells():
            path.append(coord)
            result.extend(
                find_all_paths(n, path, shrink_dict(words_dict, path, board),
                               board))
            path.pop()
    else:
        for coord in next_move(path[-1]):
            path.append(coord)
            if validate_path(path):
                result.extend(
                    find_all_paths(n, path,
                                   shrink_dict(words_dict, path, board),
                                   board))
            path.pop()
    return result


def find_length_n_paths(n, board, words):
    result = []
    for path in find_all_paths(n, [], words, board):
        if is_valid_path(board, path, words) is not None:
            result.append(path)
    return result


def find_all_words(n, path: List, board, words_dict, result):
    if n == 0:
        if is_valid_path(board, path, words_dict):
            result.append(path[:])
        return
    if len(path) == 0:
        for coord in _board_cells():
            path.append(coord)
            if len(board[coord[0]][coord[1]]) == 1:
                (find_all_words(n - 1, path, board, words_dict, result))
            elif n > 1:
                (find_all_words(n - 2, path, board, words_dict, result))
            path.pop()
    else:
        for coord in next_move(path[-1]):
            path.append(coord)
            if validate_path(path):
                if len(board[coord[0]][coord[1]]) == 1:
                    (find_all_words(n - 1, path, board, words_dict, result))
                elif n > 1:
                    (find_all_words(n - 2, path, board, words_dict, result))
            path.pop()
    return result


def find_length_n_words(n, board, words):
    result = []
    if n <= 0:
        return []
    for path in find_all_words(n, [], board, words, []):
        if is_valid_path(board, path, words) is not None:
            result.append(path)
    return result


def max_score_paths(board, words):
    result = []
    paths_dict = {}  # dict = {word: path}
    for n in range(2, 17):
        result += find_length_n_paths(n, board, words)
    for path in result:
        word = extract_word(board, path)
        if word not in paths_dict:
            paths_dict[word] = path
        else:
            if len(paths_dict[word]) < len(path):
                paths_dict[word] = path
    val_lst = [value for key, value in paths_dict.items()]
    return val_lst
