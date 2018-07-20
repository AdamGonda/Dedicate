from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.properties import StringProperty, ListProperty, BooleanProperty
import time
import random as r
import os


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
    # this class has to manage a questions and answers from a given collection
    def __init__(self):
        Screen.__init__(self)
        self.name = "QAScreen"
        self.winScreen = "WinScreen"
        self.loseScreen = "LoseScreen"
        self.timer = CountDown()
        self.questions = None
        self.question_index = -1
        self.initial_timer_time = 30
        self.is_game_started = False
        self.is_game_over = False
        self.is_exit_timer = False
        self.lives = 3
        self.default_collecton_folder = "collections"
        self.selected_collection = None
        self.default_questions_prop_values = ["Question", "A1", "A2", "A3", "A4"]
        
    time_prop = StringProperty("30")
    questions_prop = ListProperty(["Question", "A1", "A2", "A3", "A4"])
    lives_prop = StringProperty("3")

    def reset_screen(self):
        self.questions = None
        self.question_index = -1
        self.initial_timer_time = 30
        self.lives = 3
        self.is_game_started = False
        self.is_game_over = False
        self.is_exit_timer = True
        self.time_prop = str(self.initial_timer_time)
        for i in range(len(self.questions_prop)):
            self.questions_prop[i] = self.default_questions_prop_values[i]
        self.lives_prop = str(self.lives)
        
    def load_collection(self, file_name):
        with open(file_name, "r") as file:
            contents = file.readlines()
            contents = [item.replace("\n", "") for item in contents]
            contents = [item.split(",") for item in contents]
            collection = []

            for q_and_as in contents:
                question_and_answers = []
                for i in range(len(q_and_as)):
                    if i == 0:
                        question_and_answers.append(q_and_as[i])
                    elif i == 1:
                        answer = [q_and_as[i].strip(' '), True]
                        question_and_answers.append(answer)
                    else:
                        answer = [q_and_as[i].strip(' '), False]
                        question_and_answers.append(answer)

                collection.append(question_and_answers)

            return collection  

    def on_check_answer(self, btn):
        
        if self.is_game_started and not self.is_game_over:
            current_q_and_a = self.questions[self.question_index]

            for i in range(1, len(current_q_and_a)):

                answer = current_q_and_a[i][0]
                answer_value = current_q_and_a[i][1]
                
                if answer == btn.text and answer_value:
                    
                    # go to next question if it is possible
                    if self.question_index < len(self.questions) - 1:
                        self.update_question()
                    else:
                        self.win()
                    break
                else:
                    Logger.info("Lives: "+str(self.lives))
                    # decrease lives
                    if self.lives > 1:
                        self.lives -= 1
                        # update lives_prop
                        self.lives_prop = str(self.lives)
                    else:
                        self.game_over()
                    break

    def win(self):
        self.manager.current = self.winScreen
        
    def game_over(self):
        self.is_game_over = True
        self.is_game_started = False
        self.manager.current = self.loseScreen

    def update_question(self, *args):
        self.question_index += 1
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
            self.is_exit_timer = False
            # Start a clock
            self.timer.reset()
            self.timer.start(self.initial_timer_time)
            self.time_prop = str(self.timer.get_time())
            Clock.schedule_interval(self.update_clock, 1.0/60.0)
            # Load and set questions and answers
            self.questions = self.load_collection(self.default_collecton_folder + "/" + self.selected_collection)
            self.update_question()
        else:
            pass
    
    def update_clock(self, dt):
        if int(self.time_prop) == 0:
            self.game_over()
            return False
        elif self.is_game_over or self.is_exit_timer:
            return False
        else:
            self.time_prop = str(self.timer.get_time())


class WinScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.name = "WinScreen"


class LoseScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.name = "LoseScreen"


class MainScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.name = "MainScreen"


class CollectionSelectScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.name = "CollectionSelectScreen"
        self.default_collecton_folder = "./collections"
        self.collections = []
        self.load_collections()
        self.initialize_collecion_buttons()

    def load_collections(self):
        if os.path.isdir(self.default_collecton_folder):
            self.collections = sorted(os.listdir(self.default_collecton_folder))

    def initialize_collecion_buttons(self):
        box_layout = BoxLayout(orientation="vertical")
        for i in range(len(self.collections)):
            btn = Button(text=self.collections[i])
            btn.bind(on_press=self.on_select)
            box_layout.add_widget(btn)

        self.add_widget(box_layout)

    def on_select(self, btn):
        self.manager.get_screen("QAScreen").selected_collection = btn.text
        self.manager.get_screen("QAScreen").reset_screen()
        self.manager.current = "QAScreen"
            




class MyApp(App):
    def build(self):
        screen_manager = ScreenManager()

        screen_manager.add_widget(MainScreen())
        screen_manager.add_widget(CollectionSelectScreen())
        screen_manager.add_widget(QAScreen())
        screen_manager.add_widget(WinScreen())
        screen_manager.add_widget(LoseScreen())
        
        return screen_manager
        

if __name__ == '__main__':
    MyApp().run()