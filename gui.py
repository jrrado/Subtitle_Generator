from tkinter import Tk, filedialog, Label, Button, Entry, StringVar, DISABLED, NORMAL,messagebox
from subtitle_generator import extract_audio, generate_subtitles,translate_subtitles
#extract_audio, generate_subtitles, translate_subtitles

class SubtitleGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Subtitle Generator and Translator")

        self.video_path = StringVar()
        self.audio_path = StringVar()
        self.subtitle_path = StringVar()
        self.src_lang = StringVar(value="en")
        self.tgt_lang = StringVar(value="fr")
        self.language = StringVar(value="en-US")  # Language for speech-to-text

        # UI elements
        self.video_label = Label(master, text="Video Path:")
        self.video_label.grid(row=0, column=0)
        self.video_entry = Entry(master, textvariable=self.video_path, width=50, state=DISABLED)
        self.video_entry.grid(row=0, column=1)
        self.browse_video_button = Button(master, text="Browse", command=self.browse_video)
        self.browse_video_button.grid(row=0, column=2)

        self.audio_label = Label(master, text="Audio Path:")
        self.audio_label.grid(row=1, column=0)
        self.audio_entry = Entry(master, textvariable=self.audio_path, width=50, state=DISABLED)
        self.audio_entry.grid(row=1, column=1)

        self.subtitle_label = Label(master, text="Subtitle Path:")
        self.subtitle_label.grid(row=2, column=0)
        self.subtitle_entry = Entry(master, textvariable=self.subtitle_path, width=50, state=DISABLED)
        self.subtitle_entry.grid(row=2, column=1)

        self.source_lang_label = Label(master, text="Source Language:")
        self.source_lang_label.grid(row=3, column=0)
        self.source_lang_entry = Entry(master, textvariable=self.src_lang, width=10)
        self.source_lang_entry.grid(row=3, column=1)

        self.target_lang_label = Label(master, text="Target Language:")
        self.target_lang_label.grid(row=4, column=0)
        self.target_lang_entry = Entry(master, textvariable=self.tgt_lang, width=10)
        self.target_lang_entry.grid(row=4, column=1)

        self.language_label = Label(master, text="Speech Language:")
        self.language_label.grid(row=5, column=0)
        self.language_entry = Entry(master, textvariable=self.language, width=10)
        self.language_entry.grid(row=5, column=1)

        self.generate_button = Button(master, text="Generate Subtitles", command=self.generate, state=DISABLED)
        self.generate_button.grid(row=6, columnspan=3)

    def browse_video(self):
        filename = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")])
        self.video_path.set(filename)
        self.audio_path.set(filename.replace(".mp4", ".wav"))  # Assuming audio is extracted as WAV
        self.update_button_states()

    def update_button_states(self):
        """Enables/Disables buttons based on video selection"""
        video_path = self.video_path.get()
        self.generate_button.config(state=NORMAL if video_path else DISABLED)

    def generate(self):
        try:
            video_path = self.video_path.get()
            audio_path = self.audio_path.get()
            src_lang = self.src_lang.get()
            tgt_lang = self.tgt_lang.get()
            language = self.language.get()

            extract_audio(video_path, audio_path)
            generate_subtitles(audio_path, "subtitles.srt", language=language)
            translate_subtitles("subtitles.srt", src_lang, tgt_lang)

            messagebox.showinfo("Success", "Subtitle generation and translation completed!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = SubtitleGeneratorApp(root)
    root.mainloop()
