function mintexturepos = find_mindelta(texture, target, targetpos, patchsize, tol,overlap,imout)

sizetexture = size(texture);
sizetexture = sizetexture(1:2);

ssdarr_simple = zeros(sizetexture(1)-patchsize+1, sizetexture(2)-patchsize+1);
ssdarr_transfer = zeros(sizetexture(1)-patchsize+1,sizetexture(2)-patchsize+1);
ssdarr_all = zeros(sizetexture(1)-patchsize+1,sizetexture(2)-patchsize+1);

for i=1 : 1 : sizetexture(1)-patchsize+1;
   % fprintf('%d    \n',i)
    for j=1 : 1 : sizetexture(2)-patchsize+1;
        mpos = [i j];
        temp_transfer = get_ssd(texture, mpos, target, targetpos, patchsize);
        
        if temp_transfer == 0
            ssdarr_transfer(i, j) = 10000000000;
        else
            ssdarr_transfer(i, j) = temp_transfer;
        end
    end
end

if targetpos(1) ~= 1 && targetpos(2) ~= 1

    for i=1 : 1 : sizetexture(1)-patchsize+1;
    fprintf('%d    \n',i)
        for j=1 : 1 : sizetexture(2)-patchsize+1;

            mpos = [i j];
            temp_texture = ssd_patch(texture, patchsize, overlap, imout, mpos, targetpos-1);
            if temp_texture == 0
                ssdarr_simple(i, j) = 100000000;
            else
                ssdarr_simple(i, j) = temp_texture;
            end         
        end
    end
end

for i=1 : 1 : sizetexture(1)-patchsize+1;
   % fprintf('%d    \n',i)
    for j=1 : 1 : sizetexture(2)-patchsize+1;
         ssdarr_all(i,j) = 0.3*ssdarr_transfer(i,j) + 0.7*ssdarr_simple(i,j);
    end
end
        

minssd = min(min(ssdarr_all));
min_mat = repmat(minssd, size(ssdarr_all));
d_mat = min_mat*(1+tol) - ssdarr_all;
[temp_x, temp_y] = find(d_mat>0);

randindex = randperm(size(temp_x, 1) ,1);

mintexturepos = [ temp_x(randindex) temp_y(randindex) ];
