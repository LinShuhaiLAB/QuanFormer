import pickle
from pathlib import Path
from PIL import Image
from natsort import natsorted
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import torchvision.transforms as T
from quanformer.hubconf import *
from joblib import Parallel, delayed
from utils.io_utils import time_master

torch.set_grad_enabled(False);
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# COCO classes
CLASSES = [
    'peak'
]

# colors for visualization
COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098]]

# standard PyTorch mean-std input image normalization
transform = T.Compose([
    T.Resize(800),
    T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


# for output bounding box post-processing
def box_cxcywh_to_xyxy(x):
    x_c, y_c, w, h = x.unbind(1)
    b = [(x_c - 0.5 * w), (y_c - 0.5 * h),
         (x_c + 0.5 * w), (y_c + 0.5 * h)]
    return torch.stack(b, dim=1)


def rescale_bboxes(out_bbox, size, device):
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    img_size_tensor = torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32).to(device)
    b = b * img_size_tensor
    return b


def plot_results(results, n_jobs=-1):
    # Using joblib to parallelize the processing of images
    Parallel(n_jobs=n_jobs)(
        delayed(plot_single_result)(pil_img, prob, boxes, pil_img)
        for pil_img, prob, boxes in results
    )


def plot_single_result(pil_img, prob, boxes, save_path=""):
    im = Image.open(pil_img).convert('RGB')
    plt.figure(figsize=(4, 3))
    plt.imshow(im)
    ax = plt.gca()
    colors = COLORS * 100
    for p, (xmin, ymin, xmax, ymax), c in zip(prob, boxes.tolist(), colors):
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   fill=False, color=c, linewidth=3))
        cl = p.argmax()
        text = f'{CLASSES[cl]}: {p[cl]:0.2f}'
        ax.text(xmin, ymin, text, fontsize=15,
                bbox=dict(facecolor='yellow', alpha=0.5))
    plt.axis('off')

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def predict(images_path, model, transform, threshold=0.9):
    predict_results = []
    for img in images_path:

        with Image.open(img).convert('RGB') as im:
            # mean-std normalize the input image (batch-size: 1)
            anImg = transform(im).to(device)
            im.close()
            # data = nested_tensor_from_tensor_list([anImg])

            # propagate through the model
            outputs = model([anImg])

            # keep only predictions with 0.9+ confidence
            probas = outputs['pred_logits'].softmax(-1)[0, :, :-1]
            keep = probas.max(-1).values > threshold
            # convert boxes from [0; 1] to image scales
            bboxes_scaled = rescale_bboxes(outputs['pred_boxes'][0, keep], im.size, device)
            predict_results.append((img, probas[keep].cpu().detach().numpy(), bboxes_scaled.cpu().detach().numpy()))

    return predict_results

@time_master
def build_predictor(model_path, images_path, threshold, plot=False):
    model = quan_former()
    state_dict = torch.load(model_path, map_location='cpu')
    model.to(device)
    model.load_state_dict(state_dict["model"])
    model.eval()

    p = Path(images_path).resolve()
    suffix = 'jpeg'
    paths = [str(path) for path in p.rglob(f"*.{suffix}")]
    path = natsorted(paths)
    pre_results = predict(path, model, transform, threshold)
    if plot:
        plot_results(pre_results)
    return pre_results


if __name__ == "__main__":
    import time
    start = time.time()

    images_path = '/home/zzy/peak-output/Test/SA2'
    model_path = '/home/zzy/data/peak-ciou-all113-res/checkpoint0029.pth'

    results = build_predictor(model_path, images_path, threshold=0.9, plot=False)
    # FALSE 969
    # TRUE 15961
    with open('/home/zzy/results-true.pkl', 'wb') as f:
        pickle.dump(results, f)
    count = 0
    for each in results:
        if each[1].size > 0:
            count += 1
    print(count)
    print(time.time() - start)


