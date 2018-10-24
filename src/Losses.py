from keras import backend as K


def custom_distance(y_true, y_pred):
    return K.sum(K.square(y_pred - y_true), axis=-1)