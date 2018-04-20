# Fuzzy Algorithm apply on self-driving car

## Introduction

This program is the homework of Computational Intelligence in NCU.
This program applies the fuzzy algorithm on a simple self-driving car system.

The program is written in **python3.6**. 
The require package is shown below.
```python=3.6
import sys, pygame
import os
import time
import math
```

* The map is set in `map.txt`
* Fuzzy type is sellected in `Method.txt`.
There are three type of fuzzy I wrote, which is 
    1. Functional base fuzzy
    2. Center Gravity fuzzy
    3. Mean Max fuzzy

To edit the content in `Methdo.txt` as `Fuzzy`, `FuzzyGravity` or `FuzzyMean`  can change the program fuzzy type.

The main program is `autoCar.py`. 
Run the `game2exe.py` can convert the python script to the executable program.

An output Log and the screenshot will save at working direction after the program is finished.

## Fuzzy design


* The input distance function
Front distance
![](https://i.imgur.com/1v7Idhe.png)
Left and Right distance
![](https://i.imgur.com/cPYdlho.png)

* The output degree function

![](https://i.imgur.com/68LBdUp.jpg)

## Result

For the comparison of the three methods I wrote.

**The Functional base fuzzy** is as below. It shows that froms the first corner, the car had an extra turn before it back to the right path
![](https://i.imgur.com/38ZrlX7.jpg)

And in **Center Gravity** or **Mean Max** method, both of them are very stable tour to the end. But the Center Gravity is more stable than Mean Max due to less shaking when the car moved.
(Center Gravity)
![](https://i.imgur.com/23jmbzF.jpg)
(Mean Max)
![](https://i.imgur.com/aIyD88J.jpg)
