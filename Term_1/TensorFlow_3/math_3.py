# Solution is available in the other "solution.py" tab
import tensorflow as tf

x_ = 10
y_ = 2
one_ = 1
# z = x/y - 1


def run():
    r"""
    Calculating

    .. math::

        z = \frac{x}{y}-1

    using TensorFlow

    Returns
    -------
        output: numpy.int32
    """
    x = tf.constant(x_)
    y = tf.constant(y_)
    one = tf.constant(one_)

    first_div = tf.div(x, y)
    z = tf.sub(first_div, one)

    with tf.Session() as sess:
        output = sess.run(z)

    return output


if __name__ == '__main__':
    print(run())
