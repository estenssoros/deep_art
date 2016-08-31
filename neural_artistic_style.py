#!/usr/bin/env python

import os
import argparse
import numpy as np
import scipy.misc
import deeppy as dp
from multiprocessing import Pool, cpu_count
from matconvnet import vgg_net
from style_network import StyleNetwork
from transfer import upload, download, clear_images
import progressbar


def weight_tuple(s):
    try:
        conv_idx, weight = map(float, s.split(','))
        return conv_idx, weight
    except:
        raise argparse.ArgumentTypeError('weights must by "int,float"')


def float_range(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0, 1]" % x)
    return x


def weight_array(weights):
    array = np.zeros(19)
    for idx, weight in weights:
        array[idx] = weight
    norm = np.sum(array)
    if norm > 0:
        array /= norm
    return array


def imread(path):
    return scipy.misc.imread(path).astype(dp.float_)


def imsave(path, img):
    img = np.clip(img, 0, 255).astype(np.uint8)
    scipy.misc.imsave(path, img)


def to_bc01(img):
    return np.transpose(img, (2, 0, 1))[np.newaxis, ...]


def to_rgb(img):
    return np.transpose(img[0], (1, 2, 0))


def style_transfer(subject, style, output, iterations):
    pool_method = ['max', 'avg']
    init_noise = 0.0
    default_subject_weights = [(9, 1)]
    default_style_weights = [(0, 1), (2, 1), (4, 1), (8, 1), (12, 1)]
    subject_ratio = 2e-2
    smoothness = 5e-8
    learn_rate = 2.0
    animation = 'animation'
    transfer_learning = 'imagenet-vgg-verydeep-19.mat'

    np.random.seed(None)

    layers, pixel_mean = vgg_net(transfer_learning, pool_method=pool_method[1])

    # Inputs
    style_img = imread(style) - pixel_mean
    subject_img = imread(subject) - pixel_mean

    init_img = subject_img

    noise = np.random.normal(size=init_img.shape, scale=np.std(init_img) * 1e-1)

    init_img = init_img * (1 - init_noise) + noise * init_noise

    # Setup network
    subject_weights = weight_array(default_subject_weights) * subject_ratio
    style_weights = weight_array(default_style_weights)
    net = StyleNetwork(layers, to_bc01(init_img), to_bc01(subject_img),
                       to_bc01(style_img), subject_weights, style_weights,
                       smoothness)

    # Repaint image
    def net_img():
        return to_rgb(net.image) + pixel_mean
    if not os.path.exists(animation):
        os.mkdir(animation)

    params = net.params
    learn_rule = dp.Adam(learn_rate=learn_rate)
    learn_rule_states = [learn_rule.init_state(p) for p in params]
    bar = progressbar.ProgressBar()
    print 'working on {0} -> {1}'.format(style, subject)
    for i in bar(range(iterations)):
        imsave(os.path.join(animation, '%.4d.png' % i), net_img())
        cost = np.mean(net.update())
        for param, state in zip(params, learn_rule_states):
            learn_rule.step(param, state)
        # print('Iteration: {0}/{1}, cost: {2:.4f}'.format(i, iterations, cost))
    imsave(output, net_img())


if __name__ == "__main__":
    clear_images('animation')
    style_transfer('images/finn.jpg', 'images/tiger.jpg', 'finn_tiger.png', 200)
    upload('.png', 'animation/')
