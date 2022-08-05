from types import MethodType

import cPickle as pickle
import copy_reg


def pickle_method(method):
    if method.im_self is None:
        return getattr, (method.im_class, method.im_func.func_name)
    else:
        return getattr, (method.im_self, method.im_func.func_name)


copy_reg.pickle(MethodType, pickle_method)