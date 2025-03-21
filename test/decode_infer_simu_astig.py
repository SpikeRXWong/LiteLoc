import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICES'] = "5"

import logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

import torch
import time
from network import multi_process_decode
from utils.help_utils import load_yaml_infer


if __name__ == '__main__':

    yaml_file = 'infer_decode_simu_astig.yaml'  # remember to change p probability
    infer_params = load_yaml_infer(yaml_file)

    decode = torch.load(infer_params.Loc_Model.model_path)
    multi_process_params = infer_params.Multi_Process

    torch.cuda.synchronize()
    t0 = time.time()

    decode_analyzer = multi_process_decode.CompetitiveSmlmDataAnalyzer_multi_producer(
        loc_model=decode,
        tiff_path=multi_process_params.image_path,
        output_path=multi_process_params.save_path,
        time_block_gb=multi_process_params.time_block_gb,
        batch_size=multi_process_params.batch_size,  # 96
        sub_fov_size=multi_process_params.sub_fov_size,  # 336
        over_cut=multi_process_params.over_cut,
        multi_GPU=multi_process_params.multi_gpu,
        num_producers=multi_process_params.num_producers,
        # num_producers should be divisible by num_consumers, e.g. num_consumers=8, num_producers can be 1,2,4,8; if num_consumers=7, num_producers can be 1 or 7.
    )

    torch.cuda.synchronize()
    t1 = time.time()

    print('init time: ' + str(t1 - t0))

    decode_analyzer.start()
    print('analyze time: ' + str(time.time() - t1))