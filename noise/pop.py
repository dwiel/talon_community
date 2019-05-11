from talon import ctrl
from talon.audio import noise

class NoiseModel:
    def __init__(self):
        self.button = 0

        noise.register('noise', self.on_noise)

    def on_noise(self, noise):
        if noise == 'pop':
            ctrl.mouse_click(button=0, hold=16000)

model = NoiseModel()