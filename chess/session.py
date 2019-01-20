#!/usr/bin/python
import json
import socket
import sys
from builtins import str, KeyboardInterrupt
from collections import deque

from chess.board import print_board, filter_self_checking_moves, selected_piece, is_being_checked, \
    can_player_leave_check_state, is_stalemate, is_impossible_to_reach_checkmate, is_threefold_repetition_stalemate, \
    is_fifty_move_rule_draw, update_move_history, conduct_move, convert_to_string_gameboard, create
from chess.move import Move
from chess.utils import opposite_col, ProgressState, send_msg, recv_msg


class Session(object):
    def __init__(self):
        self.game_board = create()
        # Maintain complete history of all potential game moves (for the three-fold repetition rule)
        self.potential_moveset_history = []
        # The Wikipedia page for the 50-move rule suggests that for the purposes the rule, a move is a player's turn
        # followed by opponents turn.
        self.history_length = 50 * 2
        # Maintain complete history of actually completed moves (for the 50-move rule, and en passant)
        self.conducted_move_history = deque([], self.history_length)
        self.progress_state = ProgressState.IN_PROGRESS
        self.player_turn = "white"

    def get_game_state(self, player_color):
        return {'board': convert_to_string_gameboard(self.game_board),
                'progress_state': self.progress_state.to_serializable(),
                'player_turn': self.player_turn,
                'your_color': player_color}

    def get_moves(self, player_color, selection_coords):
        if player_color != self.player_turn:
            return False
        piece_legal_move_set = []
        if not selection_coords:
            print("invalid selection")
        elif selected_piece(self.game_board, selection_coords).is_blank_piece:
            print('...Error invalid piece (empty square).')
        elif selected_piece(self.game_board, selection_coords).col != self.player_turn:
            print('...Error selected opponents\' piece. Choose another piece\n')
        else:
            piece_total_move_set = selected_piece(self.game_board, selection_coords)\
                .get_move_set(self.game_board, selection_coords, self.conducted_move_history)
            piece_total_move_set += selected_piece(self.game_board, selection_coords)\
                .get_attack_set(self.game_board, selection_coords, self.conducted_move_history)
            piece_legal_move_set = filter_self_checking_moves(self.game_board, piece_total_move_set, self.player_turn,
                                                              self.conducted_move_history)
            print('Selected piece: \'' + selected_piece(self.game_board, selection_coords).type + '\'.', )

        # Convert to dictionary for serializability
        dict_move_list = list(map(lambda m: m.convert_to_dict(), piece_legal_move_set))
        return dict_move_list

    def make_move(self, player_color, selected_move):
        if player_color != self.player_turn:
            return False
        chosen_move = Move.create_from_dict(selected_move)

        update_move_history(self.game_board, self.potential_moveset_history, self.player_turn, self.conducted_move_history)
        self.game_board, move_history_element = conduct_move(self.game_board, chosen_move, self.player_turn)
        self.conducted_move_history.append(move_history_element)

        if not self.game_board:
            print("Illegal move not caught by game logic")

        if is_being_checked(self.game_board, opposite_col(self.player_turn)):
            if can_player_leave_check_state(self.game_board, opposite_col(self.player_turn), self.conducted_move_history):
                self.progress_state = ProgressState.CHECK
            else:
                print_board(self.game_board)
                self.progress_state = ProgressState.CHECKMATE
        else:
            self.progress_state = ProgressState.IN_PROGRESS

        self.player_turn = opposite_col(self.player_turn)
        if is_stalemate(self.game_board, self.player_turn, self.conducted_move_history):
            self.progress_state = ProgressState.DRAW_STALEMATE
        elif is_impossible_to_reach_checkmate(self.game_board):
            self.progress_state = ProgressState.DRAW_INSUFFICIENT_MATERIALS
        elif is_threefold_repetition_stalemate(self.potential_moveset_history):
            self.progress_state = self.progress_state.DRAW_THREEFOLD_REPETITION
        elif is_fifty_move_rule_draw(self.conducted_move_history):
            self.progress_state = self.progress_state.DRAW_FIFTY_MOVE_RULE

        print(self.player_turn + 's turn. Waiting for selection')
        return True
