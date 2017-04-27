# Project 6

## Summary
This visualization is based on the database export of the [World Cube Association](http://www.worldcubeassociation.org)(WCA). The WCA governs competitions for twisted puzzles, with the widely know "Rubik's Cube" as most popular event. In this project, I will create a visualization for the number of competitions individual competitors have attended. I recently attended my 100th competition, which makes me the 25th person ever to reach this benchmark.

## Design


## Feedback
### Boring design
The first feedback for the initial design was that the black/white design was rather boring and not very appealing.

I decided to use additional information to colour the bubbles. Despite the name and the number of comeptitions, the dataset also includes the nationalities. Therefore, I used a category scale to colour each bubble according to the nationality the competitor has.

### Bubble are difficult to differentiate and too small
Another point was that the bubbles are difficult to differentiate and too small. This is partly solved by the improvement mentioned in the first step. The size was still a problem though. I decided to upscale the complete visualization and set the range of the bubbles to 10-50 instead of 2-20.

### Static
This feedback was a very basic one: the reviewer said that he does not see any advantage in using a web application for this kind of visualization.

This feedback resulted in two changes:
#### Use of forces
d3-force is a neat module to simulate physical forces. There are several forces which can be used. I chose *n-body* and *collide*.

*n-body* applies mutually amongst all elements. By setting a positive value for strength it simulates gravity. By setting a negative value it's electrostatic charge. I decided to use a positive strength of 10.

Additionally, I used the collide function, which creates a circle collision with a specified radius. I set the radius to the radius of the node + 20.


#### Drag & drop function


## Resources
* [D3 Wiki and documentation](https://github.com/d3/d3/wiki)
* [Udacity Website](http://www.udacity.com)
* [d3-force](https://github.com/d3/d3-force)
* [D3.js version 4](https://anthonyskelton.com/2016/d3-js-version-4/)
* [Bubble charts in D3](https://jrue.github.io/coding/2014/exercises/basicbubblepackchart/)
