#!/bin/bash

gitdir=$(git rev-parse --show-toplevel);
cd ${gitdir};
cd ..;
topdir=$(pwd);
cd ${gitdir};

#sed_str="s|{gitdir}|${gitdir}|"
#sed $sed_str <$gitdir/src/mysql/load_CAMEO.raw >$gitdir/src/mysql/load_CAMEO.mysql

pathfile=${gitdir}'/user_settings.py';
echo 'Building pathfile: $pathfile';

############## SQL SETTINGS ###############################

echo "Please enter the MySQL host for your machine (if you don't know better, 
enter 'localhost' without quotes):";
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

############## CASJOBS INFO ###############################

echo "Please enter the CasJobs username (not required):";
read casjobs_username;
echo "Please enter the CasJobs wsid (not required):";
read casjobs_wsid;
echo "Please enter the CasJobs password (not required):";
read casjobs_password;

echo "You have entered
casjobs user:${casjobs_username}
casjobs wsid:${casjobs_wsid}
casjobs password:${casjobs_password}";

echo "
Continue with these settings? Enter 'yes' to continue:";

read casjobs_good
if [ $casjobs_good == yes ]; then
echo "Continuing with user entered settings";
else
echo "You dont want to continue.;
Terminating";
exit 1;
fi

echo "##### CASJOBS INFO ######
casjobs_info={
'username':'${casjobs_username}',
'password':'${casjobs_password}',
'wsid':'${casjobs_wsid}'
}

">>$pathfile;

############ PATHS ##########################
echo "##### PATHS  #####">>$pathfile;
echo "project_path='$gitdir'">>$pathfile;

if [[ ":$PYTHONPATH:" == *":${topdir}:"* ]]; then
  echo "Your path is correctly set";
else
  echo "Your PYTHONPATH is missing ${topdir}, add it now!!!";
  echo "Add ${topdir} to your PYTHONPATH in .bashrc for the future!";
  echo "If ${topdir} is not added, this module may not be found!";
fi



echo "Please enter the full path to GALFIT (not required):";
read galfit_path;

echo "You have entered 
Path to GALFIT:${galfit_path}";

echo "Continue with these settings? Enter 'yes' to continue:";

read isgood;
if [ $isgood == yes ]; then
echo "Continuing with user entered settings";
else
echo "You dont want to continue.
Terminating";
exit 1;
fi

echo "
galfit_path=${galfit_path}'

">>$pathfile;


exit 0;

