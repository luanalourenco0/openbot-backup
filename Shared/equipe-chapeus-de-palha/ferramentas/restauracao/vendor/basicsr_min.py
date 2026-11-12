# Substituto minimo do pacote `basicsr`, so com o que os arquivos copiados em vendor/ precisam.
# Trechos derivados do BasicSR (Copyright 2018-2020 BasicSR Authors, licenca Apache-2.0; texto no LICENSE-GFPGAN.txt).
# Modificado: reduzido a Registry, default_init_weights, make_layer e pixel_unshuffle, sem dependencias alem do torch.
import torch
from torch import nn as nn
from torch.nn import init as init
from torch.nn.modules.batchnorm import _BatchNorm


class Registry:
    def __init__(self, name):
        self._name = name
        self._obj_map = {}

    def register(self, obj=None, suffix=None):
        def deco(func_or_class):
            name = func_or_class.__name__
            if suffix is not None:
                name = f"{name}_{suffix}"
            self._obj_map[name] = func_or_class
            return func_or_class

        if obj is None:
            return deco
        return deco(obj)

    def get(self, name):
        return self._obj_map[name]


ARCH_REGISTRY = Registry("arch")


@torch.no_grad()
def default_init_weights(module_list, scale=1, bias_fill=0, **kwargs):
    if not isinstance(module_list, list):
        module_list = [module_list]
    for module in module_list:
        for m in module.modules():
            if isinstance(m, (nn.Conv2d, nn.Linear)):
                init.kaiming_normal_(m.weight, **kwargs)
                m.weight.data *= scale
                if m.bias is not None:
                    m.bias.data.fill_(bias_fill)
            elif isinstance(m, _BatchNorm):
                init.constant_(m.weight, 1)
                if m.bias is not None:
                    m.bias.data.fill_(bias_fill)


def make_layer(basic_block, num_basic_block, **kwarg):
    layers = []
    for _ in range(num_basic_block):
        layers.append(basic_block(**kwarg))
    return nn.Sequential(*layers)


def pixel_unshuffle(x, scale):
    b, c, hh, hw = x.size()
    out_channel = c * (scale ** 2)
    assert hh % scale == 0 and hw % scale == 0
    h = hh // scale
    w = hw // scale
    x_view = x.view(b, c, h, scale, w, scale)
    return x_view.permute(0, 1, 3, 5, 2, 4).reshape(b, out_channel, h, w)
