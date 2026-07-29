import json


class Achievement:
    def __init__(self, name, description, is_unlocked=False):
        self.name = name
        self.description = description
        self.is_unlocked = is_unlocked

    def unlock(self):
        # Mark the achievement as unlocked with a specifc entry point
        self.is_unlocked = True

with open ("databases/achievements.json", "r") as f:
    achievement_data = json.load(f)

with open("databases/save_databases/unlocked_achievements.json", "r") as f:
    unlocked_achievement_data = json.load(f)

class AchievementManager:
    def __init__(self):
        self.achievements = []
        self.unlocked_achievements = []

    def load_achievements(self):
        for achievement in achievement_data:
            name = achievement["name"]
            description = achievement["description"]
            is_unlocked = name in unlocked_achievement_data
            self.achievements.append(Achievement(name, description, is_unlocked))

    def load_unlocked_achievements(self):
        for achievement in self.achievements:
            if achievement.is_unlocked:
                self.unlocked_achievements.append(achievement)

    def unlock_achievement(self, achievement_name):
        for achievement in self.achievements:
            if achievement.name == achievement_name and achievement not in self.unlocked_achievements:
                achievement.unlock()
                self.unlocked_achievements.append(achievement)
                with open("databases/save_databases/unlocked_achievements.json", "w") as f:
                    json.dump([a.name for a in self.unlocked_achievements], f)