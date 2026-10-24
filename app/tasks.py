"""Five culturally localized, repeatable study tasks."""

TASKS = [
    {"id": "weather_lahore", "urdu": "لاہور میں آج کا موسم چیک کریں", "english": "Check today's weather in Lahore", "expected_state_change": {"weather": "Lahore: Sunny, 28°C (simulated)"}, "command": "check weather in Lahore"},
    {"id": "tea_timer_5", "urdu": "چائے کے لیے ۵ منٹ کا ٹائمر لگائیں", "english": "Set a 5-minute timer for tea", "expected_state_change": {"timer": "5 minutes"}, "command": "set timer for 5 minutes"},
    {"id": "light_blue", "urdu": "بتی کو نیلا رنگ دیں", "english": "Set the light to blue", "expected_state_change": {"light": "on", "light_color": "blue"}, "command": "set light color to blue"},
    {"id": "biryani_recipe", "urdu": "بریانی کی ترکیب دکھائیں", "english": "Show a biryani recipe", "expected_state_change": {"recipe": "Biryani recipe displayed"}, "command": "show biryani recipe"},
    {"id": "fajr_reminder", "urdu": "فجر کے لیے یاد دہانی لگائیں", "english": "Set a Fajr prayer reminder", "expected_state_change": {"reminder": "Fajr"}, "command": "set Fajr reminder"},
]

LOCALIZED_TASKS = TASKS
