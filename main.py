
__version__ = 'v0.5.0'
SOUND_DIR = './chars'


import os

from plyer import tts
import kivy
kivy.require('1.0.8')

from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup


RENAMED_CHAR = {
    '+' : 'plus',
    '-' : 'minus',
    '*' : 'times',
    '/' : 'slash',  # ambiguous with Math divide
    '=' : 'equals',
    '.' : 'dot',
    ',' : 'comma',
}


class TwiddleTalk(BoxLayout):
    """TwiddleTalk controller class."""

    textbox = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TwiddleTalk, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self.reset()

    def reset(self):
        """Restarts the Kivy application.

        When the app is suspended and later resumed, sometimes it would no longer play any sound.
        The workaround is to release all previously loaded resources and reload them.

        Parameters:
            none

        Returns:
            none
        """
        
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.textbox.text = ""
        #self.textbox.focus = True
        self._speakmode = 'SAY_LETTERS'
        self._current_word = ""

        if hasattr(self, '_sounds'):
            for key, player in self._sounds.items():
                player._sound.unload()

        # Load/Reload the sound files into memory.
        # MP3 files are smaller and preferred, but used WAV format for better cross-platform support.
        # For example, the MPEG-plugin for SoundPlayer did not work on Mac OS High Sierra.
        self._sounds = {}
        for f in os.listdir(SOUND_DIR):
            char = f.replace('.wav', '')
            self._sounds[char] = SoundPlayer(os.path.join(SOUND_DIR, f))

    def _on_keyboard_down(self, keyboard, keycode, char, modifiers):
        """Called whenever a new keystroke is received.

        Parameters:
            keyboard: Keyboard object
            keycode (int, str): Raw value and string represention. eg: (13, 'enter')
            char (str): ASCII representation
            modifiers (list): Keystroke modifiers such as 'shift'

        Returns:
            True -- to consume the keystroke. Otherwise it will be passed to the OS.
        """

        print(f"Keystroke: char={char}, code={keycode}, mods={modifiers}")
        if keycode[0] == 27:  # use the Escape key to toggle modes.
            self.toggle_speak_mode()
        elif self._speakmode == 'SAY_LETTERS':
            self.say_letter(keyboard, keycode, char, modifiers)
        else:
            self.say_word(keyboard, keycode, char, modifiers)
        return True

    def _keyboard_closed(self):
        """Called whenever a keyboard disconnect event is received from the OS."""
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def play_sound(self, char):
        """Plays the sound file of the given character.

        Parameters:
            char (str): The letter, number or special character to pronounce.

        Returns:
            none
        """

        player = self._sounds.get(char)
        if player:
            player.play()

    def speak(self, text):
        """Calls the speech synthesizer.

        Parameters:
            text (str): The text to be spoken.
            
        Returns:
            none
        """

        try:
            tts.speak(text)
        except NotImplementedError:
            popup = Popup(title='TTS Not Implemented',
                          content=Label(text='Sorry. TTS is not available.'),
                          size_hint=(None, None),
                          size=(300, 300))
            popup.open()

    def toggle_speak_mode(self):
        if self._speakmode == 'SAY_LETTERS':
          self._speakmode = 'SAY_WORDS'
        else:
          self._speakmode = 'SAY_LETTERS'
        self.play_sound(self._speakmode.lower())

    def say_letter(self, keyboard, keycode, char, modifiers):
        """Speaks the current character."""

        if keycode[1] in ('shift', 'rshift'):
            return  # ignore.. shifted keys will have their Shift modifier set
        elif keycode[1] == 'tab':
            self.play_sound('tab')
        elif keycode[1] == 'delete':
            self.play_sound('delete')
        elif keycode[1] == 'backspace':
            self.textbox.text = self.textbox.text[:-1]
            self.play_sound('backspace')
        elif keycode[1] == 'enter':
            self.textbox.text += '\n'
            self.play_sound('enter')
        elif char == ' ':
            self.textbox.text += ' '
            self.play_sound('space')      
        elif char is None:
            self.play_sound('error')
        else:
            if 'shift' in modifiers or 'rshift' in modifiers:
                self.textbox.text += char.upper()
            else:
                self.textbox.text += char
            if RENAMED_CHAR.get(char):
                self.play_sound(RENAMED_CHAR[char])
            else: 
                self.play_sound(char)

    def say_word(self, keyboard, keycode, char, modifiers):
        """Speaks word if complete, or adds the current character to word buffer."""

        if keycode[1] in ('shift', 'rshift'):
            return
        elif keycode[1] == 'backspace':
            self._current_word = self._current_word[:-1]
            self.textbox.text = self.textbox.text[:-1]
            return True
        elif keycode[1] == 'enter':
            char = '\n'

        if char in (' ', '\n', 'tab'):
            self.speak(self._current_word)
            self._current_word = ""
            self.textbox.text += char
        elif char is None:
            self.play_sound('error')
        else:
            if 'shift' in modifiers or 'rshift' in modifiers:
                char = char.upper()
            self._current_word += char
            self.textbox.text += char

    def exit(self):
        self.play_sound('exit')
        Clock.schedule_once(TwiddleTalkApp().stop, 1)  # allow audio to finish


class TwiddleTalkApp(App):
    """Boilerplate container for the Kivy application."""

    title = 'TwiddleTalk ' + __version__

    def build(self):
        return TwiddleTalk()

    def on_pause(self):
        return True

    def on_resume(self):
        pass


class SoundPlayer:
    """Wrapper to the Kivy SoundLoader class."""

    def __init__(self, audio_file):
        self._sound = SoundLoader.load(audio_file)

    def play(self):
        if self._sound.state != 'stop':  # abort previous utterance
            self._sound.stop()
        self._sound.play()


if __name__ == '__main__':
    TwiddleTalkApp().run()


