# Box-World

## Introduction

Gym implementation of the Box-World environment from the paper "Relational Deep Reinforcement Learning" (https://arxiv.org/pdf/1806.01830.pdf), which is made to explicitly target relational reasoning.

| Example Game 1 | Example Game 2 | Example Game 3 |
| :---: | :---: | :---: 
| ![Game 1](/examples/round_easy.gif?raw=true) | ![Game 2](/examples/round_medium.gif?raw=true) | ![Game 3](/examples/round_hard.gif?raw=true) |

It is a perceptually simple but combinatorially complex environment that requires abstract relational reasoning and planning. It consists of a n × n pixel room with keys and boxes randomly scattered. The room also contains an agent, represented by a single dark gray pixel, which can move in four directions: up, down, left, right. Keys are represented by a single colored pixel. The agent can pick up a loose key (i.e., one not adjacent to any other colored pixel) by walking over it. Boxes are represented by two adjacent colored pixels – the pixel on the right represents the box’s lock and its color indicates which key can be used to open that lock; the pixel on the left indicates the content of the box which is inaccessible while the box is locked.

<div style="padding:20%">
  <p align="center">
    <img src="/examples/box_world.png?raw=true">
  </p>
  <p align="center" id="topologyMask">
  </p>
</div>

To collect the content of a box the agent must first collect the key that opens the box (the one that matches the lock’s color) and walk over the lock, which makes the lock disappear. At this point, the content of the box becomes accessible and can be picked up by the agent. Most boxes contain keys that, if made accessible, can be used to open other boxes. One of the boxes contains a gem, represented by a single white pixel. The goal of the agent is to collect the gem by unlocking the box that contains it and picking it up by walking over it. The key that an agent has in possession is depicted in the input observation as a pixel in the top-left corner. In each level, there is a unique sequence of boxes that need to be opened to reach the gem. Opening one wrong box (a distractor box) leads to a dead-end where the gem cannot be reached and the level becomes unsolvable.

Three user-controlled parameters contribute to the difficulty of the level:
 - The number of boxes in the path to the goal (solution length) 
 - The number of distractor branches 
 - The length of the distractor branches

In general, the task is computationally difficult for a few reasons. First, a key can only be used once, so the agent must be able to reason about whether a particular box is along a distractor branch or the solution path. Second, keys and boxes appear in random locations in the room, emphasizing a capacity to reason about keys and boxes based on their abstract relations, rather than based on their spatial positions.

## Actions
The game provides 4 actions to interact with the environment. 
The mapping of the action numbers to the actual actions looks as follows

 | Action       | ID    | 
 | --------     | :---: | 
 | Move Up      | 0     |  
 | Move Down    | 1     | 
 | Move Left    | 2     |   
 | Move Right   | 3     |
 
## Environment Configuration
### Environment Parameters
 | Parameter  |   Description  | 
 | --------     | :---: | 
 | n      | Grid size     |  
 | goal_length    | Number of keys to collect to solve the level| 
 | num_distractor    | Number of distractors    |   
 | distractor_length   | Number of distractor keys in each distractor path    |
 | max_steps   | Maximum number of steps in a trajectory   |
 | collect_key   | If true, a key is collected immediately when its corresponding lock is opened |
 
 
### Rendering Modes
| Mode | Description |
| ---  | --- 
| rgb_array | Returns the world image as a numpy array 
| human | Displays the current state on screen

 ## Quick Game
 
 ```bash
 python Human_playing_Commandline.py --gifs
```
