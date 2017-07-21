import gensim
import tensorflow as tf
import numpy as np

def getCategory(values):
    index = np.argmax(values)
    cat = [
        "baby & child",
        "beauty",
        "diet & nutrition",
        "health & medicine",
        "home health care",
        "household & grocery",
        "personal care",
        "sexual health",
        "vitamins"
    ]
    print(cat[index])


def main(_):
    # Load Google's pre-trained Word2Vec model.
    model = gensim.models.KeyedVectors.load_word2vec_format('./models/GoogleNews-vectors-negative300.bin', binary=True)
    # Create the model
    learnningRate = 3;


    batchSize = 1;
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

    with tf.Session() as sess:
        while True:
            inputWord = input('Search term:')
            testRunData = [model[inputWord]]
            # sess.run(tf.global_variables_initializer())
            saver.restore(sess, "./model_92/a")
            # testRunData = np.reshape(testRunData,(1, dimension))
            print("Running")
            # c = tf.constant(1.0)
            c = tf.abs(y)
            # sess.run(y, feed_dict={x: testRunData})
            result = c.eval(feed_dict={x: testRunData}, session=sess)
            temp = np.exp(result-np.max(result))
            result = (temp/temp.sum())*100
            print(result)
            getCategory(result)

main("test")
