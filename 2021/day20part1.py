#! /usr/bin/env python

import sys


def print_image(image, pretty=False):
    print('image {} x {}'.format(len(image),
                                 len(image[0]) if len(image) > 0 else 0))
    i = 0
    for row in image:
        print('{} {}'.format(i, ''.join(row) if pretty else row))
        i += 1


def get_expanded_image(image, buffer_pixel):
    result = [[]]
    for column in range(len(image[0]) + 2):
        result[0].append(buffer_pixel)
    for row in image:
        result.append([])
        result[-1].append(buffer_pixel)
        for pixel in row:
            result[-1].append(pixel)
        result[-1].append(buffer_pixel)
    result.append([])
    for column in range(len(image[-1]) + 2):
        result[-1].append(buffer_pixel)

    return result


def get_output_pixel(image, i, j, algorithm, buffer_pixel):
    # print('get_output_pixel: {}, {}'.format(i, j))
    expanded = get_expanded_image(image, buffer_pixel)
    # print('expanded:')
    # print_image(expanded)
    rows = expanded[i:i + 3]
    pixels = [col[j:j + 3] for col in rows]
    # print('pixels:')
    # print_image(pixels)
    index = 0
    for row in pixels:
        for col in row:
            index *= 2
            index += (1 if col == '#' else 0)
    # print('index = {}, result = {}'.format(index, algorithm[index]))
    return algorithm[index]


def enhance(image, algorithm, buffer_pixel):
    buffered_image = get_expanded_image(image, buffer_pixel)
    # print('buffered_image:')
    # print_image(buffered_image)
    # print()
    row = ['X' for i in range(len(buffered_image))]
    result = [row.copy() for i in range(len(buffered_image[0]))]
    # print('result before filled')
    # print_image(result)
    # print()

    for i in range(len(buffered_image)):
        for j in range(len(buffered_image[i])):
            result[i][j] = get_output_pixel(buffered_image, i, j, algorithm,
                                            buffer_pixel)
            # print_image(result)
    # print('result filled:')
    # print_image(result)
    # print()

    return result


def count_lit_pixels(image):
    count = 0
    for row in image:
        for pixel in row:
            if pixel == '#':
                count += 1

    return count


def main(args):
    algorithm = None
    image = []
    width = None
    with open(args[0], 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        algorithm = lines[0]
        for line in lines[2:]:
            row = list(line)
            if width is None:
                width = len(row)
            elif width != len(row):
                raise Exception(
                    'Inconsistent widths: expected {}, got {}'.format(
                        width, len(row)))
            image.append(row)

    print(algorithm)
    print('original image:')
    print_image(image, True)
    print()

    result = enhance(image, algorithm, '.')
    print('enhanced image:')
    print_image(result, True)
    print()

    result = enhance(result, algorithm, algorithm[0])
    print('enhanced image:')
    print_image(result, True)
    print()
    print(count_lit_pixels(result))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
