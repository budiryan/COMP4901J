import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  denominator = 0
  num_train = X.shape[0]
  num_classes = W.shape[1]
  for i in xrange(num_train):
    scores = X[i].dot(W) # predict a matrix of shape (1, C)
    denominator = 0
    # prevent gradient explosion
    scores -= np.max(scores)
    for j in xrange(num_classes):
      denominator += np.exp(scores[j])
    correct_score = scores[y[i]]
    loss += -1 * np.log(np.exp(correct_score) / denominator)
    for j in xrange(num_classes):
      numerator = np.exp(scores[j])
      probability = numerator / denominator
      # Reference: https://math.stackexchange.com/questions/945871/derivative-of-softmax-loss-function
      if j == y[i]:
        # For matching class 
        dW[:,j] += (-X[i].T * (1 - probability))
      else:
        # For non-matching class
        dW[:,j] += X[i].T * probability
  
  loss /= num_train
  dW /= num_train
  # add regularization
  loss += reg * np.sum(W * W)
  dW += 2 * reg * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train = X.shape[0]
  num_classes = W.shape[1]
  scores = X.dot(W)
  scores -= np.max(scores, axis=1)[:, np.newaxis]
  denominators = np.sum(np.exp(scores), axis=1)
  correct_scores = scores[range(num_train), y]
  loss = np.sum(-1 * np.log(np.exp(correct_scores) / denominators)) / num_train
  numerators = np.exp(scores)
  probabilities = numerators / denominators[:, np.newaxis]
  probabilities[range(num_train), y] -= 1
  dW = X.T.dot(probabilities) / num_train

  # add regularization
  loss += 0.5 * reg * np.sum(W * W)
  dW += reg * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW
