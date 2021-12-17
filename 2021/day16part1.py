#! /usr/bin/env python

import math
import sys


class HexDigits:
    def __init__(self, digits, current_value, bits_available):
        self.digits = digits
        self.current_value = current_value
        self.bits_available = bits_available

    def get_state(self):
        total_bits_remaining = len(self.digits) * 4 + self.bits_available
        lines = []
        lines.append(str(self.digits))
        lines.append(
            'current_value = {}, bits_available = {}, total bits remaining = {}'
            .format(self.current_value, self.bits_available,
                    total_bits_remaining))

        return '\n'.join(lines)

    def has_digits(self):
        return len(self.digits) > 0

    def read_value(self, num_bits):
        while self.bits_available < num_bits:
            self.current_value = (self.current_value << 4) | int(
                self.digits.pop(0), 16)
            self.bits_available += 4
        self.bits_available -= num_bits
        mask = ((1 << num_bits) - 1) << self.bits_available
        result = (self.current_value & mask) >> self.bits_available
        self.current_value = self.current_value & (
            (1 << self.bits_available) - 1)
        return result

    def consume_zeroes(self):
        if self.current_value != 0:
            raise Exception('bits remain, state:\n{}'.format(self.get_state()))
        for digit in self.digits:
            if int(digit, 16) != 0:
                raise Exception('bits remain, state:\n{}'.format(
                    self.get_state()))
        bits_consumed = self.bits_available + (4 * len(self.digits))
        self.digits = []
        self.bits_available = 0
        return bits_consumed


class Packet:
    def __init__(self, version, type):
        self.version = version
        self.type = type
        self.value = None
        self.packets = None

    def __str__(self, level=0):
        indent = ' ' * 2 * level
        padding = ' ' * 2 * (level + 1)
        lines = []
        lines.append('{}Version: {}; Type: {}'.format(
            indent, self.version, 'Operator({})'.format(self.type)
            if self.is_operator() else 'Literal'))
        if self.is_operator():
            lines.append('{}Sub-Packets [{}]:'.format(padding,
                                                      len(self.packets)))
            for packet in self.packets:
                lines.append(packet.__str__(level + 1))
        else:
            lines.append('{}Value: {}'.format(padding, self.value))
        return '\n'.join(lines)

    def is_operator(self):
        return self.type != 4

    def set_value(self, value):
        if self.type != 4:
            raise Exception('Can set value only on literal value packets.')
        self.value = value

    def add_packets(self, packets):
        if type == 4:
            raise Exception('Can add packets only on operator packets.')
        if self.packets is None:
            self.packets = []
        self.packets.extend(packets)

    def get_version_sum(self):
        sum = self.version
        if self.is_operator():
            for packet in self.packets:
                sum += packet.get_version_sum()

        return sum


def decode_literal_value(hex_digits):
    digits = []
    last_digit = False
    while not last_digit:
        digit = hex_digits.read_value(5)
        leading_bit = (digit & (1 << 4)) >> 4
        if leading_bit == 0:
            last_digit = True
        digits.append(digit & ((1 << 4) - 1))

    value = 0
    for digit in digits:
        value = (value << 4) | digit
    bits_consumed = len(digits) * 5

    return (value, bits_consumed)


def decode_literal_value_packet(hex_digits):
    version_id = hex_digits.read_value(3)
    type_id = hex_digits.read_value(3)
    if type_id != 4:
        raise Exception('Expected type_id = 4, got {}'.format(type_id))
    (value, bits_consumed) = decode_literal_value(hex_digits)
    packet = Packet(version_id, type_id)
    packet.set_value(value)
    return (packet, bits_consumed + 6)


def decode_sub_packets(hex_digits):
    sub_packets = []
    length_type_id = hex_digits.read_value(1)
    total_bits_consumed = 1
    if length_type_id == 0:
        num_bits = hex_digits.read_value(15)
        total_bits_consumed += 15
        while num_bits > 0:
            (sub_packet, bits_consumed) = decode_packet(hex_digits)
            total_bits_consumed += bits_consumed
            sub_packets.append(sub_packet)
            num_bits -= bits_consumed
    else:
        num_sub_packets = hex_digits.read_value(11)
        total_bits_consumed += 11
        for i in range(num_sub_packets):
            (sub_packet, bits_consumed) = decode_packet(hex_digits)
            sub_packets.append(sub_packet)
            total_bits_consumed += bits_consumed

    return (sub_packets, total_bits_consumed)


def decode_packet(hex_digits, consume_zeroes=False):
    packet = None
    version_id = None
    type_id = None
    total_bits_consumed = 0
    if not version_id:
        version_id = hex_digits.read_value(3)
        total_bits_consumed += 3
    if not type_id:
        type_id = hex_digits.read_value(3)
        total_bits_consumed += 3

    if type_id == 4:
        (literal_value, bits_consumed) = decode_literal_value(hex_digits)
        packet = Packet(version_id, type_id)
        packet.set_value(literal_value)
        total_bits_consumed += bits_consumed
        if consume_zeroes:
            zeroes_consumed = hex_digits.consume_zeroes()
            bits_consumed += zeroes_consumed
    else:
        (sub_packets, bits_consumed) = decode_sub_packets(hex_digits)
        packet = Packet(version_id, type_id)
        packet.add_packets(sub_packets)
        total_bits_consumed += bits_consumed
        if consume_zeroes:
            zeroes_consumed = hex_digits.consume_zeroes()
            bits_consumed += zeroes_consumed

    return (packet, total_bits_consumed)


def decode(hex_digits):
    (packet, bits_consumed) = decode_packet(hex_digits, True)

    return packet


def main(args):
    transmission = []
    with open(args[0], 'r') as f:
        lines = f.readlines()
        for line in lines:
            transmission.append(list(line.strip()))

    for digits in transmission:
        hex_digits = HexDigits(digits, 0, 0)
        print('decoding {}'.format(''.join(digits)))
        packet = decode(hex_digits)
        print('Sum = {}'.format(packet.get_version_sum()))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
