import numpy as  np
import xarray as xr

import scipy
import numpy as np

import cv2

import os


def Gradient(img, order):
    """ calculate x, y gradient and magnitude """
    sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3)
    sobelx = sobelx/8.0
    sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=3)
    sobely = sobely/8.0
    sobel_norm = np.sqrt(sobelx*sobelx+sobely*sobely)
    if (order==0):
        return sobelx
    elif (order==1):
        return sobely
    else:
        return sobel_norm


def hanning2d(M, N):
    """
    A 2D hanning window, as per IDL's hanning function.  See numpy.hanning for the 1d description
    """

    if N <= 1:
        return np.hanning(M)
    elif M <= 1:
        return np.hanning(N)  # scalar unity; don't window if dims are too small
    else:
        return np.outer(np.hanning(M), np.hanning(N))


def cart2pol(x, y):
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return (phi, rho)


def Imputing_NaN(data, invalid=None):
    """
    Replace the value of invalid 'data' cells (indicated by 'invalid')
    by the value of the nearest valid data cell
    """
    import scipy.ndimage as nd
    if invalid is None: invalid = np.isnan(data)
    ind = nd.distance_transform_edt(invalid, return_distances=False, return_indices=True)
    return data[tuple(ind)]


def raPsd2dv1(img, res, hanning):
    """ Computes and plots radially averaged power spectral density (power
     spectrum) of image IMG with spatial resolution RES.
    """
    img = img.copy()
    N, M = img.shape
    if hanning:
        img = hanning2d(*img.shape) * img
    img = Imputing_NaN(img)
    imgf = np.fft.fftshift(np.fft.fft2(img))
    imgfp = np.power(np.abs(imgf) / (N * M), 2)
    # Adjust PSD size
    dimDiff = np.abs(N - M)
    dimMax = max(N, M)
    if (N > M):
        if ((dimDiff % 2) == 0):
            imgfp = np.pad(imgfp, ((0, 0), (int(dimDiff / 2), int(dimDiff / 2))), 'constant', constant_values=np.nan)
        else:
            imgfp = np.pad(imgfp, ((0, 0), (int(dimDiff / 2), 1 + int(dimDiff / 2))), 'constant',
                           constant_values=np.nan)

    elif (N < M):
        if ((dimDiff % 2) == 0):
            imgfp = np.pad(imgfp, ((int(dimDiff / 2), int(dimDiff / 2)), (0, 0)), 'constant', constant_values=np.nan)
        else:
            imgfp = np.pad(imgfp, ((int(dimDiff / 2), 1 + int(dimDiff / 2)), (0, 0)), 'constant',
                           constant_values=np.nan)
    halfDim = int(np.ceil(dimMax / 2.))
    X, Y = np.meshgrid(np.arange(-dimMax / 2., dimMax / 2. - 1 + 0.00001),
                       np.arange(-dimMax / 2., dimMax / 2. - 1 + 0.00001))
    theta, rho = cart2pol(X, Y)
    rho = np.round(rho + 0.5)
    Pf = np.zeros(halfDim)
    f1 = np.zeros(halfDim)
    for r in range(halfDim):
        Pf[r] = np.nansum(imgfp[rho == (r + 1)])
        f1[r] = float(r + 1) / dimMax
    f1 = f1 / res
    return f1, Pf


def err_raPsd2dv1(img, imgref, res, hanning):
    """ Computes and plots radially averaged power spectral density error (power
     spectrum).
    """
    f_, Pf_ = raPsd2dv1(img - imgref, res, hanning)
    Pf_ = (Pf_ / raPsd2dv1(imgref, res, hanning)[1])
    return f_, Pf_


def avg_raPsd2dv1(img3d, res, hanning):
    """ Computes and plots radially averaged power spectral density mean (power
     spectrum) of an image set img3d along the first dimension.
    """
    N = img3d.shape[0]
    for i in range(N):
        img = img3d[i, :, :]
        f_, Pf_ = raPsd2dv1(img, res, hanning)
        if i == 0:
            f, Pf = f_, Pf_
        else:
            f = np.vstack((f, f_))
            Pf = np.vstack((Pf, Pf_))
    Pf = np.mean(Pf, axis=0)
    return f_, Pf


def avg_err_raPsd2dv1(img3d, img3dref, res, hanning):
    """ Computes and plots radially averaged power spectral density error mean (power
     spectrum) of an image set img3d along the first dimension.
    """
    N = img3d.shape[0]
    for i in range(N):
        img1 = img3d[i, :, :]
        img2 = img3dref[i, :, :]
        f_, Pf_ = raPsd2dv1(img1 - img2, res, hanning)
        Pf_ = (Pf_ / raPsd2dv1(img2, res, hanning)[1])
        if i == 0:
            f, Pf = f_, Pf_
        else:
            f = np.vstack((f, f_))
            Pf = np.vstack((Pf, Pf_))
    Pf = np.mean(Pf, axis=0)
    return f_, Pf


def processUserReconstruction(rec_file,GTfile,output_dir,test_index,plot_index):
    GT = xr.open_dataset(GTfile).ssh.values[test_index]

    itrp_RECON = xr.open_dataset(rec_file).FP_GENN.values

    nrmse_RECON = np.zeros(len(GT))

    for i in range(0, len(GT)):
        gt = GT[i, :200, :200]
        RECON = itrp_RECON[i, :200, :200]
        nrmse_RECON[i] = (np.sqrt(np.nanmean(((gt - np.nanmean(gt)) - (RECON - np.nanmean(RECON))) ** 2))) / np.nanstd(gt)

    # plot nRMSE time series
    N = len(GT)

    # Plot averaged normalize error RAPS

    f0, Pf_RECON = avg_err_raPsd2dv1(itrp_RECON[:, :200, :200], GT[:, :200, :200], 4, True)
    wf0 = 1 / f0

    rms_seq = np.vstack((range(N), nrmse_RECON))
    np.savez(os.path.join(output_dir,"rms_plot.npz"), rms_seq)
    print("RMS data generated...")

    freq_seq = np.vstack((wf0[1:], Pf_RECON[1:]))
    np.savez(os.path.join(output_dir,"freq_plot.npz"), freq_seq)
    print("Frequency data generated...")
    res_im_group = np.zeros((len(plot_index), 200, 200))
    #offset = 50
    for i in plot_index:
        print("Saving frame: ",i)
        gt = GT[i  , :200, :200]
        Grad_gt = Gradient(gt, 2)
        res_im_group[i-plot_index.min(), :, :] = Grad_gt

    np.savez(os.path.join(output_dir,"im_plot.npz"), res_im_group)
    print("Image data generated...")

indN_Tt = np.concatenate([np.arange(60,80),np.arange(140,160),\
                             np.arange(220,240),np.arange(300,320)])  # index of evaluation period


usr_nc_directory="generatedData/Users/jupyter-carl456/FP_GENN.nc"
ref_nc_directory="generatedData/Users/jupyter-carl456/ref.nc"
output_dir="generatedData/Users/jupyter-carl456/"
frames_index=np.arange(50,55)

processUserReconstruction(usr_nc_directory,ref_nc_directory,output_dir,indN_Tt,frames_index)