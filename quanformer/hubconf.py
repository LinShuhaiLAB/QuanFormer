# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import torch

from quanformer.models.backbone import Backbone, Joiner
from quanformer.models.detr import DETR, PostProcess
from quanformer.models.position_encoding import PositionEmbeddingSine
from quanformer.models.transformer import Transformer

dependencies = ["torch", "torchvision"]


def _make_former(backbone_name: str, dilation=False, num_classes=1, mask=False):
    hidden_dim = 256
    backbone = Backbone(backbone_name, train_backbone=True, return_interm_layers=mask, dilation=dilation)
    pos_enc = PositionEmbeddingSine(hidden_dim // 2, normalize=True)
    backbone_with_pos_enc = Joiner(backbone, pos_enc)
    backbone_with_pos_enc.num_channels = backbone.num_channels
    transformer = Transformer(d_model=hidden_dim, num_encoder_layers=1, num_decoder_layers=1, return_intermediate_dec=True)
    detr = DETR(backbone_with_pos_enc, transformer, num_classes=num_classes, num_queries=3)
    return detr


def quan_former(num_classes=1, return_postprocessor=False):
    """
    DETR R50 with 1 encoder and 1 decoder layers.

    Achieves 42/62.4 AP/AP50 on COCO val5k.
    """
    model = _make_former( "resnet50", dilation=False, num_classes=num_classes)
    if return_postprocessor:
        return model, PostProcess()
    return model




