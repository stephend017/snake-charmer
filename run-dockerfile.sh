
#!/bin/bash
docker build -t sc .
docker run -e INPUT_GITHUB_TOKEN=$(echo $GH_PAT) -e "INPUT_EVENT_PAYLOAD=$(<docker-env.json)" -e GITHUB_REPOSITORY="stephend017/snake_charmer" sc
