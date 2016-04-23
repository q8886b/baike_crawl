import sys, json

# Load the data that PHP sent us
try:
        data = json.loads(sys.argv[1])
except:
        print "ERROR"
        sys.exit(1)

# generate some data to send to PHP
result = {'status': 'yes!'}

# send it to stdout (to php)
print json.dumps(result)
