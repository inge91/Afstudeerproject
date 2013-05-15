function [map, obst] = LoadMap(mapfile)
%LOADMAP loads map and generates variables
%param: mapfile ie: map.txt
%output: map, in 2D array
%        obstacles, as a list
%        gates, clockwise list of gates starting from top-left
%        items, as a list

fid = fopen(mapfile);
mapSize = fscanf(fid,'%d %d',2);
map = fscanf(fid,'%d',[mapSize(2) mapSize(1)])';
fclose(fid);

[i,j] = find(map==1);
obst = [i j];
%[i,j] = find(map==-1);
%items = [i j];

%[i,j] = find([map(1,1:end);zeros(size(map,1)-1,size(map,2))] == 2);
%gates = [i j];
%[i,j] = find([zeros(size(map,1),size(map,2)-1) map(1:end,end)] == 2);
%gates = [gates; i j];
%[i,j] = find([zeros(size(map,1)-1,size(map,2));map(end,1:end)] == 2);
%gates = [gates; i j];
%[i,j] = find([map(1:end,1) zeros(size(map,1),size(map,2)-1)] == 2);
%gates = [gates; i j];


end

