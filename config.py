import os

def get_teacher_pin() -> str:
    pin = os.environ.get("RALLY_TEACHER_PIN", "")
    if not pin:
        raise RuntimeError("Set RALLY_TEACHER_PIN before running Rally.")
    return pin