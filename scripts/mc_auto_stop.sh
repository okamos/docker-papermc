#!/bin/bash
COUNT_FILE=/tmp/mc_player_exists

/usr/bin/docker-compose -f /home/${EXEC_USER}/docker-papermc/docker-compose.yml exec -T mc rcon-cli list | grep -e 'There are 0 of a'
if [ $? -eq 0 ]; then
  # player not exists
  cat ${COUNT_FILE}
  if [ $? -eq 0 ]; then
    COUNT=$(expr $(cat ${COUNT_FILE}) - 1)
    if [ ${COUNT} -le 0 ]; then
      rm ${COUNT_FILE}
      /usr/bin/docker-compose -f /home/${EXEC_USER}/docker-papermc/docker-compose.yml down
      gcloud compute instances stop --project="${GCP_PROJECT}" --zone="${GCP_ZONE}" ${INSTANCE_NAME}
    else
      echo ${COUNT} > ${COUNT_FILE}
    fi
  else
    # decrease a number for stop mc server
    echo "10" > ${COUNT_FILE}
  fi
else
  # player exists
  rm ${COUNT_FILE}
fi
