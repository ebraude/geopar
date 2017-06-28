#### Intent
This project implements a type of computational reasoning. It postulates and proves various theorems
in plane geometry. In particular, it can prove a new generalization of Morley's Trisector Theorem (as of June, 2016).

#### To Run the Program
(1) Specify the input in input.txt (see below for format)
(2) Execute `run.py` script. GEOPAR may ask whether the user wants "pairing," to which the user usually agrees. This is explained in the paper.

#### Functionality (diagrams to be updated)
[Activity Diagram](https://drive.google.com/open?id=1NkYzuc2SvzuM0E-Suw00hTjIOd0kKMthwJZFddhUuCc)  
[Class Model](https://drive.google.com/open?id=0B13UVf6NnzqsUnRobzFkcldDR2c)

#### Format of `input.txt`
`input.txt` file serves as an input source for the project. It specifies the vertices (points) and the angles of a triangulated figure.

The first number `n` on the first line in `input.txt` denotes a number of triangles in the triangulated figure.
The second number `m` on the first line in `input.txt` denotes a dimension of the angles that constitute those triangles.
The following `n` lines denote the points (vertices) and angles of each triangle in the triangulated figure.
The program will process first `n+1` lines in `input.txt` and neglect the remaining part.

The points are written as 3 non-zero, distinct integer numbers in clockwise order separated by a comma.  
_Example:_ `1, 3, 5`

The angle is written as a mathematical expression:
it is a finite combination of linear terms, where a term is specified by a
_coefficient_ and a _variable_: `aα + bβ + c` (`c` is a constant term).

Coefficients can be of the form:
1. 2, 3, 4 - integer number
2. 2.5, 3.14 - floating point number
3. 1/2, 3/4 - fraction number

Terms can be of the form:
1. α - greek letter
2. a, b, c - latin letter
3. \alpha, \beta - Latex style.

One line contains information about one triangle: three points and three angles,
where group of points is separated by a semicolon from a group of angles. 
Please note that points and angles correspond to each other via their indices in the list.

* This is an example of an information about triangle with all known angles for `m = 3`:  
  `1, 3, 5; -α - β + 60, β, α + 120`  
  Vertices: `1, 3, 5`  
  Angles: `-α - β + 60, β, α + 120`
* This is an example of an information about triangle with one `unknown` angle:  
  `1, 5, 4; -α - β + 60, β, x`
  Vertices: `1, 5, 4`  
  Angles: `-α - β + 60, β + 60, unknown`

The program processes only the first triangle configuration in `input.txt`.
Thus, you may store all your configurations in `input.txt`, and move the one of interest to the top
before running the program.

#### Example Configurations
Examples of triangle configurations are collected in a separate section of this github site.

#### Conventions
- Triangle vertices are called triangle points (or simply, points), for convenience

#### Terminology
- interior point
- dimension of angle
- angle points (Triangle)
