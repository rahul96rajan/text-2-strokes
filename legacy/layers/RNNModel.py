import tensorflow as tf


class RNNModel(tf.compat.v1.nn.rnn_cell.RNNCell):
    def __init__(self, layers, num_units, input_size, num_letters, batch_size, window_layer):
        super(RNNModel, self).__init__()
        self.layers = layers
        self.num_units = num_units
        self.input_size = input_size
        self.num_letters = num_letters
        self.window_layer = window_layer
        self.last_phi = None

        with tf.compat.v1.variable_scope('rnn', reuse=None):
            self.lstms = [tf.nn.rnn_cell.LSTMCell(num_units)
                          for _ in range(layers)]
            self.states = [tf.Variable(tf.zeros([batch_size, s]), trainable=False)
                           for s in self.state_size]

            self.zero_states = tf.group(*[sp.assign(sc)
                                          for sp, sc in zip(self.states,
                                                            self.zero_state(batch_size, dtype=tf.float32))])

    @property
    def state_size(self):
        return [self.num_units] * self.layers * 2 + self.window_layer.output_size

    @property
    def output_size(self):
        return [self.num_units]

    def call(self, inputs, state, **kwargs):
        # state[-3] --> window
        # state[-2] --> k
        # state[-1] --> finish
        # state[2n] --> h
        # state[2n+1] --> c
        window, k, finish = state[-3:]
        output_state = []
        prev_output = []

        for layer in range(self.layers):
            x = tf.concat([inputs, window] + prev_output, axis=1)
            with tf.variable_scope('lstm_{}'.format(layer)):
                output, s = self.lstms[layer](x, tf.nn.rnn_cell.LSTMStateTuple(state[2 * layer],
                                                                               state[2 * layer + 1]))
                prev_output = [output]
            output_state += [*s]

            if layer == 0:
                window, k, self.last_phi, finish = self.window_layer(output, k)

        return output, output_state + [window, k, finish]