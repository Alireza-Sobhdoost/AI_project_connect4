import math
import random


class TreeNode:
    def __init__(self, board, parent=None):
        self.board = board
        self.parent = parent
        self.visits = 0
        self.score = 0
        self.children = {}
        
        # Determine terminal state and expansion status
        self.is_terminal = board.winning_move(board.player_2) or not board.check_draw()
        self.is_fully_expanded = self.is_terminal


class MCTS:
    def __init__(self, iterations=17000, exploration_constant=2.25):
        self.iterations = iterations
        self.exploration_constant = exploration_constant

    def search(self, initial_state):
        root = TreeNode(initial_state)

        for _ in range(self.iterations):
            node = self.select(root)
            score = self.rollout(node.board)
            print(score)
            self.backpropagate(node, score)

        return self.get_best_move(root, exploration_constant=self.exploration_constant)

    def select(self, node):
        """Select the most promising child node."""
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.get_best_move(node, self.exploration_constant)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        """Expand the node by adding a new child."""
        for state in node.board.generate_states():
            if str(state.position) not in node.children:
                new_node = TreeNode(state, parent=node)
                node.children[str(state.position)] = new_node

                # Mark as fully expanded if all states are added
                if len(node.board.generate_states()) == len(node.children):
                    node.is_fully_expanded = True

                return new_node

        raise RuntimeError("Expand function encountered an unexpected issue.")


    def backpropagate(self, node, score):
        while node is not None:
            node.visits += 1
            node.score += score
            # print(f"Backpropagate: Node visits = {node.visits}, Score = {node.score}")
            score = -score  # Alternate for opponent's perspective
            node = node.parent

    def rollout(self, board):
        while not (board.winning_move(1) or board.winning_move(2)) :
            try:
                board = self.select_best_child(board)  # Choose the most promising state based on heuristic
            except IndexError:
                result = self.evaluate_board_state(board)
                # print(result)
                return result # Draw

        result = self.evaluate_board_state(board)

        if board.winning_move(board.player_2):
            # print(10 + result)
            return 10 + result
        elif board.winning_move(board.player_1):
            # print(-20 + result)
            return -20 + result
        else:
            # print(0)
            return 0

    def select_best_child(self, board):
        best_child = None
        best_score = float('-inf')

        for child in board.generate_states():
            score = self.evaluate_board_state(child)
            if score > best_score:
                best_score = score
                best_child = child

        # print(best_score)
        return best_child
    
    def heuristic_calc (self ,player, potential_lines) :
        player_score = 0
        best_score = 0
        for line in potential_lines :
            count_ally = 0
            count_enemy = 0

            for item in line :
                if item == player :
                    count_ally += 1
                if item == 1 :
                    count_enemy += 1

            if count_ally == 4 :
                player_score = 500
            elif count_ally == 1  :
                if count_enemy == 2 :
                    player_score = 300
                    # print("get here2")
                elif count_enemy == 3 :
                    player_score = 800
                    # print("get here3")
                        
            elif count_ally == 3 :
                player_score = 400
            elif count_ally == 2 :
                player_score = 10
            elif count_ally == 0 :
                if count_enemy == 2 :
                    player_score -= 250
                    # print("get here2")
                elif count_enemy == 3 :
                    player_score = 900
                    # print("get here3")
                        
                        
            if abs(player_score) > abs(best_score ):
                best_score = player_score

        return best_score

    def evaluate_board_state(self, board):
        # Example heuristic: difference in potential winning lines

        lines = board.potential_winning_lines()
        # print(len(lines))
        player_1_score = self.heuristic_calc(board.player_1 , lines)
        player_2_score = self.heuristic_calc(board.player_2 , lines)
        # player_1_score *= 1.5
        # player_2_score *= 1
        # print(player_2_score , player_1_score)
        return  player_2_score 

    def get_best_move(self, node, exploration_constant):
        best_score = float('-inf')
        best_moves = []

        for child in node.children.values():
            exploitation = child.score / (child.visits + 1e-6)
            exploration = exploration_constant * math.sqrt(math.log(node.visits + 1) / (child.visits + 1e-6))
            uct_score = exploitation + exploration

            if uct_score > best_score:
                best_score = uct_score
                best_moves = [child]
            elif uct_score == best_score:
                best_moves.append(child)
        return random.choice(best_moves)