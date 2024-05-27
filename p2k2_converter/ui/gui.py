import os
os.environ["KIVY_NO_ARGS"] = "1"

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup


from pathlib import Path


Builder.load_string('''
<FileList>:
    viewclass: 'Label'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')


class FileList(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []

    def add_file(self, file_path):
        self.data.append({"text": str(file_path)})

    @property
    def files(self):
        return [Path(item["text"]) for item in self.data]


def open_filechooser(
        on_select,
        title="Seleziona un file",
        action_name="Seleziona",
        dir_choosable: bool = False,
        filters = ['*.*'],
        root_path = None,):
    if root_path is None:
        root_path = Path.home()

    popup = Popup(title=title, size_hint=(0.9, 0.9))
    layout = BoxLayout(orientation='vertical')
    filechooser = FileChooserIconView(
        dirselect=dir_choosable,
        path=str(root_path),
        filters=filters,
    )
    def on_press(instance):
        on_select([Path(file) for file in filechooser.selection])
        popup.dismiss()
    select_button = Button(text=action_name,on_press=on_press)
    layout.add_widget(filechooser)
    layout.add_widget(select_button)
    popup.content = layout
    popup.open()


class FileProcessingApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._last_destination = None
        self._last_folder = None

    def build(self):
        # Layout
        layout = BoxLayout(orientation="vertical")

        # File list view
        self.file_list = FileList()

        # Text box and button for destination folder selection
        destination_row = BoxLayout(orientation="horizontal")
        self.destination_text = TextInput(hint_text="Cartella lavorazioni")
        select_dest_button = Button(text="...", on_press=self.select_destination)
        destination_row.add_widget(self.destination_text)
        destination_row.add_widget(select_dest_button)

        # Buttons for adding files and processing
        buttons_row = BoxLayout(orientation="horizontal")
        add_files_button = Button(text="Aggiungi file", on_press=self.open_filechooser)
        process_button = Button(text="Genera lavorazioni", on_press=self.process_files)
        buttons_row.add_widget(add_files_button)
        buttons_row.add_widget(process_button)

        # Add widgets to layout
        layout.add_widget(self.file_list)
        layout.add_widget(destination_row)
        layout.add_widget(buttons_row)

        return layout

    def select_destination(self, instance):
        open_filechooser(
            title="Seleziona cartella lavorazioni:",
            on_select=self.update_destination_text,
            dir_choosable=True,
            filters=['dirs'],
            root_path=self._last_destination,
        )

    def update_destination_text(self, values):
        dir = values[0] if values else ""
        self.destination_text.text = str(dir)
        self._last_destination = dir

    def open_filechooser(self, instance):
        open_filechooser(
            title="Seleziona file barriere:",
            on_select=self.add_file,
            dir_choosable=False,
            filters=['*.xls', '*.xlsm'],
            root_path=self._last_folder,
        )

    def add_file(self, file_paths):
        for path in file_paths:
            self.file_list.add_file(path)
            self._last_folder = path.parent

    def process_files(self, instance):
        # Implement your processing logic here using the selected files and destination folder
        # (Access file paths from self.file_list.selection and destination from self.destination_text.text)
        print("Processing files:", self.file_list.files)
        print("Destination folder:", self.destination_text.text)


def run_gui(args):
    FileProcessingApp().run()
