@ECHO OFF
SET LOGFILE=MyLogFile.log
echo Started... >> %LOGFILE% 

for /f "tokens=*" %%a in (t100-tweeters.txt) do (
	echo Started Scrapping %%a... >> %LOGFILE% 
	start /wait cmd.exe /k "C: && cd \Users\moham\Desktop\scrapy-tweets && scrapy crawl TweetScraper -a query=%%a -a  crawl_user=True && exit()
	echo Finished Scrapping %%a... >> %LOGFILE% 
)
pause

echo Finished Scrapping all Users >> %LOGFILE% 