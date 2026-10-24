"""Stable Urdu labels and command translations used when the LLM is offline."""

COMMAND_TRANSLATIONS = {
    "turn on light": "بتی جلائیں",
    "turn off light": "بتی بند کریں",
    "set light color to blue": "بتی کا رنگ نیلا کریں",
    "set light color to red": "بتی کا رنگ سرخ کریں",
    "set light color to green": "بتی کا رنگ سبز کریں",
    "set timer for 5 minutes": "۵ منٹ کا ٹائمر لگائیں",
    "set timer for 10 minutes": "۱۰ منٹ کا ٹائمر لگائیں",
    "check weather in Lahore": "لاہور کا موسم دیکھیں",
    "show biryani recipe": "بریانی کی ترکیب دکھائیں",
    "set Fajr reminder": "فجر کے لیے یاد دہانی لگائیں",
    "show calendar": "کیلنڈر دکھائیں",
}

ACTION_VERBS_UR = ["روشن کریں", "بند کریں", "سیٹ کریں", "دکھائیں", "چیک کریں", "بدلیں", "یاد دہانی لگائیں", "مدد لیں"]
TASK_OPTIONS_UR = [
    "لاہور کا آج کا موسم دیکھیں", "چائے کے لیے ۵ منٹ کا ٹائمر لگائیں",
    "بتی کا رنگ نیلا کریں", "بریانی کی ترکیب دکھائیں",
    "فجر کے لیے یاد دہانی لگائیں", "کیلنڈر دکھائیں",
    "بتی جلائیں", "بتی بند کریں",
]
FOLLOWUP_OPTIONS_UR = ["۵ منٹ", "۱۰ منٹ", "۱۵ منٹ", "آج", "کل", "صبح", "شام", "منسوخ کریں"]

# Compatibility alias for callers that use the name in the implementation prompt.
TRANSLATIONS = COMMAND_TRANSLATIONS
