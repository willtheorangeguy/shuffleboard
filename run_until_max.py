import argparse
import random

from simulate import MAX_SCORE, SimConfig, simulate_turn


def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Run turns until the maximum score is achieved."
    )
    parser.add_argument("--seed", type=int)
    parser.add_argument(
        "--progress-every",
        type=int,
        default=10,
        help="Print progress every N turns (0 disables).",
    )
    parser.add_argument("--verbose", action="store_true", help="Print per-turn details.")
    parser.add_argument(
        "--max-turns",
        type=int,
        default=0,
        help="Stop after N turns without success (0 means no limit).",
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
    return parser


def run_until_max(rng, config: SimConfig, progress_every, verbose, max_turns):
    turns = 0
    print("Running turns until maximum score is achieved...")
    while True:
        turns += 1
        score, trace = simulate_turn(rng, config, verbose=verbose)
        if verbose:
            print(f"Turn {turns}: score {score}")
            for sub_index, entry in enumerate(trace, start=1):
                counts = ", ".join(str(value) for value in entry["counts"])
                print(
                    f"  Sub-turn {sub_index}: scored {entry['scored']}, "
                    f"remaining {entry['remaining']}, counts [{counts}]"
                )
        elif progress_every and (turns == 1 or turns % progress_every == 0):
            print(f"Turn {turns}: score {score}")
        if score == MAX_SCORE:
            return turns
        if max_turns and turns >= max_turns:
            return None


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
    turns = run_until_max(
        rng,
        config,
        progress_every=args.progress_every,
        verbose=args.verbose,
        max_turns=args.max_turns,
    )
    if turns is None:
        print("Stopped before reaching the maximum score.")
        return
    probability = 1 / turns
    print(f"Turns to reach {MAX_SCORE}: {turns}")
    print(f"Estimated per-turn probability of {MAX_SCORE}: {probability:.6f}")


if __name__ == "__main__":
    main()
