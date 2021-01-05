import tensorflow as tf
import numpy as np


class WindowLayer(object):
    def __init__(self, num_mixtures, sequence, num_letters):
        self.sequence = sequence  # one-hot encoded sequence of characters -- [batch_size, length, num_letters]
        self.seq_len = tf.shape(sequence)[1]
        self.num_mixtures = num_mixtures
        self.num_letters = num_letters
        self.u_range = -tf.expand_dims(tf.expand_dims(tf.range(0., tf.cast(self.seq_len, dtype=tf.float32)), axis=0),
                                       axis=0)

    def __call__(self, inputs, k, reuse=None):
        initializer = tf.keras.initializers.TruncatedNormal(stddev=0.075)
        # TODO: Try tf.math.exp or tf.keras.activations.exponential
        with tf.variable_scope('window', reuse=reuse):
            alpha = tf.layers.dense(inputs, self.num_mixtures,
                                    activation=tf.exp,
                                    kernel_initializer=initializer,
                                    name='alpha')
            beta = tf.layers.dense(inputs, self.num_mixtures,
                                   activation=tf.exp,
                                   kernel_initializer=initializer, name='beta')
            kappa = tf.layers.dense(inputs, self.num_mixtures,
                                    activation=tf.exp,
                                    kernel_initializer=initializer,
                                    name='kappa')

            a = tf.expand_dims(alpha, axis=2)
            b = tf.expand_dims(beta, axis=2)
            k = tf.expand_dims(k + kappa, axis=2)

            phi = tf.exp(-np.square(self.u_range + k) * b) * a  # [batch_size, mixtures, length]
            phi = tf.reduce_sum(phi, axis=1, keep_dims=True)  # [batch_size, 1, length]

            # whether or not network finished generating sequence
            finish = tf.cast(phi[:, 0, -1] > tf.reduce_max(phi[:, 0, :-1], axis=1), tf.float32)

            return tf.squeeze(tf.matmul(phi, self.sequence), axis=1), \
                tf.squeeze(k, axis=2), \
                tf.squeeze(phi, axis=1), \
                tf.expand_dims(finish, axis=1)

    @property
    def output_size(self):
        return [self.num_letters, self.num_mixtures, 1]
