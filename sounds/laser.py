import pygame
import numpy as np

def create_laser_sound():
    """Tạo âm thanh laser đơn giản và lưu thành file WAV"""
    pygame.mixer.init()
    sample_rate = 44100
    duration = 0.2  # 200ms
    
    # Tạo âm thanh laser đơn giản
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    frequency = np.linspace(1000, 500, int(sample_rate * duration))
    
    # Tạo sóng âm
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    # Chuyển đổi sang định dạng 16-bit
    wave = (wave * 32767).astype(np.int16)
    
    # Lưu thành file WAV
    pygame.sndarray.make_sound(wave).save("laser.wav")
    
if __name__ == "__main__":
    create_laser_sound()