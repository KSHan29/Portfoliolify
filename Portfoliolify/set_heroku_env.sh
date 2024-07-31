# set_heroku_env.sh
while IFS= read -r line || [ -n "$line" ]; do
  heroku config:set "$line" -a 
done < .env
