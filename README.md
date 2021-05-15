A Novel Evaluation to GANs
=============
This is an example of computing the Likeness Score: LS on datasets of real images and generated images by GANs.

It includes codes to compute the ***2-class*** distance-based separability index (DSI). **LS=1-DSI**. There are two versions (CPU and GPU).

Related paper
=============
### A Novel Measure to Evaluate Generative Adversarial Networks Based on Direct Analysis of Generated Images

`Citation` Guan, S., Loew, M. A novel measure to evaluate generative adversarial networks based on direct analysis of generated images. Neural Comput & Applic (2021). doi: 10.1007/s00521-021-06031-5.

[`Paper`](https://doi.org/10.1007/s00521-021-06031-5)  [`Arxiv`](https://arxiv.org/abs/2002.12345)

Time Complexity
=============
Data: 2000 real images and 2000 generated images from CIFAR-10 dataset (32x32 RGB images); CPU: i7-6900K; GPU: GTX 1080Ti

- `CPU ver.` 110.859 s
- `GPU ver.` 2.406   s
