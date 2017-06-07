# snakepy
AI powered classic snake game implemented using pygame and Reinforcement learning. You may also like my [Self Driving Car simulation](https://github.com/satwikkansal/smartcab) project developed on similar lines.

## Usage

```sh
python snake.py
```

## Configurations

To configure the game accoring to you, open the snake.py and change the constants defined at the top.
#TODO: Add CLI arguments support

## How it works?
As of now, it uses Q-learning algorithm to decide the next move and it really gets smart after few iterations of trainiing.

## Current Status

![GIF output](https://github.com/satwikkansal/snakepy/blob/master/outputs/out.gif)

PS: The rule of "snake-biting itself and getting killed" was disabled while taking this screencast.

## Next Steps

- Add Length of the sanke to state
- Apply state space optimizations to reduce the state space.
- Implement SARSA and compare results.
- Integrate Deep Q-Learning and compare results.
