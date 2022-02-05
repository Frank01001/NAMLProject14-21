from svm.one_to_one.svm_oto_classifier import *
import numpy as np

genre_names = ['blues', 'classical', 'country', 'disco', 'hipop', 'jazz', 'metal', 'pop', 'reggae', 'rock']


class PrimalFeatureMapClassifier(SVMClassifier):
  def __init__(self, genre1, genre2):
    super().__init__(genre1, genre2)
    feature_size = 9
    self.w = np.zeros(feature_size)
    self.b = 0
    self.learning_rate = 0.02
    self.num_epochs = 200

  def bin_classify(self, input):
    return self.genre1 if self.internal_classify(input) >= 0 else self.genre2

  def train(self, x, y):
    class1_data = x[y == genre_names.index(self.genre1)]
    class2_data = x[y == genre_names.index(self.genre2)]

    total_samples_count = x.shape[0]

    class1_samples_count = class1_data.shape[0]
    class2_samples_count = class2_data.shape[0]

    for epoch in range(self.num_epochs):
      gradient_w = np.zeros(self.w.size)
      gradient_b = 0

      for sample_index in range(class1_samples_count):
        phi_1 = PrimalFeatureMapClassifier.phi(class1_data[sample_index, :])
        gradient_w += self.hinge_derivative_w(phi_1, 1)
        gradient_b += self.hinge_derivative_b(phi_1, 1)

      for sample_index in range(class2_samples_count):
        phi_2 = PrimalFeatureMapClassifier.phi(class2_data[sample_index, :])
        gradient_w += self.hinge_derivative_w(phi_2, -1)
        gradient_b += self.hinge_derivative_b(phi_2, -1)

      gradient_w /= total_samples_count
      gradient_b /= total_samples_count

      self.w -= self.learning_rate * gradient_w
      self.b -= self.learning_rate * gradient_b

    confusion_mat = np.zeros((2, 2))

    for test_index in range(class1_samples_count):
      predicted = 0 if self.internal_classify(class1_data[test_index, :]) >= 0 else 1
      confusion_mat[0, predicted] += 1

    for test_index in range(class2_samples_count):
      predicted = 0 if self.internal_classify(class2_data[test_index, :]) >= 0 else 1
      confusion_mat[1, predicted] += 1

    print() # Newline
    print(" - Accuracy: " + str(confusion_mat.trace() / np.sum(confusion_mat)))
    print()  # Newline

  def set_learning_rate(self, val):
    self.learning_rate = val

  def set_num_epochs(self, val):
    self.num_epochs = val

  # Utils
  def internal_classify(self, x):
    phi = PrimalFeatureMapClassifier.phi(x)
    return np.dot(self.w, phi) - self.b

  def hingeloss(self, x, y):
    prod = y * self.internal_classify(x)

    if prod >= 1:
      return 0
    else:
      return 1 - prod

  def hinge_derivative_w(self, x, y):
    prod = y * self.internal_classify(x)
    prod_elem = y * x
    if prod >= 1:
      return np.zeros(x.shape[0])
    else:
      return -prod_elem

  def hinge_derivative_b(self, x, y):
    prod = y * self.internal_classify(x)
    if prod >= 1:
      return 0
    else:
      return y

  @staticmethod
  def phi(x):
    f1 = x[0]
    f2 = x[1]
    f3 = x[2]
    return np.array([f1, f2, f3, f1 ** 2, f2 ** 2, f3 ** 2, f1 * f2, f2 * f3, f1 * f3])