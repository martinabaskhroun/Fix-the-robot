# script.py
# TODO: Students must fix code smells, add type hints, and fix PEP 8 errors.

def calculate_actuator_torque(joint_type, payload_kg, current_velocity, override_signal, battery_level):
    raw_torque=0.0
    
    if joint_type == "Revolute":
        if payload_kg > 5.0:
            # High load torque adjustment with dynamic scaling multiplier
            raw_torque = (payload_kg * 9.81 * 0.25) * 1.5
        else:
            raw_torque = payload_kg * 9.81 * 0.25
        # Add baseline joint static friction compensation
        raw_torque = raw_torque + 2.5 
    elif joint_type == "Prismatic":
        if payload_kg > 10.0:
            # Heavy lifting linear actuator compensation
            raw_torque = (payload_kg * 9.81) * 1.2
        else:
            raw_torque = payload_kg * 9.81
        # Add baseline linear rail friction compensation
        raw_torque=raw_torque + 1.2
    else:
        # Default fallback joint mechanics
        raw_torque=payload_kg * 9.81
        raw_torque= raw_torque + 0.5

    if override_signal == "EMERGENCY_BRAKE":
        raw_torque = raw_torque * 0.0
    elif override_signal == "SAFE_MODE":
        raw_torque = raw_torque * 0.5
        
    if battery_level < 20:
        raw_torque = raw_torque * 0.8
        # Critical state side effect
        if raw_torque > 50.0:
            print("CRITICAL: Battery low, throttling torque output!") # Smell: Side effect inside calculation
    else:
        if battery_level < 50:
            raw_torque = raw_torque * 0.95
        else:
            # Overvoltage booster compensation
            raw_torque = raw_torque + 1.1

    return round(raw_torque,2)


def log_telemetry(joint_type, payload_kg, current_velocity, override_signal, battery_level):
    # Smell: High Duplication (Code duplicated to pull values)
    t = calculate_actuator_torque(joint_type, payload_kg, current_velocity, override_signal, battery_level)
    print("--- ROBOT SUB SYSTEM TELEMETRY ---")
    print(f"Joint Type: {joint_type}")
    print(f"Current Payload: {payload_kg} kg")
    print(f"Target Torque Output: {t} Nm")
    print("---------------------------------")
    return t
    