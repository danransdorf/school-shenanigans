input()  # Počet typů láhví je přebytečný
BOTTLE_VOLUMES = list(map(int, input().split()))
goal_volume = int(input())


def display_combinations(goal_volume: int, *, last_bottle_index: int = 0, current_bottles_used: list[int] = []) -> None:
  if goal_volume < 0:  # Neplatná kombinace: vyskoč returnem
    return
  if goal_volume == 0:  # Platná kombinace: vypiš
    print(*current_bottles_used, sep=" ")

  for bottle_index, bottle_volume in enumerate(BOTTLE_VOLUMES[last_bottle_index:]):  # Nepoužívej větší láhve
    display_combinations(
      goal_volume=goal_volume - bottle_volume,
      last_bottle_index=last_bottle_index + bottle_index,  # Naprav index (kvůli enumerate)
      current_bottles_used=current_bottles_used + [bottle_volume],
    )


display_combinations(goal_volume)
