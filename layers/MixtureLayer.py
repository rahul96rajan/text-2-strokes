import tensorflow as tf


class MixtureLayer(object):
    def __init__(self, input_size, output_size, num_mixtures):
        self.input_size = input_size
        self.output_size = output_size
        self.num_mixtures = num_mixtures

    def __call__(self, inputs, bias=0., reuse=None):
        initializer = tf.keras.initializers.TruncatedNormal(stddev=0.075)
        with tf.variable_scope('mixture_output', reuse=reuse):
            e = tf.layers.dense(inputs, 1,
                                kernel_initializer=initializer, name='e')
            pi = tf.layers.dense(inputs, self.num_mixtures,
                                 kernel_initializer=initializer, name='pi')
            mu1 = tf.layers.dense(inputs, self.num_mixtures,
                                  kernel_initializer=initializer, name='mu1')
            mu2 = tf.layers.dense(inputs, self.num_mixtures,
                                  kernel_initializer=tf.initializer,
                                  name='mu2')
            std1 = tf.layers.dense(inputs, self.num_mixtures,
                                   kernel_initializer=tf.initializer,
                                   name='std1')
            std2 = tf.layers.dense(inputs, self.num_mixtures,
                                   kernel_initializer=tf.initializer,
                                   name='std2')
            rho = tf.layers.dense(inputs, self.num_mixtures,
                                  kernel_initializer=tf.initializer,
                                  name='rho')

            return tf.nn.sigmoid(e), \
                tf.nn.softmax(pi * (1. + bias)), \
                mu1, mu2, \
                tf.exp(std1 - bias), tf.exp(std2 - bias), \
                tf.nn.tanh(rho)
