start_date="2025-06-22"
total_days=16

# Find all files deeply nested in subfolders (excluding the script itself)
mapfile -t all_files < <(find . -type f -not -path '*/.*' -not -name "*.sh")

for day in $(seq 0 $total_days); do
    # 1. Randomly decide if we work today (skips ~30% of days for realism)
    if [ $((RANDOM % 10)) -lt 3 ]; then continue; fi

    # 2. Randomly decide HOW MUCH we work today (1 to 8 commits)
    # More commits = Darker Green Square
    daily_commits=$((1 + RANDOM % 8))

    for ((c=0; c<daily_commits; c++)); do
        # Pick a random file from our list
        random_file="${all_files[$RANDOM % ${#all_files[@]}]}"
        
        if [ -f "$random_file" ]; then
            # Generate random time
            random_hour=$(printf "%02d" $((9 + RANDOM % 12)))
            random_min=$(printf "%02d" $((RANDOM % 60)))
            commit_date=$(date -d "$start_date + $day days $random_hour:$random_min:00" +"%Y-%m-%dT%H:%M:%S")

            export GIT_AUTHOR_DATE="$commit_date"
            export GIT_COMMITTER_DATE="$commit_date"

            # Commit the specific file
            git add "$random_file"
            git commit -m "Refactoring and updating $(basename "$random_file")" --allow-empty
        fi
    done
done

# Final catch-all to make sure everything is added
git add .
git commit -m "Final project cleanup" --date="2025-11-30T18:00:00"
unset GIT_AUTHOR_DATE GIT_COMMITTER_DATE