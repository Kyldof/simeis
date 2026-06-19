#ce code à besoin de la variable d'environnement LABELS

TARGETS=$(echo "$LABELS" | jq -r '.[] | select(startswith("propagate:")) | ltrimstr("propagate:")')

echo "$TARGETS" | while read -r target; do
  echo "target is $target"
done
