attempts at style transfer using GPU optimized EC2 with the following:

- DeepPy
- CUDArray with cuDNN
- imagenet-vgg-verydeep-19.


# Get Cuda:

## Install build essential
```
$ sudo apt-get update
$ sudo apt-get install build-essential
$ sudo apt-get install gcc make
$ sudo apt-get install linux-image-extra-virtual
$ sudo apt-get install xorg
$ sudo apt-get install pkg-config
$ sudo reboot
```

## Get Cuda Installer:
```
wget http://developer.download.nvidia.com/compute/cuda/7.5/Prod/local_installers/cuda_7.5.18_linux.run
```

## Extract Cuda Installer:
```
$ chmod +x cuda_7.5.18_linux.run
$ mkdir nvidia_installers
$ ./cuda_7.5.18_linux.run -extract=`pwd`/nvidia_installers
```

## Do some stuff to fix installer:
```
$ sudo nano /etc/modprobe.d/blacklist-nouveau.conf
blacklist nouveau
blacklist lbm-nouveau
options nouveau modeset=0
alias nouveau off
alias lbm-nouveau off
```
```
$   sudo echo options nouveau modeset=0 | sudo tee -a /etc/modprobe.d/nouveau-kms.conf
$ sudo update-initramfs -u
$ sudo reboot
```

## One more try:
```
$ sudo apt-get install linux-source
$ sudo apt-get install linux-headers-3.13.0-37-generic
```

## Run Nvidia driver installer:
```
$ cd nvidia_installers
$ ./NVIDIA-Linux-x86_64-352.39.run
```
# it works!
## Load nvidia kernel module:
```
$ modprobe nvidia
```
## Run CUDA + samples installer:
```
$ sudo ./cuda-linux64-rel-6.5.14-18749181.run
$ sudo ./cuda-samples-linux-6.5.14-18745345.run
```


Install cudNN:
scp -i  ~/.ssh/<your_pem>.pem ~/Downloads/<your_cudnn>.tar.gz ubuntu@<ip_address>:/home/ubuntu

gzip -d file.tar.gz
tar xf file.tar

echo -e "\nexport LD_LIBRARY_PATH=/home/ubuntu/cudnn-6.5-linux-x64-v2:$LD_LIBRARY_PATH" >> ~/.bashrc

sudo cp cudnn.h /usr/local/cuda-<version>/include
sudo cp libcudnn* /usr/local/cuda-<version/lib64
