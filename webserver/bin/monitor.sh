 #!/bin/sh

 ps -ef|grep webserver.py|grep -v "grep"
 if [ $? -ne 0 ]
 then
 echo "start process....."
 	./services.sh webserver.py start
 else
 echo "runing....."
 fi
