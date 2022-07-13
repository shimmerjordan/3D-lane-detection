# Install

```shell
conda create -n ganet python=3.7 -y
conda activate ganet
conda install pytorch==1.6.0 torchvision==0.7.0 cudatoolkit=10.1 -c pytorch -y
pip install -r requirements/build.txt
```

# Train

```shell
CUDA_LAUNCH_BLOCKING=1 ./dist_train.sh tusimple final_exp_res18_s8 /data/output/ganet
```

# Test

```shell
bash dist_test.sh tusimple final_exp_res18_s8 /data/output/ganet/tusimple/final_exp_res18_s8/latest.pth /data/vis/ganet/ori/tusimple --show
```


