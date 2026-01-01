from env import Blackjack_Env, Action

def get_player_action() -> Action:
    while True:
        user_input = input("Choose action [h = hit, s = stand, d = double]: ").strip().lower()

        if user_input == "h":
            print('')
            return Action.HIT
        elif user_input == "s":
            print('')
            return Action.STAND
        elif user_input == "d":
            print('')
            return Action.DOUBLE
        else:
            print("Invalid input. Please enter 'h', 's' or 'd'.")

def print_hands(env, state):
    print(f"Dealer: {env.dealer_hand.cards[0]}")    
    print(f"Player: {env.player_hand.cards} (value={state[0]}), Can double={state[2]}")

def main():
    blackjack_env = Blackjack_Env()
    state = blackjack_env.reset()
    done = False

    while not done:
        print_hands(blackjack_env, state)

        action = get_player_action()
        state, done, reward = blackjack_env.step(action)

    print(f"Dealer: {blackjack_env.dealer_hand.cards} (value={blackjack_env.dealer_hand.best_value})")  
    print(f"Player: {blackjack_env.player_hand.cards} (value={blackjack_env.player_hand.best_value})")
    print(f'Reward: {reward}')
    print('Game finished')

if __name__ == '__main__':
    main()