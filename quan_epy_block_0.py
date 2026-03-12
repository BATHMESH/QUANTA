import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self, n_bits=4, v_max=1.0, v_min=-1.0):
        gr.sync_block.__init__(
            self,
            name='Mid-Tread Quantizer',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.n_bits = n_bits
        self.v_max = v_max
        self.v_min = v_min
        self.L = 2**n_bits
        self.delta = (v_max - v_min) / self.L

    def work(self, input_items, output_items):
        in0 = input_items[0]
        # Implementation of mid-tread logic: round(x/delta) * delta
        # We also clip the signal to prevent overflow outside Vmin/Vmax
        quantized = np.round(in0 / self.delta) * self.delta
        output_items[0][:] = np.clip(quantized, self.v_min, self.v_max)
        return len(output_items[0])