# TurtLSystems

*In development. Project is still messy and not fully documented or tested.*

Python package for drawing [l-systems](https://en.wikipedia.org/wiki/L-system) with turtle graphics with options for png and gif output.

**<https://pypi.org/project/TurtLSystems/>**

`pip install TurtLSystems`

For png and gif output you need the ghostscript image converter: <https://ghostscript.com/>

Example and generating code:

![example](https://raw.githubusercontent.com/discretegames/TurtLSystems/main/example.gif)

```py
from TurtLSystems import init, draw
init((600, 600), background_color=(36, 8, 107))
draw('A', 'A B-A-B B A+B+A.', 60, 8, 5, 2, heading=150, position=(200, 00),
    color=(200, 220, 255), fill_color=(255, 255, 255), red_increment=-2, duration=30,
    gif='tri', max_frames=500, draws_per_frame=1, padding=10, fin=True, speed=10, asap=False)
```

Rules:
```
F	         Move forward by line length drawing a line
f	         Move forward by line length without drawing a line
+	         Turn left by turning angle
-	         Turn right by turning angle
|	         Reverse direction (ie: turn by 180 degrees)
[	         Push current drawing state onto stack (position, angle, pensize, length)
]	         Pop current drawing state from the stack
>	         Increment the line width by line width increment
>	         Decrement the line width by line width increment
@	         Draw a dot with line width radius (use default turtle dot ra)
{	         Open a polygon
}	         Close a polygon and fill it with fill colour
*	         Multiply the line length by the line length scale factor
/	         Divide the line length by the line length scale factor
^			add line len incr
%			subtract line len incr
&	         Swap the meaning of + and -
(	         Decrement turning angle by turning angle increment
)	         Increment turning angle by turning angle increment
0			switch pen to color0 (default)
1			switch pen to color1
2			switch pen to color2
3			switch pen to color3
4			switch pen to color4
5			switch fill to color0 (change to allow 10 colors total for each? YES)
6			switch fill to color1 (default)
7			switch fill to color2
8			switch fill to color3
9			switch fill to color4
_			reset line length back to initial value
=			reset line width back to initial value
~			reset turning angle back to initial value
#			next color op (0-9 ,.;:!? applies to fill color rather than pen color)
(space, any other chars) 	ignored
`			clear stack
$			stop everything immediately
,.			increase/decrease red by red delta (does not affect color list)
;:			green
?!			blue
```
