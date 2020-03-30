# robocomp-dl

Generic deep learning component for [robocomp](https://github.com/robocomp/robocomp).
---

The repository contains 2 components that demonstrate use of deep learning along with robocomp. 

## Server Component
This component hosts deep learning project that can be used by other components. It implements an interface called `DLServer`. In this specific component, the deep learning model is a ConvNet that can classify handwritten digits from [MNIST dataset](http://yann.lecun.com/exdb/mnist/). Therefore, the interface `DLServer` expects set of images as an input and returns probability scores corresponding to each class for every image. (If the image belongs to class `1`, the returned probability scores would look something like `[0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]` since there are 10 digits) Inferring class label based on probability scores is left to client.

## Client Component
This is an example component that demonstrates use of "server" component described above. In this specific component, the "client" creates a PyTorch [dataloader](https://pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader) and keeps sending 1 image to the server for inference. The client can infer from the returned class probabilities by choosing the maximum value as class label. For example, if the server returns `[0.1, 0.02, 0.02, 0.95, 0.5, 0.1, 0.0, 0.0, 0.0, 0.0]`, the client can conclude that the input image belongs to class `3`. Inferring at client component is especially useful when the algorithm uses different evaluation techniques for inferring class labels. 

### Installation
1. Make sure robocomp is installed properly. Follow instructions [here](https://github.com/robocomp/robocomp#installation-from-source) to correctly install robocomp.
2. Put `DLServer.idsl` at `/opt/robocomp/interfaces/IDSLs/DLServer.idsl`.
3. Use command `robocompdsl IDSLs/DLServer.idsl DLServer.ice` in `/opt/robocomp/interfaces/` directory and make sure `DLServer.ice` is present in `/opt/robocomp/interfaces/` folder.
4. Switch to `server` directory from this repo and run `python src/dl_server.py etc/config` to start the server.
5. Open another terminal, go to `client` directory from this repo and run `python src/dl_client.py etc/config` to start the client.

In case of further modifications (say to adapt this component to "Voice recognition"), you can start by modifying `DLServer.idsl` to match the requirements. Then you will have to regenerate the `server` component with this new IDSL. After you've finalized the model and modified relevant files from the new `server` component, you will need to regenerate `.ice` file before you can finally test it.
