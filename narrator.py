import os
from pathlib import Path
import win32com.client
import time
import win32com.client
#from ollama_llm import make_slide_narration
from gemini_llm import make_slide_narration
from hume_voice import speak_hume

def ensure_dir(p):
    Path(p).mkdir(parents=True, exist_ok=True)

class PPTController:
    def __init__(self, ppt_path: str):
        self.ppt_path = ppt_path
        self.app = None
        self.pres = None

    def open(self):
        self.app = win32com.client.Dispatch("PowerPoint.Application")
        self.app.Visible = True

        #self.pres = self.app.Presentations.Open(self.ppt_path)
        self.pres = self.app.Presentations.Open(self.ppt_path, WithWindow=True)

        # Start slideshow
        self.pres.SlideShowSettings.Run()

        # ✅ wait until slideshow window exists
        for _ in range(30):
            try:
                if self.app.SlideShowWindows.Count > 0:
                    return
            except Exception:
                pass
            time.sleep(0.2)

        raise RuntimeError("SlideShowWindow did not start. Please start slideshow manually once and retry.")

    def _view(self):
        # ✅ always get active slideshow view
        return self.app.SlideShowWindows(1).View

    def goto_slide(self, n: int):
        self._view().GotoSlide(n)

    def next_slide(self):
        self._view().Next()

    def prev_slide(self):
        self._view().Previous()

    def close(self):
        try:
            if self.pres:
                self.pres.Close()
        except:
            pass
        try:
            if self.app:
                self.app.Quit()
        except:
            pass

def run_presentation(slides, hume_key: str, out_dir: str, ppt_path: str):
    scripts_dir = os.path.join(out_dir, "scripts")
    ensure_dir(scripts_dir)

    ppt = PPTController(ppt_path)
    ppt.open()

    speak_hume(hume_key, "Hello everyone. I will be presenting this deck today on behalf of Akhilesh.")

    for s in slides:
        slide_no = s["slide_no"]
        script_path = os.path.join(scripts_dir, f"slide_{slide_no:03}.txt")

        # show current slide
        ppt.goto_slide(slide_no)
        #ppt.next_slide()

        # narration text
        if os.path.exists(script_path):
            narration = open(script_path, "r", encoding="utf-8").read().strip()
        else:
            #narration = make_slide_narration(ollama_model, s["context"])
            narration = make_slide_narration(s["context"])
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(narration)

        # speak narration
        speak_hume(hume_key, narration)

        # go next slide automatically
        ppt.next_slide()

    speak_hume(hume_key, "That concludes the presentation. Happy to take any questions.")
