import argparse
import csv
import math
import random
import statistics
from dataclasses import dataclass

import numpy as np
import pymunk

GATE_VALUES = [2, 3, 4, 1]  # left to right
MAX_SCORE = 148
DISKS_PER_TURN = 30


@dataclass
class SimConfig:
    board_length: float = 2.0
    board_width: float = 0.4
    start_bar_y: float = 0.43
    gate_bar_y: float = 1.61
    gate_width: float = 0.06
    disk_diameter: float = 0.052
    wall_friction: float = 0.4
    wall_restitution: float = 0.2
    disk_friction: float = 0.4
    disk_restitution: float = 0.2
    damping: float = 0.98
    dt: float = 1 / 120
    max_time: float = 6.0
    stop_speed: float = 0.05
    stable_steps: int = 30
    launch_speed_mean: float = 1.6
    launch_speed_std: float = 0.25
    aim_x_std: float = 0.01
    aim_angle_std_deg: float = 2.0
    aim_y_offset: float = 0.2
    mass: float = 0.05

    @property
    def radius(self) -> float:
        return self.disk_diameter / 2

    @property
    def gap(self) -> float:
        return (self.board_width - 4 * self.gate_width) / 5


def compute_openings(config: SimConfig):
    openings = []
    x = config.gap
    for i in range(4):
        start = x
        end = x + config.gate_width
        openings.append((start, end, i))
        x = end + config.gap
    return openings


def build_space(config: SimConfig, openings):
    space = pymunk.Space()
    space.gravity = (0, 0)
    space.damping = config.damping
    static_body = space.static_body
    thickness = 0.002
    segments = [
        pymunk.Segment(static_body, (0, 0), (config.board_width, 0), thickness),
        pymunk.Segment(
            static_body,
            (0, config.board_length),
            (config.board_width, config.board_length),
            thickness,
        ),
        pymunk.Segment(static_body, (0, 0), (0, config.board_length), thickness),
        pymunk.Segment(
            static_body,
            (config.board_width, 0),
            (config.board_width, config.board_length),
            thickness,
        ),
    ]

    gate_y = config.gate_bar_y
    cursor = 0.0
    for start, end, _ in openings:
        if start > cursor:
            segments.append(
                pymunk.Segment(static_body, (cursor, gate_y), (start, gate_y), thickness)
            )
        cursor = end
    if cursor < config.board_width:
        segments.append(
            pymunk.Segment(
                static_body, (cursor, gate_y), (config.board_width, gate_y), thickness
            )
        )

    for i in range(3):
        boundary_x = openings[i][1] + config.gap / 2
        segments.append(
            pymunk.Segment(
                static_body,
                (boundary_x, gate_y),
                (boundary_x, config.board_length),
                thickness,
            )
        )

    for segment in segments:
        segment.friction = config.wall_friction
        segment.elasticity = config.wall_restitution
    space.add(*segments)
    return space


def ideal_distribution():
    """Disk counts per gate that yield the maximum possible score.

    The best score comes from completing as many full sets as possible (each
    set is one disk in every gate, worth 20 points) and placing any leftover
    disks in the highest-value gate. For 30 disks this is 7 in every gate plus
    2 extras in the value-4 gate, i.e. [7, 7, 9, 7], which scores 148.
    """
    base, extra = divmod(DISKS_PER_TURN, 4)
    best_gate = max(range(len(GATE_VALUES)), key=lambda i: GATE_VALUES[i])
    ideal = [base] * len(GATE_VALUES)
    ideal[best_gate] += extra
    return ideal


def choose_target_gate(counts):
    """Pick the gate furthest below its share of the score-maximizing layout.

    Aiming at the gate with the largest remaining deficit keeps the gates
    balanced (maximizing complete sets) while steering the leftover disks into
    the highest-value gate. Ties are broken toward the higher-value gate so the
    extras land where they score the most. With perfect aim this produces the
    148-point layout; the previous min-count strategy capped out at 143 and
    could never reach the maximum.
    """
    ideal = ideal_distribution()
    deficits = [ideal[i] - counts[i] for i in range(len(counts))]
    max_deficit = max(deficits)
    candidates = [i for i, deficit in enumerate(deficits) if deficit == max_deficit]
    return max(candidates, key=lambda i: GATE_VALUES[i])


def opening_for_x(x, radius, openings):
    for index, (start, end, _) in enumerate(openings):
        if x >= start + radius and x <= end - radius:
            return index
    return None


def add_disk(space, config: SimConfig, rng, openings, target_index):
    radius = config.radius
    start, end, _ = openings[target_index]
    target_x = (start + end) / 2
    spawn_x = target_x + rng.gauss(0, config.aim_x_std)
    spawn_x = max(radius, min(config.board_width - radius, spawn_x))
    spawn_y = radius + 0.002
    target_y = config.gate_bar_y + config.aim_y_offset
    dx = target_x - spawn_x
    dy = target_y - spawn_y
    base_angle = math.atan2(dy, dx)
    angle = base_angle + math.radians(rng.gauss(0, config.aim_angle_std_deg))
    speed = max(0.05, rng.gauss(config.launch_speed_mean, config.launch_speed_std))
    vx = speed * math.cos(angle)
    vy = speed * math.sin(angle)
    if vy <= 0:
        angle = base_angle
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)

    body = pymunk.Body(config.mass, pymunk.moment_for_circle(config.mass, 0, radius))
    body.position = (spawn_x, spawn_y)
    body.velocity = (vx, vy)
    shape = pymunk.Circle(body, radius)
    shape.friction = config.disk_friction
    shape.elasticity = config.disk_restitution
    shape.user_data = {"has_crossed_start": False}
    space.add(body, shape)
    return shape


def step_until_stable(space, config: SimConfig, openings, counts):
    stable_counter = 0
    elapsed = 0.0
    while elapsed < config.max_time:
        space.step(config.dt)
        elapsed += config.dt
        to_remove = []
        for shape in list(space.shapes):
            if shape.body.body_type != pymunk.Body.DYNAMIC:
                continue
            body = shape.body
            radius = shape.radius
            if (
                not shape.user_data["has_crossed_start"]
                and body.position.y - radius >= config.start_bar_y
            ):
                shape.user_data["has_crossed_start"] = True
            if (
                shape.user_data["has_crossed_start"]
                and body.position.y + radius <= config.start_bar_y
            ):
                to_remove.append(shape)
                continue
            if (
                body.position.x < -radius
                or body.position.x > config.board_width + radius
                or body.position.y < -radius
                or body.position.y > config.board_length + radius
            ):
                to_remove.append(shape)
                continue
            if body.position.y - radius >= config.gate_bar_y:
                gate_index = opening_for_x(body.position.x, radius, openings)
                if gate_index is not None:
                    counts[gate_index] += 1
                    to_remove.append(shape)
                    continue

        for shape in to_remove:
            space.remove(shape, shape.body)

        dynamic_bodies = [
            body
            for body in space.bodies
            if body.body_type == pymunk.Body.DYNAMIC
        ]
        if not dynamic_bodies:
            stable_counter += 1
        else:
            max_speed = max(body.velocity.length for body in dynamic_bodies)
            if max_speed < config.stop_speed:
                stable_counter += 1
            else:
                stable_counter = 0
        if stable_counter >= config.stable_steps:
            break


def simulate_subturn(num_disks, counts, rng, config: SimConfig, openings):
    space = build_space(config, openings)
    initial_scored = sum(counts)
    for _ in range(num_disks):
        target_gate = choose_target_gate(counts)
        add_disk(space, config, rng, openings, target_gate)
        step_until_stable(space, config, openings, counts)
    scored_this_subturn = sum(counts) - initial_scored
    return scored_this_subturn


def compute_score(counts):
    sets = min(counts)
    score = sets * 20
    for count, value in zip(counts, GATE_VALUES):
        score += (count - sets) * value
    return score


def simulate_turn(rng, config: SimConfig, verbose=False):
    remaining = DISKS_PER_TURN
    counts = [0, 0, 0, 0]
    openings = compute_openings(config)
    trace = []
    for _ in range(3):
        if remaining <= 0:
            break
        scored = simulate_subturn(remaining, counts, rng, config, openings)
        remaining -= scored
        if verbose:
            trace.append(
                {
                    "scored": scored,
                    "remaining": remaining,
                    "counts": counts.copy(),
                }
            )
    return compute_score(counts), trace


def run_trials(trials, max_turns, rng, config: SimConfig, verbose=False, progress_every=10):
    results = []
    best_score = 0
    print(f"Running {trials} trial(s)...")
    for trial_index in range(1, trials + 1):
        if progress_every and (
            trial_index == 1
            or trial_index % progress_every == 0
            or trial_index == trials
        ):
            print(f"Trial {trial_index}/{trials} (best score so far: {best_score})")
        turns = 0
        success = False
        while turns < max_turns:
            turns += 1
            score, trace = simulate_turn(rng, config, verbose=verbose)
            best_score = max(best_score, score)
            if verbose:
                print(f"  Turn {turns}: score {score}")
                for sub_index, entry in enumerate(trace, start=1):
                    counts = ", ".join(str(value) for value in entry["counts"])
                    print(
                        f"    Sub-turn {sub_index}: scored {entry['scored']}, "
                        f"remaining {entry['remaining']}, counts [{counts}]"
                    )
            if score == MAX_SCORE:
                success = True
                break
        results.append(turns if success else None)
    return results, best_score


def summarize_results(results, max_turns, best_score=None):
    successes = [result for result in results if result is not None]
    failed = len(results) - len(successes)
    print(f"Trials: {len(results)}")
    print(f"Max turns per trial: {max_turns}")
    print(f"Successes: {len(successes)}")
    if best_score is not None:
        print(f"Best score observed: {best_score}/{MAX_SCORE}")
    if failed:
        print(f"Failures (hit max turns): {failed}")
    if not successes:
        print("No successful trials. Increase max turns or adjust parameters.")
        return

    mean = statistics.mean(successes)
    median = statistics.median(successes)
    percentiles = np.percentile(successes, [10, 25, 50, 75, 90])
    print(f"Expected turns (mean): {mean:.2f}")
    print(f"Median turns: {median:.2f}")
    print(
        "Percentiles (10/25/50/75/90): "
        + "/".join(f"{p:.0f}" for p in percentiles)
    )


def write_csv(path, results):
    with open(path, "w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["trial", "turns", "success"])
        for index, turns in enumerate(results, start=1):
            writer.writerow([index, turns or "", "yes" if turns else "no"])


def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Sjoelbak simulator for estimating turns to max score."
    )
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--max-turns", type=int, default=200)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--verbose", action="store_true", help="Print turn details.")
    parser.add_argument(
        "--progress-every",
        type=int,
        default=10,
        help="Print trial progress every N trials (0 disables).",
    )
    parser.add_argument("--launch-speed-mean", type=float, default=1.6)
    parser.add_argument("--launch-speed-std", type=float, default=0.25)
    parser.add_argument("--aim-x-std", type=float, default=0.01)
    parser.add_argument("--aim-angle-std-deg", type=float, default=2.0)
    parser.add_argument("--damping", type=float, default=0.98)
    parser.add_argument("--disk-friction", type=float, default=0.4)
    parser.add_argument("--disk-restitution", type=float, default=0.2)
    parser.add_argument("--wall-friction", type=float, default=0.4)
    parser.add_argument("--wall-restitution", type=float, default=0.2)
    parser.add_argument("--dt", type=float, default=1 / 120)
    parser.add_argument("--max-time", type=float, default=6.0)
    parser.add_argument("--stop-speed", type=float, default=0.05)
    parser.add_argument("--stable-steps", type=int, default=30)
    parser.add_argument("--csv", type=str, help="Write per-trial results to CSV.")
    return parser


def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    config = SimConfig(
        launch_speed_mean=args.launch_speed_mean,
        launch_speed_std=args.launch_speed_std,
        aim_x_std=args.aim_x_std,
        aim_angle_std_deg=args.aim_angle_std_deg,
        damping=args.damping,
        disk_friction=args.disk_friction,
        disk_restitution=args.disk_restitution,
        wall_friction=args.wall_friction,
        wall_restitution=args.wall_restitution,
        dt=args.dt,
        max_time=args.max_time,
        stop_speed=args.stop_speed,
        stable_steps=args.stable_steps,
    )
    rng = random.Random(args.seed)
    results, best_score = run_trials(
        args.trials,
        args.max_turns,
        rng,
        config,
        verbose=args.verbose,
        progress_every=args.progress_every,
    )
    summarize_results(results, args.max_turns, best_score=best_score)
    if args.csv:
        write_csv(args.csv, results)


if __name__ == "__main__":
    main()
