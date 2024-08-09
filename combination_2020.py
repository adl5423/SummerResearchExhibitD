```python
from __future__ import absolute_import, division, print_function, unicode_literals

import functools
import tensorflow as tf
import tensorflow.compat.v1 as tf1
import tensorflow as tf2
from tensorflow import compat

from tensorflow.python.eager import context
from tensorflow.python.framework import ops_v2 as ops
from tensorflow.python.keras.testing_utils import test_combinations
from tensorflow.python.util import tf_export

tf1.disable_v2_behavior()

class EagerGraphCombination(test_combinations.TestCombination):
  """Run the test in Graph or Eager mode.

  The optional `mode` parameter controls the test's execution mode.  Its
  accepted values are "graph" or "eager" literals.
  """

  def context_managers(self, kwargs):
    """Handle context managers with given keyword arguments."""
    mode = kwargs.pop("mode", None)
    if mode is None: return
    if mode == "graph":
      return [ops.Graph().as_default()]
    elif mode == "eager":
      return [context.eager_mode()]
    raise ValueError(f"'mode' has to be either 'eager' or 'graph' and not {mode}")

  def parameter_modifiers(self):
    """Modify parameters of the object."""

  def should_execute_combination(self, kwargs):
    """Determine if the combination should be executed."""

class TFVersionCombination(test_combinations.TestCombination):
  """Control the execution of the test in TF1.x and TF2.

  If TF2 is enabled then a test with TF1 test is going to be skipped and vice
  versa.

  Test targets continuously run in TF2 thanks to the tensorflow.v2 TAP target.
  A test can be run in TF2 with bazel by passing --test_env=TF2_BEHAVIOR=1.
  """

  def context_managers(self, kwargs):
    tf_api_version = kwargs.pop("tf_api_version", None)
    if tf_api_version == 1 and tf2.enabled(): return 1
    if tf_api_version == 2: return 2
    raise ValueError(f"Invalid tf_api_version: {tf_api_version}")

  def parameter_modifiers(self):
    """Modify parameters of the object."""

  def should_execute_combination(self, kwargs):
    """Determine if the combination should be executed."""

def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(512, activation='relu', input_shape=(784,)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def train_model(model, train_images, train_labels):
    model.fit(train_images, train_labels, epochs=5)

def main():
    mnist = tf.keras.datasets.mnist
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
    train_images = train_images / 255.0
    test_images = test_images / 255.0
    
    model = create_model()
    train_model(model, train_images, train_labels)
    model.evaluate(test_images, test_labels, verbose=2)

if __name__ == '__main__':
    main()

generate = functools.partial(test_combinations.generate,
                             test_combinations=(EagerGraphCombination(),
                                                TFVersionCombination()))
tf_export("__internal__.test.combinations.generate", v1=[])(generate)
combine = test_combinations.combine
times = test_combinations.times
NamedObject = test_combinations.NamedObject
```