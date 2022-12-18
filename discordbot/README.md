# setup
sudo cp services/discord.service /etc/systemd/system/discord.service
cp discordbot/env.template discordbot/.env
vim discordbot/.env # edit environment variables
sudo systemctl enable discord.service
