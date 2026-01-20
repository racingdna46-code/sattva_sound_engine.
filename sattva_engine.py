import numpy as np
import sounddevice as sd
import time

class SattvaSoundEngine:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.stream = None

    def generate_sine_wave(self, frequency, duration, volume=0.5):
        """Generates a pure sine wave for Solfeggio frequencies."""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        wave = np.sin(2 * np.pi * frequency * t) * volume
        return wave

    def generate_binaural_beat(self, carrier_freq, beat_freq, duration, volume=0.5):
        """
        Generates a binaural beat.
        carrier_freq: The base tone (e.g., 200Hz)
        beat_freq: The target brainwave (e.g., 40Hz for Gamma)
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        
        # Left ear: Carrier - (Beat/2)
        # Right ear: Carrier + (Beat/2)
        left_side = np.sin(2 * np.pi * (carrier_freq - beat_freq / 2) * t) * volume
        right_side = np.sin(2 * np.pi * (carrier_freq + beat_freq / 2) * t) * volume
        
        # Stack into a stereo array
        return np.column_stack((left_side, right_side))

    def play_preset(self, solfeggio_freq, brainwave_freq, duration=60):
        """
        Layers a Solfeggio grounding tone with a Binaural brainwave.
        Example: 852Hz (Stop Overthinking) + 40Hz (Gamma Focus)
        """
        print(f"ALGORITHM: Layering {solfeggio_freq}Hz with {brainwave_freq}Hz for ADHD relief...")
        
        # Generate the two layers
        grounding = self.generate_sine_wave(solfeggio_freq, duration, volume=0.3)
        # Convert mono grounding to stereo
        grounding_stereo = np.column_stack((grounding, grounding))
        
        entrainment = self.generate_binaural_beat(200, brainwave_freq, duration, volume=0.4)
        
        # Mix the layers
        mixed_audio = grounding_stereo + entrainment
        
        # Play the audio
        sd.play(mixed_audio, self.sample_rate)
        sd.wait()

# Initialize Engine
engine = SattvaSoundEngine()

# PRESET: THE BREAKTHROUGH (396Hz to stop shame + 18Hz Beta for momentum)
engine.play_preset(396, 18, duration=30)

# PRESET: THE OVERTHINKING STOPPER (852Hz + 40Hz Gamma)
# engine.play_preset(852, 40, duration=30)
