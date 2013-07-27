#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import sys

OK=0
WARNING=1
CRITICAL=2
UNKNOWN=3

def opt():
    parser = OptionParser(usage="usage: %prog -w WARNING -c CRITICAL")
    parser.add_option("-c", default='100M', action="store", type="string", dest="critical")
    parser.add_option("-w", default='200M', action="store", type="string", dest="warning")
    return parser.parse_args()

def convertUnit(s):
    unit = {'g':2**30,'m':2**20,'k':2**10,'t':2**40,'b':1}
    s = s.lower()
    lastchar = s[-1]
    num = int(s[:-1])
    if lastchar in unit:
        return num*unit[lastchar]
    else:
        return int(s)

def getFreeMemory():
    with open('/proc/meminfo', 'r') as fd:
        for line in fd.readlines():
            if line.startswith('MemFree'):
                 k, v, u = line.split()
                 return int(v)*1024

def ch_unit(free_mem):
    t = 2**40

    g = 2**30
    m = 2**20
    k = 2**10
    if free_mem >= t:
        free_mem = "%f T" % free_mem/(t)
    if  free_mem >= g:
        free_mem = "%s G" % (free_mem/g)
    elif g > free_mem >= m:
        free_mem = "%s M" % (free_mem/m)
    elif m > free_mem >= b:
        free_mem = "%s K" % (free_mem/k)
    else:
        free_mem = "%s B" % free_mem
    return free_mem
                       
def main():
    opts, args = opt()
    w = convertUnit(opts.warning)
    c = convertUnit(opts.critical)
    free_mem = getFreeMemory()
    t = ch_unit(free_mem)
    if w >= free_mem > c:
        print "WARNING,free:%s" % t
        sys.exit(WARNING)
    elif free_mem <= c:
        print "CRITICAL,free:%s" % t
        sys.exit(CRITICAL)
    elif free_mem > w:
        print "OK, free:%s" % t
        sys.exit(OK)
    else:
        print "UNKNOWN, free:%s " % t
        sys.exit(UNKNOWN)

if __name__ == "__main__":
    main()
    
