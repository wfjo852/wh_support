#-*- coding:utf-8 -*-

import sys
import time
def printProgress (iteration, total, prefix = 'progress', suffix = 'Done', decimals = 1, barLength = 50):
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    progress_text = str(iteration)+"/"+str(total)
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s |%s| %s' % (prefix, bar, percent, '%', progress_text,suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

