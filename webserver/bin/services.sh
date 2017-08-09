#!/bin/bash
#
# 2017/03/28 by yuhang.liu

if [ -z $1  ]; then
        echo "usage: ./"`basename $0`" [service1,service2,...] [start|stop|restart]"
        exit
fi

case "$2" in
        start)
        ;;
        restart)
        ;;
        stop)
        ;;
        *)
        echo "usage: ./"`basename $0`" [service1,service2,...] [start|stop|restart]"
        exit
        ;;
esac

param_list=`echo $1 | sed s/,/" "/g`
process_list=""

for param_item in $param_list
do
        if [ $2 == "stop" ] || [ $2 == "restart" ]; then
                killall -q $param_item
                sleep 3
                pid=`ps -ef|grep $param_item|grep -v "grep"|grep -v $0|awk '{print $2}'`
                i=0
                while [ "$i" != "5" ] && [ "$pid" ]
                do
                        kill -9 $pid
                        sleep 3
                        pid=`ps -ef|grep $param_item|grep -v "grep"|grep -v $0|awk '{print $2}'`
                        if [ !"$pid" ]
                        then
                                break
                        fi
                        let i++
                done

                if [ "$pid" ]
                then
                        echo "stop $param_item failed, pid:$pid"
                        exit 0
                else
                        echo "stop $param_item succeed"
                fi
        fi

        if [ $2 == "start" ] || [ $2 == "restart" ]; then
                nohup ./$param_item 1>/dev/null 2>&1 &
                sleep 1
                pid=`ps -ef|grep $param_item|grep -v "grep"|grep -v $0|awk '{print $2}'`
                i=0
                while [ "$i" != "5" ] && [ ! -n "$pid" ]
                do
                        nohup ./$param_item 1>/dev/null 2>&1 &
                        sleep 1
                        pid=`ps -ef|grep $param_item|grep -v "grep"|grep -v $0|awk '{print $2}'`
                        if [ "$pid" ]
                        then
                                break
                        fi
                        let i++
                done

                if [ "$pid" ]
                then
                        echo "start $param_item successed, pid:$pid"
                else
                        echo "start $param_item failed"
                fi
        fi
done;