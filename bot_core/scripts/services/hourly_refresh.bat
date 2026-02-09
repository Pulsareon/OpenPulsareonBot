@echo off
echo Running hourly OAuth token refresh...
python "E:\PulsareonThinker\scripts\services\oauth_refresher.py" once
echo Refresh completed at %date% %time%