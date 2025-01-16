from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect

import four_digits_game


class FDGApp(App):
    def __init__(self):
        super(FDGApp, self).__init__()

        scale = Window.dpi / 96
        Window.size = (600 / scale, 1200 / scale)

        self.numbers = 4
        self.input_holders = [-1] * (self.numbers)
        self.answer = []
        self.input_pos = 0
        self.is_win = False
        self.attempt = 0

        self.input_areas = []
        for _ in range(self.numbers):
            self.input_areas.append(Label(text="", font_size=32))

        self.fdgame_instance = four_digits_game.FourDigitsGame(self.numbers)
        self.generated_numbers = self.fdgame_instance.generate()
        
        print(self.generated_numbers)


    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        top_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10, size_hint_y=0.08)

        self.reset_button = Button(text="Reset", height=50, on_press=self.on_new_game, font_size=28)
        self.give_up_button = Button(text="Give up", height=50, on_press=self.give_up, font_size=28)
        self.give_up_button.background_color = (1, 1, 1, 1)
        top_layout.add_widget(self.reset_button)
        top_layout.add_widget(self.give_up_button)

        main_layout.add_widget(top_layout)

        self.history_layout = ScrollView(size_hint=(1, 1), size_hint_y=0.47)
        self.history_layout.effect_x = ScrollEffect()
        self.history_layout.effect_y = ScrollEffect()

        self.init_scroll_box()

        main_layout.add_widget(self.history_layout)


        bottom_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=0.45)

        control_layout = GridLayout(cols=3, padding=[0, 0, 0, 20], spacing=10, size_hint=(1, 0.2))

        self.clear_button = Button(text="Remove", font_size=28)
        self.clear_button.bind(on_press=self.on_clear)
        control_layout.add_widget(self.clear_button)

        input_layout = GridLayout(cols=4, padding=10, spacing=2, size_hint=(1, 1))
        for i in range(self.numbers):
            input_layout.add_widget(self.input_areas[i])
        control_layout.add_widget(input_layout)

        self.enter_button = Button(text="Enter", font_size=28)
        self.enter_button.bind(on_press=self.on_enter, on_release=self.on_enter_release)
        control_layout.add_widget(self.enter_button)

        bottom_layout.add_widget(control_layout)

        # Numpad
        self.numpad_layout = GridLayout(cols=3, spacing=10, size_hint=(1, 0.8))

        for i in range(1, 10):
            button = Button(text=str(i), font_size=28)
            button.bind(on_press=self.on_numpad_press)
            self.numpad_layout.add_widget(button)

        self.numpad_layout.add_widget(Button(background_color=[0, 0, 0, 0], background_normal='', text="", disabled=True))

        zero_button = Button(text="0", font_size=28)
        zero_button.bind(on_press=self.on_numpad_press)
        self.numpad_layout.add_widget(zero_button)

        bottom_layout.add_widget(self.numpad_layout)
        main_layout.add_widget(bottom_layout)
        return main_layout


    def set_enter_button_color(self, color):
        self.enter_button.background_color = color


    def update_input_areas(self):
        for i in range(self.numbers):
            if self.input_holders[i] == -1:
                self.input_areas[i].text = ""
            else:
                self.input_areas[i].text = f"{self.input_holders[i]}"
    

    def add_entry(self):
        entry_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        entry_container.add_widget(Label(text=f"Attempt: {self.attempt}", font_size=28))
        entry_container.add_widget(Label(text=f"{self.input_holders}", font_size=28))
        entry_container.add_widget(Label(text=f"{self.answer}", font_size=28))

        self.scroll_box.add_widget(entry_container)
    

    def init_scroll_box(self):
        self.scroll_box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.scroll_box.bind(minimum_height=self.scroll_box.setter('height'))
        
        self.history_layout.add_widget(self.scroll_box)
    

    def on_new_game(self, instance):
        self.new_game()


    def new_game(self):
        self.attempt = 0

        self.give_up_button.background_color = (1, 1, 1, 1)
        self.history_layout.clear_widgets()
        self.init_scroll_box()

        self.is_win = False
        self.clear_button.disabled = False
        self.enter_button.disabled = False
        self.give_up_button.disabled = False

        self.set_enter_button_color((1, 1, 1, 1))

        self.reset_button.text = "Reset"

        self.numpad_layout.disabled = False

        self.input_holders = [-1] * (self.numbers)
        self.update_input_areas()

        self.fdgame_instance.reset_numbers_pool()
        self.generated_numbers = self.fdgame_instance.generate()
        self.input_pos = 0
        print(self.generated_numbers)


    def give_up(self, instance):
        print(self.generated_numbers)
        self.give_up_button.background_color = (1, 0, 0, 1)
        self.win()


    def win(self):
        self.set_enter_button_color((0, 1, 0, 1))
        self.is_win = True
        self.clear_button.disabled = True
        self.enter_button.disabled = True
        self.give_up_button.disabled = True
        self.reset_button.text = "New Game"
        self.input_holders = self.generated_numbers
        self.update_input_areas()
        self.numpad_layout.disabled = True


    def on_numpad_press(self, instance):
        if self.input_pos <= self.numbers - 1:
            self.input_holders[self.input_pos] = int(instance.text)
            self.update_input_areas()
            self.input_pos += 1
        else:
            print("No change")


    def on_clear(self, instance):
        is_last = False
        if self.input_pos == self.numbers:
            self.input_pos -= 1
            is_last = True

        if self.input_holders[self.input_pos] == -1:
            if self.input_pos > 0:
                self.input_pos -= 1

            self.input_holders[self.input_pos] = -1
            self.update_input_areas()
        else:
            self.input_holders[self.input_pos] = -1
            self.update_input_areas()

            if self.input_pos > 0:
                self.input_pos -= 1
        
        if is_last:
            self.input_pos += 1


    def on_enter(self, instance):
        if -1 in self.input_holders:
            print("Nothing")
            return

        print(self.input_holders)

        if not self.fdgame_instance.check_identical(self.input_holders):
            self.attempt += 1
            print("Process")

            self.answer = self.fdgame_instance.process_guess(self.generated_numbers, self.input_holders)
            print(self.answer)

            self.add_entry()

            self.input_holders = [-1] * (self.numbers)
            self.update_input_areas()
            self.input_pos = 0

            if self.answer == [self.numbers, self.numbers]:
                self.win()
        else:
            self.set_enter_button_color((1, 0, 0, 1))
    

    def on_enter_release(self, instance):
        if not self.is_win:
            self.set_enter_button_color((1, 1, 1, 1))


if __name__ == "__main__":
    FDGApp().run()
