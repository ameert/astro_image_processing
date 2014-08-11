#!/bin/bash

gitdir=$(git rev-parse --show-toplevel) ;

#sed_str="s|{gitdir}|${gitdir}|"
#sed $sed_str <$gitdir/src/mysql/load_CAMEO.raw >$gitdir/src/mysql/load_CAMEO.mysql

pathfile=${gitdir}'/user_settings.py';

echo "Please enter the MySQL host for your machine (if you don't know better, enter 'localhost' without quotes):";
read mysql_host;
echo "Please enter the MySQL user name for your machine:";
read mysql_user;
echo "Please enter the MySQL password for user ${mysql_user} (if none, leave blank):";
read mysql_password;
echo "Please enter the MySQL database:";
read mysql_dba;

echo "You have entered
user:${mysql_user}
password:${mysql_password}
database:${mysql_dba}
host:${mysql_host}";

echo "
Continue with these settings? Enter 'yes' to continue:";

read mysql_good
if [ $mysql_good == yes ]; then
echo "Continuing with user entered settings";
else
echo "You dont want to continue.;
Terminating";
exit 1;
fi

echo "##### SQL INFO ######
mysql_params={
'user':'${mysql_user}',
'pwd':'${mysql_password}',
'dba':'${mysql_dba}',
'host':'${mysql_host}'
}

">$pathfile;

echo "##### PATHS  #####">>$pathfile;
echo "project_path='$gitdir'">>$pathfile;

if [[ ":$PYTHONPATH:" == *":$gitdir:"* ]]; then
  echo "Your path is correctly set";
else
  echo "Your PYTHONPATH is missing $gitdir, add it now!!!";
  echo "Add $gitdir to your PYTHONPATH in .bashrc for the future!";
fi