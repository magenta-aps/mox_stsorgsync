# Mox : stsorgsync

Integration between OS2MO and StsOrgSync

StsOrgSync ([https://github.com/Gentofte/STSOrgSync](https://github.com/Gentofte/STSOrgSync)) is a middleware meant to make it easier to 
insert / upgrade organizational units and users into STS organization

This small module exports OS2MO Employees and Organizational units along with selected relations, a subset of the available addresses, itsystems and engagements to STS organization via StsOrtgSync.

Apart from the configuration for this module, which is rather small, care must be taken to follow the steps outlined in the installation manual for StsOrgSync, 
the current version being [this](https://github.com/Gentofte/STSOrgSync/raw/master/Documentation/Installation%20Guide.docx)

A docker image of the service component is available on the following public repository (docker hub),
Docker image: https://hub.docker.com/r/os2sync/linux

The most important step is to get access to Production and Test-instances of STS-Organization on serviceplatformen.

The configuration of this module is quite simple and is done using a configuration file which is found like this:

* location is specifed in environment-variable *MOX_MO_CONFIG*
* location is 'settings.ini' in current working directory
* location is 'settings.ini' next to the file 'config.py'


The configuration looks like this:

    [settings]

    ; log level set this to a numeric representation of a log level - 10 is debug.
    MOX_LOG_LEVEL = 10 

    ; log file - set this to blank to have log in stderr, otherwise this must be a file name. 
    MOX_LOG_FILE =

    ; os2mo-service url - this is the full url to os2mo-service - it must end in '/service'.
    OS2MO_SERVICE_URL = 

    ; os2mo saml token - if You are running an authenticated OS2MO, You must use this access token.
    OS2MO_SAML_TOKEN =

    ; os2mo org uuid - leave it blank to query it from server. 
    OS2MO_ORG_UUID = 
    
    ; os2mo ca bundle - 'true' means use the built in ca-bundle, 'false' or blank means dont use any
    ; otherwise it is interpreted as a filename pointing to the ca certs.
    OS2MO_CA_BUNDLE = true

    ; os2mo top org unit of administrative tree 
    OS2MO_TOP_UNIT_UUID = decc5c18-98a7-11e9-98aa-00163e3c4928

    ; stsorgsync api url - this is the url to the stsorgsync instance - it will typically end with '/api/v1_1' or similar 
    STSORGSYNC_API_URL = http://some-stsorgsync-url/api/v1_1

    ; stsorgsync ca bundle - 'true' means use the built in ca-bundle, 'false' or blank means dont use any
    ; otherwise it is interpreted as a filename pointing to the ca certs.
    STSORGSYNC_CA_BUNDLE = true

    ; stsorgsync municipality this is the cvr(vat) number of the municipality
    ; this is an 8 digit number dfound on virk.dk
    STSORGSYNC_MUNICIPALITY = 21212121

    ; IMPORTANT
    ; Due to a limitation of the current service component,
    ; certain name values must not exceed the length of 64 chars.
    stsorgsync_truncate = 64


A typical logfile (with loglevel 20) should look somethat like this:

    INFO 2019-09-02 10:55:51,043 mox_stsorgsync mox_stsorgsync starting
    WARNING 2019-09-02 10:55:51,043 mox_stsorgsync -----------------------------------------
    WARNING 2019-09-02 10:55:51,043 mox_stsorgsync program configuration:
    WARNING 2019-09-02 10:55:51,043 mox_stsorgsync     MOX_LOG_FILE='/tmp/logfile'
    WARNING 2019-09-02 10:55:51,043 mox_stsorgsync     MOX_LOG_LEVEL='0'
    WARNING 2019-09-02 10:55:51,043 mox_stsorgsync     OS2MO_CA_BUNDLE=True
    WARNING 2019-09-02 10:55:51,043 mox_stsorgsync     OS2MO_ORG_UUID=''
    WARNING 2019-09-02 10:55:51,043 mox_stsorgsync     OS2MO_SERVICE_URL='http://localhost:4000/service'
    WARNING 2019-09-02 10:55:51,043 mox_stsorgsync     OS2MO_TOP_UNIT_UUID='f06ee470-9f17-566f-acbe-e938112d46d9'
    WARNING 2019-09-02 10:55:51,043 mox_stsorgsync     STSORGSYNC_API_URL='http://localhost:3000'
    WARNING 2019-09-02 10:55:51,043 mox_stsorgsync     STSORGSYNC_CA_BUNDLE=True
    WARNING 2019-09-02 10:55:51,043 mox_stsorgsync     STSORGSYNC_MUNICIPALITY='21212121'
    INFO 2019-09-02 10:55:51,116 mox_stsorgsync sync_stsorgsync_orgunits starting
    INFO 2019-09-02 10:55:51,116 mox_stsorgsync sync_stsorgsync_orgunits getting all organisational units from os2mo
    INFO 2019-09-02 10:55:51,722 mox_stsorgsync sync_stsorgsync_orgunits getting all organisational units from stsorgsync
    INFO 2019-09-02 10:55:51,725 mox_stsorgsync sync_stsorgsync_orgunits deleting organisational units from stsorgsync if deleted in os2mo
    INFO 2019-09-02 10:55:51,725 mox_stsorgsync sync_stsorgsync_orgunits upserting organisational units in stsorgsync
    ...
    INFO 2019-09-02 10:56:17,560 mox_stsorgsync sync_stsorgsync_orgunits done
    INFO 2019-09-02 10:56:17,560 mox_stsorgsync sync_stsorgsync_users starting
    INFO 2019-09-02 10:56:17,560 mox_stsorgsync sync_stsorgsync_users getting list of users from stsorgsync
    INFO 2019-09-02 10:56:17,563 mox_stsorgsync sync_stsorgsync_users getting list of users from os2mo
    INFO 2019-09-02 10:56:19,228 mox_stsorgsync sync_stsorgsync_users deleting os2mo-deleted users in stsorgsync
    INFO 2019-09-02 10:56:19,228 mox_stsorgsync sync_stsorgsync_users upserting stsorgsync users
    ...
    INFO 2019-09-02 12:06:56,656 mox_stsorgsync sync_stsorgsync_users done
    INFO 2019-09-02 12:06:56,656 mox_stsorgsync -----------------------------------------
    INFO 2019-09-02 12:06:56,656 mox_stsorgsync program counters:
    INFO 2019-09-02 12:06:56,656 mox_stsorgsync     Medarbejdere fundet i OS2MO=270
    INFO 2019-09-02 12:06:56,656 mox_stsorgsync     Medarbejdere fundet i OS2Sync=0
    INFO 2019-09-02 12:06:56,656 mox_stsorgsync     Medarbejdere overført til OS2SYNC=230
    INFO 2019-09-02 12:06:56,656 mox_stsorgsync     Orgenheder fundet i OS2MO=73
    INFO 2019-09-02 12:06:56,656 mox_stsorgsync     Orgenheder fundet i OS2Sync=0
    INFO 2019-09-02 12:06:56,656 mox_stsorgsync     Orgenheder som opdateres i OS2Sync=54
    WARNING 2019-09-02 12:06:56,656 mox_stsorgsync -----------------------------------------
    WARNING 2019-09-02 12:06:56,657 mox_stsorgsync program configuration:
    WARNING 2019-09-02 12:06:56,657 mox_stsorgsync     MOX_LOG_FILE='/tmp/logfile'
    WARNING 2019-09-02 12:06:56,657 mox_stsorgsync     MOX_LOG_LEVEL='0'
    WARNING 2019-09-02 12:06:56,657 mox_stsorgsync     OS2MO_CA_BUNDLE=True
    WARNING 2019-09-02 12:06:56,657 mox_stsorgsync     OS2MO_ORG_UUID='1f76c88c-2a40-41db-968b-bfbbcc1ae762'
    WARNING 2019-09-02 12:06:56,657 mox_stsorgsync     OS2MO_SERVICE_URL='http://localhost:4000/service'
    WARNING 2019-09-02 12:06:56,657 mox_stsorgsync     OS2MO_TOP_UNIT_UUID='c8755b84-8cc9-483b-83cf-dfb1babd2419'
    WARNING 2019-09-02 12:06:56,657 mox_stsorgsync     STSORGSYNC_API_URL='http://localhost:3000'
    WARNING 2019-09-02 12:06:56,657 mox_stsorgsync     STSORGSYNC_CA_BUNDLE=True
    WARNING 2019-09-02 12:06:56,657 mox_stsorgsync     STSORGSYNC_MUNICIPALITY='21212121'
    INFO 2019-09-02 12:06:56,657 mox_stsorgsync mox_stsorgsync done


## Os2sync log printer

A small module has been added to this package in order to facilitate log-forensics regarding os2sync

    python -m os2sync_log_printer /var/log/os2sync/service.log

It simply transforms the log, which is partly xml, into more human readble form
