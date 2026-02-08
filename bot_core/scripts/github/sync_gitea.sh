#!/bin/bash
# Sync to local Gitea
# Usage: ./sync_gitea.sh

cd /e/PulsareonThinker

# Check if gitea remote exists
if ! git remote | grep -q "gitea"; then
    echo "Adding gitea remote..."
    git remote add gitea http://localhost:3000/pulsareonbot/PulsareonThinker.git
fi

# Push to gitea
echo "Pushing to Gitea..."
git push gitea master

echo "Done!"
