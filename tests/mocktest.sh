# this is well suited for testing using the data in 
# os2mo/backend/tests/fixtures(sql/normal.sql
# without having an actual stsorgsync running
(cat << EOF
[settings]
MOX_LOG_LEVEL = 10 
MOX_LOG_FILE =
OS2MO_SERVICE_URL = http://localhost:4000/service
OS2MO_SAML_TOKEN =
OS2MO_ORG_UUID = 
OS2MO_CA_BUNDLE = true
OS2MO_TOP_UNIT_UUID = f06ee470-9f17-566f-acbe-e938112d46d9
STSORGSYNC_API_URL = http://localhost:3000
STSORGSYNC_CA_BUNDLE = true
STSORGSYNC_MUNICIPALITY = 21212121
EOF
) > /tmp/mocktest.ini
export MOX_MO_CONFIG=/tmp/mocktest.ini

pkill -9 -f tests/mock-stsorgsync.py
python tests/mock-stsorgsync.py &
python -m mox_stsorgsync
