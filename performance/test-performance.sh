GOOGLE_API_KEY="AIzaSyCnEBxfAnkQluYBbgCMXkzfUm3oWVKKoKM"
PROJECT_URL="https://sasadangelo.github.io/code4projects"
OUTPUT="performance-result.txt"

PROJECTS_PAGES=$(cat project-page.sh)

>> $OUTPUT
for page in $PROJECTS_PAGES
do
    RESULT=$(curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$PROJECT_URL$page/&prettyprint=false&strategy=mobile&&category=performance&fields=lighthouseResult.categories.*.score&key=$GOOGLE_API_KEY" 2>/dev/null)
    echo "$PROJECT_URL$page (MOBILE) $RESULT"
    sleep 2
    RESULT=$(curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$PROJECT_URL$page/&prettyprint=false&strategy=desktop&&category=performance&fields=lighthouseResult.categories.*.score&key=$GOOGLE_API_KEY" 2>/dev/null)
    echo "$PROJECT_URL$page (DESKTOP) $RESULT"
    sleep 2
done 
