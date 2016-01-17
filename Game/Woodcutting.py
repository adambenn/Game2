import Skill

class woodcutting(Skill.skill):
    def __init__(self,owner,overlay):
        super().__init__('Woodcutting',owner,overlay,99)
        self.baseSpeed = 0.4
        self.chopSpeed = self.baseSpeed
        self.speedDecrease = -0.004

    def setLevel(self,lvl):
        super().setLevel(lvl)
        self.chopSpeed = self.baseSpeed + (lvl - 1) * self.speedDecrease
