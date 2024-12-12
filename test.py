import os
import torch
print("CUDA Version:", torch.version.cuda)
print("LD_LIBRARY_PATH:", os.environ.get('LD_LIBRARY_PATH'))
print("CUDA_HOME:", os.environ.get('CUDA_HOME'))