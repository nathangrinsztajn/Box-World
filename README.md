# Box-World
Implementation of the Box-World environment from the paper "Relational Deep Reinforcement Learning"

| Example Game 1 | Example Game 2 | Example Game 3 |
| :---: | :---: | :---: 
| ![Game 1](/examples/round_1.gif?raw=true) | ![Game 2](/examples/round_2.gif?raw=true) | ![Game 3](/examples/round_0.gif?raw=true) |

Box-World is made to explicitly target relational reasoning.

![Box-World grid](/examples/box_world.png)

It is a perceptually simple but combinatorially complex environment that requires abstract relational reasoning and planning. It consists of a n × n pixel room with keys and boxes randomly scattered. The room also contains an agent, represented by a single dark gray pixel, which can move in four directions: up, down, left, right. Keys are represented by a single colored pixel. The agent can pick up a loose key (i.e., one not adjacent to any other colored pixel) by walking over it. Boxes are represented by two adjacent colored pixels – the pixel on the right represents the box’s lock and its color indicates which key can be used to open that lock; the pixel on the left indicates the content of the box which is inaccessible while the box is locked. To collect the content of a box the agent must first collect the key that opens the box (the one that matches the lock’s color) and walk over the lock, which makes the lock disappear. At this point, the content of the box becomes accessible and can be picked up by the agent. Most boxes contain keys that, if made accessible, can be used to open other boxes. One of the boxes contains a gem, represented by a single white pixel. The goal of the agent is to collect the gem by unlocking the box that contains it and picking it up by walking over it. The key that an agent has in possession is depicted in the input observation as a pixel in the top-left corner. In each level, there is a unique sequence of boxes that need to be opened to reach the gem. Opening one wrong box (a distractor box) leads to a dead-end where the gem cannot be reached and the level becomes unsolvable.

Three user-controlled parameters contribute to the difficulty of the level:
l. The number of boxes in the path to the goal (solution length)
l. The number of distractor branches 
l. The length of the distractor branches.

In general, the task is computationally difficult for a few reasons. First, a key can only be used once, so the agent must be able to reason about whether a particular box is along a distractor branch or the solution path. Second, keys and boxes appear in random locations in the room, emphasizing a capacity to reason about keys and boxes based on their abstract relations, rather than based on their spatial positions
