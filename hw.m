clear;
clc;
datestr(now)
texture = imread('img/texture-synthesis/texture3.jpg');
texture = double(texture);
patchsize = 50;
overlap = 3;
target = imread('img/texture-synthesis/target.jpg');
target = double(target);
tol = 0.1;

imout = texture_transfer(texture, target, patchsize, overlap, tol);
imout = imout / 255;
imshow(imout);
