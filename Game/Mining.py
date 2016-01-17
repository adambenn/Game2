import Skill

class mining(Skill.skill):
    def __init__(self,owner,overlay):
        super().__init__('Mining',owner,overlay,99)
        self.baseSpeed = 0.4
        self.mineSpeed = self.baseSpeed
        self.speedDecrease = -0.004

    def setLevel(self,lvl):
        super().setLevel(lvl)
        self.mineSpeed = self.baseSpeed + (lvl - 1) * self.speedDecrease
