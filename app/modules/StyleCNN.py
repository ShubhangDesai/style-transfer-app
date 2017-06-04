import torch.nn as nn

class StyleCNN(object):
    def __init__(self):
        super(StyleCNN, self).__init__()

        self.use_cuda = torch.cuda.is_available()

        final_linear = nn.Linear(256, 32)
        torch.randn(final_linear.weight.size(), out=final_linear.weight.data).mul_(0.01)
        final_linear.bias.data.mul_(0.01)
        final_linear.bias.data[:16].add_(1)
        self.normalization_network = nn.Sequential(nn.Conv2d(3, 32, 9, stride=2, padding=0),
                                                   nn.Conv2d(32, 64, 9, stride=2, padding=0),
                                                   nn.Conv2d(64, 128, 9, stride=2, padding=0),
                                                   Flatten(),
                                                   nn.Linear(625, 256),
                                                   final_linear
                                                   )

        self.transform_network = nn.Sequential(nn.ReflectionPad2d(40),
                                               nn.Conv2d(3, 32, 9, stride=1, padding=4),
                                               nn.Conv2d(32, 64, 3, stride=2, padding=1),
                                               nn.Conv2d(64, 128, 3, stride=2, padding=1),
                                               nn.Conv2d(128, 128, 3, stride=1, padding=0),
                                               nn.Conv2d(128, 128, 3, stride=1, padding=0),
                                               nn.Conv2d(128, 128, 3, stride=1, padding=0),
                                               nn.Conv2d(128, 128, 3, stride=1, padding=0),
                                               nn.Conv2d(128, 128, 3, stride=1, padding=0),
                                               nn.Conv2d(128, 128, 3, stride=1, padding=0),
                                               nn.Conv2d(128, 128, 3, stride=1, padding=0),
                                               nn.Conv2d(128, 128, 3, stride=1, padding=0),
                                               nn.Conv2d(128, 128, 3, stride=1, padding=0),
                                               nn.Conv2d(128, 128, 3, stride=1, padding=0),
                                               nn.ConvTranspose2d(128, 64, 3, stride=2, padding=1, output_padding=1),
                                               nn.ConvTranspose2d(64, 32, 3, stride=2, padding=1, output_padding=1),
                                               nn.Conv2d(32, 3, 9, stride=1, padding=4),
                                               )

        try:
            self.transform_network.load_state_dict(torch.load("models/transform_net_ckpt"))
            self.normalization_network.load_state_dict(torch.load("models/normalization_net_ckpt"))
        except(IOError):
            pass

        self.out_dims = [32, 64, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 64, 32, 3]

        if self.use_cuda:
            self.normalization_network.cuda()

    def eval(self, content, style):
        norm_params = self.normalization_network.forward(style)
        N = norm_params.size(1)

        idx = 0
        for layer in list(self.transform_network):
            if idx != 0:
                out_dim = self.out_dims[idx - 1]
                weight = norm_params[:out_dim, idx - 1].data
                bias = norm_params[:out_dim, idx + int(N/2) - 1].data
                instance_norm = LearnedInstanceNorm2d(out_dim, Parameter(weight), Parameter(bias))

                layers = nn.Sequential(*[layer, instance_norm, nn.ReLU()])
            else:
                layers = nn.Sequential(layer)

            if self.use_cuda:
                layers.cuda()

            content = layers(content)
            idx += 1

        content.data.clamp_(0, 255)
        return content

class Flatten(nn.Module):
    def __init__(self):
        super(Flatten, self).__init__()

    def forward(self, input):
        N, C, H, W = input.size()
        output = input.view(N * C, H * W)
        return output
