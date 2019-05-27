from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.core.window import Window
import time
import random as r
import os


Builder.load_file("myKivyFile.kv")


class CountDown():
    def start(self, set_time):
        self.count_from = set_time
        self.start_time = time.time()

    def get_time(self):
        return self.count_from - int(time.time() - self.start_time)


class AnswerButton(Button):
    def __init__(self, **kw):
        super(AnswerButton, self).__init__(**kw)
    answer_value = BooleanProperty(False)

    def on_press(self):
        if self.answer_value:
            self.background_normal = "btn_good.png"
        else:
            self.background_normal = "btn_wrong.png"

    def reset_color(self):
        self.background_normal = "btn_normal.png"


class QAScreen(Screen):
    # this class has to manage the questions and answers from a given collection
    TIMER_TIME = 10
    Q_AND_A_VALUES = ["Question", "A1", "A2", "A3", "A4"]
    COLLECTIONS_FOLDER = "collections"
    FILE_EXTENSION = ".txt"
    TRANSITION_TIME_BETWEEN_QUESTIONS = 1

    def __init__(self, **kw):
        super(QAScreen, self).__init__(**kw)

        self.name = "QAScreen"
        self.winScreen = "WinScreen"
        self.loseScreen = "LoseScreen"
        self.timer = CountDown()
        self.selected_collection = None
        self.lives = 3

        self.questions = None
        self.question_index = -1

        self.is_game_started = False
        self.is_game_over = False
        self.is_exit_timer = False
        
    time_prop = StringProperty("")
    currant_q_and_a = ListProperty(["Question", "A1", "A2", "A3", "A4"])
    lives_prop = StringProperty("3")

    def reset_btn_colors(self):
        for i in range(4):
            self.ids["A"+str(i+1)].reset_color()

    def set_is_exit_timer(self):
        self.is_exit_timer = True

    def set_to_default_currant_q_and_a(self):
        for i in range(len(self.currant_q_and_a)):
            self.currant_q_and_a[i] = self.Q_AND_A_VALUES[i]

    def reset_screen(self):
        self.questions = None
        self.question_index = -1
        self.lives = 3
        self.is_game_started = False
        self.is_game_over = False
        self.is_exit_timer = False
        self.time_prop = str(self.TIMER_TIME)
        self.set_to_default_currant_q_and_a()
        self.lives_prop = str(self.lives)
        self.reset_btn_colors()
        
    def load_collection(self, file_name):
        with open(file_name + self.FILE_EXTENSION, "r") as file:
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
            
            if btn.answer_value:    
                # go to next question if it is possible
                if self.question_index < len(self.questions) - 1:
                    Clock.schedule_once(lambda dt: self.update_q_and_a(), self.TRANSITION_TIME_BETWEEN_QUESTIONS)
                else:
                    self.is_exit_timer = True
                    Clock.schedule_once(lambda dt: self.win(), self.TRANSITION_TIME_BETWEEN_QUESTIONS)
                
            else:
                # decrease lives
                if self.lives > 1:
                    self.lives -= 1
                    # update lives_prop
                    self.lives_prop = str(self.lives)
                else:
                    Clock.schedule_once(lambda dt: self.game_over(), self.TRANSITION_TIME_BETWEEN_QUESTIONS)
                    
    def win(self):
        self.manager.current = self.winScreen
        
    def game_over(self):
        self.is_game_over = True
        self.is_game_started = False
        self.manager.current = self.loseScreen

    def update_q_and_a(self, *args):
        self.reset_btn_colors()

        self.question_index += 1

        answer = self.questions[self.question_index][0]
        self.currant_q_and_a[0] = answer

        # choose from answers randomly
        index_list = [1, 2, 3, 4]
        for i in range(1, 5):
            random_index = r.randint(0, len(index_list) - 1)

            question_text = self.questions[self.question_index][index_list[random_index]][0]
            question_value = self.questions[self.question_index][index_list[random_index]][1]

            self.currant_q_and_a[i] = question_text
            self.ids["A"+str(i)].answer_value = question_value

            index_list.pop(random_index)

    def on_start(self):
        if not self.is_game_started:
            # Set state variables
            self.is_game_started = True
            self.is_game_over = False
            self.is_exit_timer = False
            # Start a clock
            
            self.timer.start(self.TIMER_TIME)
            Clock.schedule_interval(self.update_clock, 1.0/60.0)
            # Load and set questions and answers
            self.questions = self.load_collection(self.COLLECTIONS_FOLDER + "/" + self.selected_collection)
            self.update_q_and_a()
    
    def update_clock(self, dt):
        if int(self.time_prop) == 0:
            self.game_over()
            return False
        elif self.is_game_over or self.is_exit_timer:
            return False
        else:
            self.time_prop = str(self.timer.get_time())


class WinScreen(Screen):
    def __init__(self, **kw):
        super(WinScreen, self).__init__(**kw)
        self.name = "WinScreen"


class LoseScreen(Screen):
    def __init__(self, **kw):
        super(LoseScreen, self).__init__(**kw)
        self.name = "LoseScreen"


class MainScreen(Screen):
    def __init__(self, **kw):
        super(MainScreen, self).__init__(**kw)
        self.name = "MainScreen"


class CollectionSelectScreen(Screen):
    COLLECTIONS_FOLDER = "./collections"

    def __init__(self, **kw):
        super(CollectionSelectScreen, self).__init__(**kw)
        self.name = "CollectionSelectScreen"
        self.collections = []
        
        self.load_collections()
        self.initialize_screen_layout()

    def load_collections(self):
        if os.path.isdir(self.COLLECTIONS_FOLDER):
            self.collections = sorted(os.listdir(self.COLLECTIONS_FOLDER))

    def initialize_screen_layout(self):
        box_layout = self.ids["btn_container"]
        for i in range(len(self.collections)):
            btn = Button(text=self.collections[i].replace(".txt", ''), background_normal="btn_normal.png", font_size=60)
            btn.bind(on_press=self.on_select)
            box_layout.add_widget(btn)

    def on_select(self, btn):
        self.manager.get_screen("QAScreen").selected_collection = btn.text
        self.manager.get_screen("QAScreen").reset_screen()
        self.manager.transition.direction = 'left'
        self.manager.current = "QAScreen"
    

class DedicateApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        screen_manager = ScreenManager()
        screen_manager.add_widget(MainScreen())
        screen_manager.add_widget(CollectionSelectScreen())
        screen_manager.add_widget(QAScreen())
        screen_manager.add_widget(WinScreen())
        screen_manager.add_widget(LoseScreen())
        
        return screen_manager
        

if __name__ == '__main__':
    DedicateApp().run()