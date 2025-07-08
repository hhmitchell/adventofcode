#! /usr/bin/env python

from common import util

from functools import partial
import re

class Block():
    def __init__(self, blkid, blk_size):
        self.blkid = blkid
        self.blk_size = blk_size
        self.free_size = 0
        self.prev = None
        self.next = None

    def append_free(self, free_size):
        self.free_size += free_size

    def set_free(self, free_size):
        self.free_size = free_size

    def total(self):
        return self.blk_size + self.free_size

    def __str__(self):
        return f'({str(self.blkid)},{self.blk_size},{self.free_size})'

class BlockInfo():
    def __init__(self):
        self._block = []
        self._block_by_id = []

    def total(self):
        return sum([block.total() for block in self._block])

    def append_block(self, blkid, blk_size):
        block = Block(blkid, blk_size)
        if self._block:
            block.prev = self._block[-1]
            self._block[-1].next = block

        self._block.append(block)
        if len(self._block_by_id) < blkid:
            print(f'Appending non-contiguous block ID: {block}')
            self._block_by_id.extend([None] * (blkid - len(self._block_by_id)))
        self._block_by_id.append(block)

    def append_free(self, free_size):
        self._block[-1].set_free(free_size)
        self._block_by_id[-1].set_free(free_size)

    def compact(self):
        start_total = self.total()
        print(f'start total = {start_total}')
        for i in range(len(self._block_by_id) -1, 0, -1):
            block = self._block_by_id[i]
            # print(f'Looking to move {block}')
            j = 0
            target_block = self._block[j]
            while target_block != block:
                if target_block.free_size >= block.blk_size:
                    # print(f'Moving {block} to in front of {target_block}')
                    if block.prev:
                        block.prev.append_free(block.total())
                        block.prev.next = block.next
                    if block.next:
                        block.next.prev = block.prev

                    block.set_free(target_block.free_size - block.blk_size)
                    target_block.set_free(0)

                    block.next = target_block.next
                    block.prev = target_block
                    target_block.next.prev = block
                    target_block.next = block

                    self._block.remove(block)
                    self._block.insert(j + 1, block)
                    break
                j += 1
                target_block = self._block[j]
        print(f'end total = {self.total()}')

    def checksum(self):
        result = 0
        position = 0
        for block in self._block:
            # print(f'block = {block}')
            result += ((position * block.blk_size) + ((block.blk_size * (block.blk_size - 1)) // 2)) * block.blkid
            position += block.total()

        return result


    def __str__(self):
        wrap = 10
        counter = 0
        total = 0
        lines = ['*****']
        for block in self._block:
            total += block.total()
            if counter % 10 == 0:
                lines.append(f'{block}')
            else:
                lines[-1] = lines[-1] + f'{block}'
            counter += 1
        lines.append(f'total blocks: {counter}')
        lines.append(f'total size: {total}')
        lines.append('*****')
        return '\n'.join(lines)


def process_line(block_info, line):
    blkid = 0
    for i in range(len(line.strip())):
        if i % 2 == 0:
            block_info.append_block(blkid, int(line[i]))
            blkid += 1
        else:
            block_info.append_free(int(line[i]))

def main():
    block_info = BlockInfo()
    # util.read('day09/sample.txt', partial(process_line, block_info))
    util.read('day09/input.txt', partial(process_line, block_info))

    print(block_info)
    block_info.compact()
    print(block_info)
    print(f'checksum = {block_info.checksum()}')

if __name__ == '__main__':
    main()
