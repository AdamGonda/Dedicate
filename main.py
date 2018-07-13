from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.properties import StringProperty, ListProperty, BooleanProperty
import time
import random as r


Builder.load_file("myKivyFile.kv")


class CountDown():
    def __init__(self):
        self.start_time = 0
        self.set_time = 0

    def start(self, set_time):
        self.set_time = set_time
        self.start_time = time.time()

    def reset(self):
        self.start_time = 0

    def get_time(self):
        return self.set_time - int(time.time() - self.start_time + 1)


class QAScreen(Screen):
    # this class has to manage a questions from a given collection
    def __init__(self):
        Screen.__init__(self)
        self.name = "QA"
        self.timer = CountDown()
        self.questions = None
        self.question_index = 0
        self.initial_timer_time = 30
        self.is_game_started = False
        self.is_game_over = False
        self.lives = 3
        
    time_prop = StringProperty("30")
    questions_prop = ListProperty(["Question", "A1", "A2", "A3", "A4"])
    lives_prop = StringProperty("3")
    
    def load_set(self, file_name):
        with open(file_name, "r") as file:
            contents = file.readlines()
            contents = [item.replace("\n", "") for item in contents]
            contents = [item.split(",") for item in contents]
            rSet = []

            for q_and_as in contents:
                question_structure = []
                for i in range(len(q_and_as)):
                    if i == 0:
                        question_structure.append(q_and_as[i])
                    elif i == 1:
                        answer = [q_and_as[i].strip(' '), True]
                        question_structure.append(answer)
                    else:
                        answer = [q_and_as[i].strip(' '), False]
                        question_structure.append(answer)

                rSet.append(question_structure)

            return rSet  

    def on_check_answer(self, instance):
        if self.is_game_started and not self.is_game_over:
            current_question_set = self.questions[self.question_index]

            for i in range(1, len(current_question_set)):

                if current_question_set[i][0] == instance.text:
                    if current_question_set[i][1]:
                        
                        # go to next question if it is possible
                        if self.question_index < len(self.questions) - 1:

                            self.question_index += 1
                            self.set_question_and_answers()

                        else:
                            self.win()
                    else:
                        # decrease lives
                        if self.lives > 1:
                            self.lives -= 1
                            # update lives_prop
                            self.lives_prop = str(self.lives)
                        else:
                            self.game_over()

    def win(self):
        Logger.info(self.manager.current)
        self.manager.current = 'WIN'
        

    def game_over(self):
        self.is_game_over = True
        self.is_game_started = False
        self.manager.current = "LOSE"

    def set_question_and_answers(self, *args):
        # choose from answers randomly
        self.questions_prop[0] = self.questions[self.question_index][0]
        av_q = [1, 2, 3, 4]
        for i in range(1, 5):
            random_index = r.randint(0, len(av_q) - 1)
            self.questions_prop[i] = self.questions[self.question_index][av_q[random_index]][0]
            av_q.pop(random_index)

    def on_start(self):
        if not self.is_game_started:

            # Set state variables
            self.is_game_started = True
            self.is_game_over = False
            # Start a clock
            self.timer.reset()
            self.timer.start(self.initial_timer_time)
            self.time_prop = str(self.timer.get_time())
            Clock.schedule_interval(self.update_clock, 1.0/60.0)
            # Load and set questions and answers
            self.questions = self.load_set("test_collection.txt")
            self.load_set("test_collection.txt")
            self.set_question_and_answers()

        else:
            pass
    
    def update_clock(self, dt):
        if int(self.time_prop) == 0:
            self.game_over()
            return False
        elif self.is_game_over:
            return False
        else:
            self.time_prop = str(self.timer.get_time())

class WinScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.name = "WIN"

class LoseScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.name = "LOSE"

class MainScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.name = "MAIN"
    

class MyApp(App):
    def build(self):
        screen_manager = ScreenManager()

        
        
        screen_manager.add_widget(MainScreen())
        screen_manager.add_widget(QAScreen())
        screen_manager.add_widget(WinScreen())
        screen_manager.add_widget(LoseScreen())
        
        return screen_manager
        

if __name__ == '__main__':
    MyApp().run()