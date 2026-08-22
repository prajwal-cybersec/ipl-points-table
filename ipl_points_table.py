"""
IPL Points Table Generator
---------------------------
Takes team stats as input (matches won/lost, runs scored/conceded,
balls faced/bowled) and prints a sorted IPL-style points table
with Net Run Rate (NRR).

Points system: Win = 2 points, Loss = 0 points, Draw/No Result = 1 point each
              (Tied matches are decided by Super Over in IPL, so a "tie" still
              counts as a Win or Loss overall — only abandoned/no-result
              matches count as a true "Draw" here.)
NRR formula   : (Runs Scored / Overs Faced) - (Runs Conceded / Overs Bowled)
                where Overs = Balls / 6
                Note: No-result matches don't add runs/balls, so they don't
                affect NRR.
"""


def balls_to_overs(balls):
    """Convert balls into a decimal 'overs' value used for NRR calculation."""
    return balls / 6


def calculate_nrr(runs_scored, balls_faced, runs_conceded, balls_bowled):
    overs_faced = balls_to_overs(balls_faced)
    overs_bowled = balls_to_overs(balls_bowled)

    run_rate_for = runs_scored / overs_faced if overs_faced > 0 else 0
    run_rate_against = runs_conceded / overs_bowled if overs_bowled > 0 else 0

    return run_rate_for - run_rate_against


def get_team_data():
    teams = []

    try:
        num_teams = int(input("Enter number of teams: "))
    except ValueError:
        print("Please enter a valid number.")
        return teams

    for i in range(num_teams):
        print(f"\n--- Enter details for Team {i + 1} ---")
        name = input("Team name: ").strip()

        try:
            matches_won = int(input("Matches won: "))
            matches_lost = int(input("Matches lost: "))
            matches_drawn = int(input("Matches drawn / no result: "))
            runs_scored = int(input("Total runs scored: "))
            balls_faced = int(input("Total balls faced (batting): "))
            runs_conceded = int(input("Total runs conceded (bowling): "))
            balls_bowled = int(input("Total balls bowled: "))
        except ValueError:
            print("Invalid input, skipping this team.")
            continue

        matches_played = matches_won + matches_lost + matches_drawn
        points = (matches_won * 2) + (matches_drawn * 1)
        nrr = calculate_nrr(runs_scored, balls_faced, runs_conceded, balls_bowled)

        teams.append({
            "name": name,
            "played": matches_played,
            "won": matches_won,
            "lost": matches_lost,
            "drawn": matches_drawn,
            "points": points,
            "nrr": nrr
        })

    return teams


def print_points_table(teams):
    if not teams:
        print("\nNo team data available to display.")
        return

    # Sort by Points (desc), then NRR (desc) — standard IPL tiebreaker
    teams.sort(key=lambda t: (t["points"], t["nrr"]), reverse=True)

    print("\n" + "=" * 76)
    print("IPL POINTS TABLE".center(76))
    print("=" * 76)
    header = f"{'Pos':<5}{'Team':<20}{'P':<5}{'W':<5}{'L':<5}{'D':<5}{'Pts':<6}{'NRR':<8}{'Status':<15}"
    print(header)
    print("-" * 70)

    for pos, team in enumerate(teams, start=1):
        # Simple status logic: top 4 -> Playoffs, else -> Eliminated
        status = "Playoffs" if pos <= 4 else "Eliminated"
        nrr_str = f"{team['nrr']:+.3f}"

        row = (f"{pos:<5}{team['name']:<20}{team['played']:<5}"
               f"{team['won']:<5}{team['lost']:<5}{team['drawn']:<5}"
               f"{team['points']:<6}{nrr_str:<8}{status:<15}")
        print(row)

    print("=" * 76)


def main():
    print("Welcome to the IPL Points Table Generator!\n")
    teams = get_team_data()
    print_points_table(teams)


if __name__ == "__main__":
    main()
