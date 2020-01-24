def sepia(img):
    h, w, _ = img.shape

    for i in range(h):
        for j in range(w):
            s = sum(img[i, j]) // 3
            k = 10
            img[i, j, :] = (s+k*2, s+k, s)

    return img


def black_white(img):
    h, w, _ = img.shape

    for i in range(h):
        for j in range(w):
            s = sum(img[i, j]) // 3
            img[i, j, :] = (s, s, s)

    return img


def negative(img):
    h, w, _ = img.shape

    for i in range(h):
        for j in range(w):
            img[i, j, :] = [255-img[i, j, 0], 255-img[i, j, 1], 255-img[i, j, 2]]

    return img

