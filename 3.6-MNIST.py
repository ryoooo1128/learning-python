from os import path, pardir

current_dir = path.abspath(path.dirname('3.6-MNIST')) 
parent_dir = path.abspath(path.join(current_dir, pardir)) 
parent_parent_dir = path.abspath(path.join(parent_dir, pardir)) 

print(current_dir)
print(parent_dir)
print(parent_parent_dir)


import mnist

(x_train, t_train), (x_test, t_test) = mnist.load_mnist(flatten=True, normalize=False)

print(x_test.shape)