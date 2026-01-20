import numpy as np
try:
    import sounddevice as sd
except ImportError:
    sd = None
import threading

# Configuration
SAMPLE_RATE = 44100
AMPLITUDE = 0.5

class SattvaEngine:
    def __init__(self):
        self.stream = None
        self.is_playing = False
        self.thread = None

    def _generate_wave(self, carrier_hz, beat_hz, duration_sec):
        """
        Generates a stereo signal:
        Left Ear: Carrier
        Right Ear: Carrier + Beat
        """
        t = np.linspace(0, duration_sec, int(SAMPLE_RATE * duration_sec), False)
        
        # Carrier (Solfeggio)
        # Using pure sine waves
        left_channel = AMPLITUDE * np.sin(2 * np.pi * carrier_hz * t)
        
        # Carrier + Beat (Binaural)
        right_channel = AMPLITUDE * np.sin(2 * np.pi * (carrier_hz + beat_hz) * t)
        
        # Combine into stereo
        stereo_signal = np.column_stack((left_channel, right_channel))
        
        # Fade in/out to prevent clicking
        fade_duration = 0.1 # seconds
        fade_samples = int(fade_duration * SAMPLE_RATE)
        if len(t) > 2 * fade_samples:
             fade_in = np.linspace(0, 1, fade_samples)
             fade_out = np.linspace(1, 0, fade_samples)
             # Apply to both channels
             stereo_signal[:fade_samples, 0] *= fade_in
             stereo_signal[:fade_samples, 1] *= fade_in
             stereo_signal[-fade_samples:, 0] *= fade_out
             stereo_signal[-fade_samples:, 1] *= fade_out
             
        return stereo_signal.astype(np.float32)

    def play_frequency(self, carrier_hz, beat_hz, duration_sec=60):
        """
        Stops any current stream and plays the new frequency combination.
        Non-blocking.
        """
        self.stop_audio()
        
        wave = self._generate_wave(carrier_hz, beat_hz, duration_sec)
        
       if sd:
            try:
               self.thread = threading.Thread(target=lambda: sd.play(wave, SAMPLE_RATE, blocking=True))
               self.thread.start()
               self.is_playing = True
            except Exception as e:
                print(f"Audio Error: {e}")
       else:
           print("Audio device not available (Android/Missing Lib)")

    def stop_audio(self):
        """Force stops all audio."""
        try:
            if sd:
                sd.stop()
        except:
            pass
        self.is_playing = False

# Global Instance
engine = SattvaEngine()
