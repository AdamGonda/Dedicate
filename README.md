# Dedicate
## This is my first pet projet
I liked to build this to mimic an existing app on my phone, which was a gamified math trainer. I had a few ideas about how I’d liked to implement mine in python, and a few in terms of features, but I did use just the terminal up until then to UI purposes, so I had to look up some library for the UI and I found [Kivy](https://kivy.org)

![](https://github.com/AdamGonda/Dedicate/blob/master/q%26a.png)


The main idea was that you can compose question sets in text files with a specified format which looks like this:
```
question, a1, a2, a3, a4
          ^
          |
       Good answer 
       
       
Eg.
1 + 1 = ?, 2, 3, 4, 5
```
Then it's shuffling the questions and present them to the user.
During one session you have limited time and lives to answer them and depending on you was successful or not you get to a win or lose screen.

## What I learned?
Before this project, I didn't deal with the OOP aspects of Python and any kind of UI stuff and I don't know the [Kivy](https://kivy.org) framework.
So mostly these were the most challenging parts of this project, Kivy is mostly well documented but I had a hard time to grasp some parts of the framework sometimes. The other was the OOP in Python like:
##### What is exactly the self part means, and why do you have to specify it as the first parameter in the method signature. 
```python
def do_something(self):
    ...
```
So I am happy with the results and I learned a lot from this project.


## Last but not least two gifs and the flow of the app
### Answer every question right 
![](https://github.com/AdamGonda/Dedicate/blob/master/win%20demo.gif)


### Run out of time 
![](https://github.com/AdamGonda/Dedicate/blob/master/time%20is%20up%20demo.gif)


### App flow
![](https://github.com/AdamGonda/Dedicate/blob/master/flow.png)
