@ECHO OFF
SET LOGFILE=MyLogFile.log
echo Started... >> %LOGFILE% 

for /f "tokens=*" %%a in (t500-tweeters.txt) do (
	echo Started Scrapping %%a... >> %LOGFILE% 
	start /wait cmd /k "C: && cd %cd% && scrapy crawl TweetScraper -a query=%%a && exit()
	echo Finished Scrapping %%a... >> %LOGFILE% 
)
pause

echo Finished Scrapping all Users >> %LOGFILE% 