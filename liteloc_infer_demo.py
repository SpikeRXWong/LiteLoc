import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICES'] = "2"

import torch
import time
import analyzer


if __name__ == '__main__':

    model_path = "./training_model/liteloc_spline_tetra6/checkpoint.pkl"
    liteloc = torch.load(model_path)

    image_path = "/home/feiyue/LiteLoc_spline/spline_data/hsnr_ld_spline_tetra6.tif"
    save_path = "/home/feiyue/LiteLoc_spline/spline_data/liteloc_hsnr_ld_spline_tetra6.csv"

    torch.cuda.synchronize()
    t0 = time.time()

    liteloc_analyzer = analyzer.CompetitiveSmlmDataAnalyzer_multi_producer(
        loc_model=liteloc,
        tiff_path=image_path,
        output_path=save_path,
        time_block_gb=0.5,  # todo: to be adaptable
        batch_size=100,  # 96  # todo
        sub_fov_size=128,  # 336  # todo
        over_cut=8,
        multi_GPU=False,
        end_frame_num=None,
        num_producers=1,
        # num_producers should be divisible by num_consumers, e.g. num_consumers=8, num_producers can be 1,2,4,8; if num_consumers=7, num_producers can be 1 or 7.
    )

    torch.cuda.synchronize()
    t1 = time.time()

    print('init time: ' + str(t1 - t0))

    liteloc_analyzer.start()
    print('analyze time: ' + str(time.time() - t1))
