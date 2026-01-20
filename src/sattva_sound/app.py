import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, LEFT, RIGHT, TOP, BOTTOM
import asyncio
import time
from sattva_sound.sattva_engine import engine

class SattvaSoundApp(toga.App):
    def startup(self):
        # Window setup
        self.main_window = toga.MainWindow(title="Sattva Sound Pharmacy", size=(1000, 700))
        
        # Styles
        style_box_group = Pack(direction=COLUMN, padding=10, flex=1, background_color='#1E1E1E')
        style_header = Pack(text_align=CENTER, font_size=20, padding_bottom=10, color='white')
        style_button = Pack(padding=5, height=50, background_color='#2d2d2d', color='white') # Toga coloring is limited on some platforms but we try
        style_label = Pack(padding=5, color='#E0E0E0')
        
        # --- UI COMPONENTS ---
        
        # 1. Executive Momentum
        box_exec = toga.Box(style=style_box_group)
        box_exec.add(toga.Label("I. EXECUTIVE MOMENTUM", style=style_header))
        box_exec.add(toga.Button("STOP OVERTHINKING", on_press=self.on_stop_overthinking, style=style_button))
        box_exec.add(toga.Button("BREAK PARALYSIS", on_press=self.on_break_paralysis, style=style_button))
        box_exec.add(toga.Button("DEEP WORK", on_press=self.on_deep_work, style=style_button))

        # 2. Emotional Clearing
        box_emo = toga.Box(style=style_box_group)
        box_emo.add(toga.Label("II. EMOTIONAL CLEARING", style=style_header))
        box_emo.add(toga.Button("SHAME SPIRAL STOPPER", on_press=self.on_shame_stopper, style=style_button))
        box_emo.add(toga.Button("CORTISOL RESET", on_press=self.on_cortisol_reset, style=style_button))
        box_emo.add(toga.Button("FAILURE RESONANCE CLEAR", on_press=self.on_failure_clear, style=style_button))

        # 3. Physical Grounding
        box_phys = toga.Box(style=style_box_group)
        box_phys.add(toga.Label("III. PHYSICAL GROUNDING", style=style_header))
        box_phys.add(toga.Button("PANIC OVERRIDE", on_press=self.on_panic_override, style=style_button))
        box_phys.add(toga.Button("BIOLOGICAL RESTORATION", on_press=self.on_bio_restore, style=style_button))
        box_phys.add(toga.Button("NEURAL DRAINAGE", on_press=self.on_neural_drainage, style=style_button))

        # Grid Layout
        self.grid_box = toga.Box(style=Pack(direction=ROW, padding=10, background_color='#0E1117', flex=1))
        self.grid_box.add(box_exec)
        self.grid_box.add(box_emo)
        self.grid_box.add(box_phys)

        # Active State Section (Initially Hidden-ish or updated)
        self.lbl_active_title = toga.Label("READY", style=Pack(text_align=CENTER, font_size=24, color='#00FF99', padding_top=20))
        self.lbl_timer = toga.Label("", style=Pack(text_align=CENTER, font_size=60, color='white'))
        self.lbl_instructions = toga.Label("Select a protocol to begin.", style=Pack(text_align=CENTER, font_size=16, color='#AAAAAA'))
        self.btn_stop = toga.Button("STOP SESSION", on_press=self.stop_session, style=Pack(padding=10, background_color='red', width=200))
        
        self.active_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER, padding=20, background_color='#111111', flex=0))
        self.active_box.add(self.lbl_active_title)
        self.active_box.add(self.lbl_instructions)
        self.active_box.add(self.lbl_timer)
        self.active_box.add(self.btn_stop)

        # Main Layout
        self.main_box = toga.Box(style=Pack(direction=COLUMN, background_color='#0E1117'))
        self.main_box.add(toga.Label("S A T T V A  |  L O C A L", style=Pack(text_align=CENTER, font_size=30, padding=20, color='white')))
        self.main_box.add(self.grid_box)
        self.main_box.add(self.active_box)

        self.main_window.content = self.main_box
        self.main_window.show()

        # State
        self.is_active = False
        self.end_time = 0

    # --- ACTION HANDLERS ---
    def start_therapy(self, label, carrier, beat, instruction):
        engine.play_frequency(carrier, beat)
        self.is_active = True
        self.end_time = time.time() + 60
        
        self.lbl_active_title.text = f"ACTIVE: {label}"
        self.lbl_instructions.text = instruction
        
        # Start timer loop
        self.add_background_task(self.timer_loop)

    async def timer_loop(self, app):
        while self.is_active:
            remaining = int(self.end_time - time.time())
            if remaining <= 0:
                self.stop_session(None)
                break
            self.lbl_timer.text = str(remaining)
            await asyncio.sleep(1) # Standard async sleep for Toga loop
    
    def stop_session(self, widget):
        engine.stop_audio()
        self.is_active = False
        self.lbl_active_title.text = "SESSION COMPLETE"
        self.lbl_timer.text = "0"
        self.lbl_instructions.text = "Audio stopped."

    # --- BUTTON CALLBACKS ---
    def on_stop_overthinking(self, widget):
        self.start_therapy("STOP OVERTHINKING", 852, 40, "YINTANG POINT: Tap gently between your eyebrows.")

    def on_break_paralysis(self, widget):
        self.start_therapy("BREAK PARALYSIS", 396, 18, "THILARTHA VARMAM: Press firmly on the mid-forehead point.")

    def on_deep_work(self, widget):
        self.start_therapy("DEEP WORK", 741, 40, "TEMPLES: Massage both temples in slow circles.")

    def on_shame_stopper(self, widget):
        self.start_therapy("SHAME SPIRAL STOPPER", 396, 10, "THILARTHA RESET: Press mid-forehead. Inhale 4s, Hold 4s, Exhale 4s.")

    def on_cortisol_reset(self, widget):
        self.start_therapy("CORTISOL RESET", 528, 5, "MAMMALIAN DIVE REFLEX: Splash cold water on face or hold ice pack.")

    def on_failure_clear(self, widget):
        self.start_therapy("FAILURE RESONANCE CLEAR", 417, 10, "YINTANG POINT: Tap rhythmically between eyebrows.")

    def on_panic_override(self, widget):
        self.start_therapy("PANIC OVERRIDE", 174, 3, "MAMMALIAN DIVE REFLEX: Splash cold water on face. Hold breath for 10s.")

    def on_bio_restore(self, widget):
        self.start_therapy("BIOLOGICAL RESTORATION", 285, 5, "THILARTHA VARMAM: Gentle sustained pressure on mid-forehead.")

    def on_neural_drainage(self, widget):
        self.start_therapy("NEURAL DRAINAGE", 963, 2, "YINTANG POINT: Light touch between eyebrows. Close eyes. Visualize white light.")

def main():
    return SattvaSoundApp()
