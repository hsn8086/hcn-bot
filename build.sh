WORK_DIR="hcn-bot-building"
if [ -d "$WORK_DIR" ]; then
  echo "${WORK_DIR} exists, do not reclone"
else
    git clone https://github.com/hsn8086/hcn-bot $WORK_DIR
fi
docker build . -t hsn8086/hcn-bot
