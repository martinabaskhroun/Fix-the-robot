ROBO_SYS_GRAVITY = 9.81

ROBO_SYS_REVOLUTE_LOAD_THRESHOLD = 5.0
ROBO_SYS_REVOLUTE_ARM_LENGTH = 0.25
ROBO_SYS_REVOLUTE_HEAVY_LOAD_MULTIPLIER = 1.5
ROBO_SYS_REVOLUTE_FRICTION_COMPENSATION = 2.5

ROBO_SYS_PRISMATIC_LOAD_THRESHOLD = 10.0
ROBO_SYS_PRISMATIC_HEAVY_LOAD_MULTIPLIER = 1.2
ROBO_SYS_PRISMATIC_FRICTION_COMPENSATION = 1.2

ROBO_SYS_DEFAULT_FRICTION_COMPENSATION = 0.5

ROBO_SYS_EMERGENCY_BRAKE_MULTIPLIER = 0.0
ROBO_SYS_SAFE_MODE_MULTIPLIER = 0.5

ROBO_SYS_CRITICAL_BATTERY_THRESHOLD = 20
ROBO_SYS_LOW_BATTERY_THRESHOLD = 50

ROBO_SYS_CRITICAL_BATTERY_TORQUE_MULTIPLIER = 0.8
ROBO_SYS_LOW_BATTERY_TORQUE_MULTIPLIER = 0.95

ROBO_SYS_OVERVOLTAGE_BOOST = 1.1

ROBO_SYS_CRITICAL_TORQUE_WARNING_THRESHOLD = 50.0

ROBO_SYS_ROUNDING_PRECISION = 2


def stage_one_kinematics(
    joint_type: str,
    payload_kg: float
) -> float:
    if joint_type == "Revolute":
        if payload_kg > ROBO_SYS_REVOLUTE_LOAD_THRESHOLD:
            raw_torque = (
                payload_kg
                * ROBO_SYS_GRAVITY
                * ROBO_SYS_REVOLUTE_ARM_LENGTH
            ) * ROBO_SYS_REVOLUTE_HEAVY_LOAD_MULTIPLIER
        else:
            raw_torque = (
                payload_kg
                * ROBO_SYS_GRAVITY
                * ROBO_SYS_REVOLUTE_ARM_LENGTH
            )

        raw_torque += ROBO_SYS_REVOLUTE_FRICTION_COMPENSATION

    elif joint_type == "Prismatic":
        if payload_kg > ROBO_SYS_PRISMATIC_LOAD_THRESHOLD:
            raw_torque = (
                payload_kg * ROBO_SYS_GRAVITY
            ) * ROBO_SYS_PRISMATIC_HEAVY_LOAD_MULTIPLIER
        else:
            raw_torque = payload_kg * ROBO_SYS_GRAVITY

        raw_torque += ROBO_SYS_PRISMATIC_FRICTION_COMPENSATION

    else:
        raw_torque = payload_kg * ROBO_SYS_GRAVITY
        raw_torque += ROBO_SYS_DEFAULT_FRICTION_COMPENSATION

    return raw_torque


def stage_two_signal_overrides(
    raw_torque: float,
    override_signal: str
) -> float:
    if override_signal == "EMERGENCY_BRAKE":
        raw_torque *= ROBO_SYS_EMERGENCY_BRAKE_MULTIPLIER
    elif override_signal == "SAFE_MODE":
        raw_torque *= ROBO_SYS_SAFE_MODE_MULTIPLIER

    return raw_torque


def stage_three_power_profile(
    raw_torque: float,
    battery_level: int
) -> float:
    if battery_level < ROBO_SYS_CRITICAL_BATTERY_THRESHOLD:
        raw_torque *= ROBO_SYS_CRITICAL_BATTERY_TORQUE_MULTIPLIER

        if raw_torque > ROBO_SYS_CRITICAL_TORQUE_WARNING_THRESHOLD:
            print("CRITICAL: Battery low, throttling torque output!")
    else:
        if battery_level < ROBO_SYS_LOW_BATTERY_THRESHOLD:
            raw_torque *= ROBO_SYS_LOW_BATTERY_TORQUE_MULTIPLIER
        else:
            raw_torque += ROBO_SYS_OVERVOLTAGE_BOOST

    return raw_torque


def torque_engine(
    joint_type: str,
    payload_kg: float,
    override_signal: str,
    battery_level: int
) -> float:
    raw_torque = stage_one_kinematics(
        joint_type,
        payload_kg
    )

    raw_torque = stage_two_signal_overrides(
        raw_torque,
        override_signal
    )

    raw_torque = stage_three_power_profile(
        raw_torque,
        battery_level
    )

    return raw_torque


def calculate_actuator_torque(
    joint_type: str,
    payload_kg: float,
    current_velocity: float,
    override_signal: str,
    battery_level: int
) -> float:
    raw_torque = torque_engine(
        joint_type,
        payload_kg,
        override_signal,
        battery_level
    )

    return round(raw_torque, ROBO_SYS_ROUNDING_PRECISION)


def log_telemetry(
    joint_type: str,
    payload_kg: float,
    current_velocity: float,
    override_signal: str,
    battery_level: int
) -> float:
    raw_torque = torque_engine(
        joint_type,
        payload_kg,
        override_signal,
        battery_level
    )

    t = round(raw_torque, ROBO_SYS_ROUNDING_PRECISION)

    print("--- ROBOT SUB SYSTEM TELEMETRY ---")
    print(f"Joint Type: {joint_type}")
    print(f"Current Payload: {payload_kg} kg")
    print(f"Target Torque Output: {t} Nm")
    print("---------------------------------")

    return t