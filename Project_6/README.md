# Project 6

## Summary
This visualization is based on the database export of the [World Cube Association](http://www.worldcubeassociation.org)(WCA). The WCA governs competitions for twisted puzzles, with the widely know "Rubik's Cube" as most popular event. In this project, I will create a visualization for the number of competitions individual competitors have attended. I recently attended my 100th competition, which makes me the 25th person ever to reach this benchmark.

## Design
[Screenshot](images/final_visualization.png)

* The visualization shows each competitor as a bubble in a bubble chart. The size represents the number of competitions. I decided to use a linear scale to map the variable to the radius of the bubble.
* Furthermore, the bubbles are colored according to the nationality of the competitor using an ordinal scale and the ['schemeCategory20'](https://github.com/d3/d3-scale) color scheme.
* When hovering over a bubble, a small tooltip with the name, the nationality and the number of competitions of the competitor is shown.
* In order to allow users to interact with the chart, I added a drag and drop function, which makes the bubbles movable. There is also a collision prevention, so the other bubbles are pushed aside when one of them is moved. This is not an essential function to understand the data, but it invites to play around with it.

## Feedback
This section represents a collection of feedback I received for the initial version of the chart and subsequent revisions. As I did not consequently push all changes to GitHub, I have only included this version here.

#### Boring design
The first feedback for the initial design was that the black/white design was rather boring and not very appealing.

Instead of just adding some colors to the css file, I decided to use additional information to color the bubbles. Despite the name and the number of competitions, the dataset also includes the nationalities. Therefore, I used a category scale to color each bubble according to the nationality the competitor has.

#### Bubble are difficult to differentiate and too small
Another point was that the bubbles are difficult to differentiate and too small. Especially on a small screen the bubbles are so cluttered that it's nearly impossible to find the right spot to let the tooltip appear.

This is partly solved by the improvement mentioned in the first step. The size was still a problem though. I decided to upscale the complete visualization and set the range of the bubbles to 10-50 instead of 2-20.

#### Static
This feedback was a very basic one: the reviewer said that he does not see any advantage in using a web application instead of a simple drawing for this kind of visualization.

This feedback resulted in two changes:
* Use of forces
[d3-force](https://github.com/d3/d3-force) is a neat module to simulate physical forces. There are several forces which can be used. I chose *n-body* and *collide*. *n-body* applies mutually amongst all elements. By setting a positive value for strength it simulates gravity. By setting a negative value it's electrostatic charge. I decided to use a positive strength of 10. Additionally, I used the collide function, which creates a circle collision with a specified radius. I set the radius to the radius of the node + 20.

* Drag & drop function
Afterwards, I decided to also add a [drag and drop function](https://github.com/d3/d3-drag) which lets you move the individual bubbles.

## Resources
* [D3 Wiki and documentation](https://github.com/d3/d3/wiki)
* [Udacity Website](http://www.udacity.com)
* [d3-force](https://github.com/d3/d3-force)
* [D3.js version 4](https://anthonyskelton.com/2016/d3-js-version-4/)
* [Bubble charts in D3](https://jrue.github.io/coding/2014/exercises/basicbubblepackchart/)
* [WCA database export](https://www.worldcubeassociation.org/results/misc/export.html)
