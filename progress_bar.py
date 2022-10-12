#!/usr/bin/env python3.7
'''
@author: Chang Min Park (cpark22@buffalo.edu)
'''

import config as cfg


class ProgressBar():
    def __init__(self, _size, _prefix, _length):
        self._percentage = 0
        self._size = _size
        self._prefix = _prefix
        self._suffix = 'Complete'
        self._length = _length

    def start(self):
        if not cfg.ENABLE_PROGRESS_BAR: return
        ProgressBar._printProgressBar(self._percentage, self._size, \
                                        prefix = self._prefix, \
                                        suffix = self._suffix, \
                                        length = self._length)

    def update(self):
        if not cfg.ENABLE_PROGRESS_BAR: return
        self._percentage += 1
        ProgressBar._printProgressBar(self._percentage, self._size, \
                                        prefix = self._prefix, \
                                        suffix = self._suffix, \
                                        length = self._length)

    # Print iterations progress
    def _printProgressBar (iteration, total, prefix = '', suffix = '', \
                    decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent 
                                    complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(
            100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix),
              end=printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()