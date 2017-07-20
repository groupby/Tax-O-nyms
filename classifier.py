import argparse
import sys

import tensorflow as tf
import dataReader as input_data
FLAGS = None


def main(_):
  # Import data
  input_data.read('sample.data')

  # Create the model
  learnningRate = 0.02;


  batchSize = 100;
  iteration = 1000;

  dimension = 10;
  category = 5;
  hidden1 = 2;
  x = tf.placeholder(tf.float32, [None, dimension])
  W1 = tf.Variable(tf.zeros([dimension, hidden1]))
  W2 = tf.Variable(tf.zeros([hidden1, category]))
  b1 = tf.Variable(tf.zeros([hidden1]))
  b2 = tf.Variable(tf.zeros([category]))

  saver = tf.train.Saver()

  layer1 = tf.matmul(x, W1) + b1;
  layer1 = tf.nn.tanh(layer1);
  y = tf.matmul(layer1, W2) + b2;

  y_ = tf.placeholder(tf.float32, [None, category])

  cross_entropy = tf.reduce_mean(
      tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
  train_step = tf.train.GradientDescentOptimizer(learning_rate = learnningRate).minimize(cross_entropy)

  sess = tf.InteractiveSession()
  tf.global_variables_initializer().run()
  # Train
  for _ in range(iteration):
    batch_xs, batch_ys = input_data.next_batch(batchSize)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

  saver.save(sess, "./model/a")


  # Test trained model
  correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  print(sess.run(accuracy, feed_dict={x: input_data.test['x'],
                                      y_: input_data.test['y']}))

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_dir', type=str, default='/tmp/tensorflow/mnist/input_data',
                      help='Directory for storing input data')
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)