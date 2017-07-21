import argparse
import sys
import time


import tensorflow as tf
import dataReader as input_data
FLAGS = None


def main(_):

  start = time.time()
  # Import data
  input_data.read('output2')

  # Create the model
  learnningRate = 3;


  batchSize = 100;
  iteration = 100000;

  dimension = 300;
  category = 9;
  hidden1 = 100;
  x = tf.placeholder(tf.float32, [None, dimension])
  W1 = tf.Variable(tf.zeros([dimension, category]))
  # W2 = tf.Variable(tf.zeros([hidden1, category]))
  b1 = tf.Variable(tf.zeros([category]))
  # b2 = tf.Variable(tf.zeros([category]))

  saver = tf.train.Saver()

  # layer1 = tf.matmul(x, W1) + b1;
  # layer1 = tf.nn.tanh(layer1);
  # y = tf.matmul(layer1, W2) + b2;
  y = tf.matmul(x, W1) + b1;

  y_ = tf.placeholder(tf.float32, [None, category])

  cross_entropy = tf.reduce_mean(
      tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
  train_step = tf.train.GradientDescentOptimizer(learning_rate = learnningRate).minimize(cross_entropy)

  correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

  with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    # saver.restore(sess, "./model/a")
    for i in range(iteration):
      batch = input_data.next_batch(batchSize)
      if i % 1000 == 0:
        train_accuracy = accuracy.eval(feed_dict={
            x: batch[0], y_: batch[1]})
        print('step %d, training accuracy %g' % (i, train_accuracy))
      if i % 10000 == 0:
        train_accuracy = accuracy.eval(feed_dict={
            x: input_data.test['x'], y_: input_data.test['y']})
        print('step %d, test accuracy %g' % (i, train_accuracy))
      train_step.run(feed_dict={x: batch[0], y_: batch[1]})

    print('test accuracy %g' % accuracy.eval(feed_dict={
        x: input_data.test['x'], y_: input_data.test['y']}))
    saver.save(sess, "./model/a")

  # sess = tf.InteractiveSession()
  # tf.global_variables_initializer().run()
  # # Train
  # for _ in range(iteration):
  #   batch_xs, batch_ys = input_data.next_batch(batchSize)
  #   sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

  # saver.save(sess, "./model/a")

  # end = time.time()
  # print end - start

  # # Test trained model
  # correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
  # accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  # print(sess.run(accuracy, feed_dict={x: input_data.test['x'],
  #                                     y_: input_data.test['y']}))

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_dir', type=str, default='/tmp/tensorflow/mnist/input_data',
                      help='Directory for storing input data')
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)