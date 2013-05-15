function DrawMap( map, varargin )
%SHOWMAP Plots the map as a figure
%The map is plotted upside down
%Input map is composed of values:
%   0: empty cell
%   1: obstacle
%   2: gates
%  -1: extra cells that are dyed in yellow
fig = figure();
%set(gca,'YDir','reverse');
hold on;
axis([0 88 0 50]);
%axis square;
% axis equal;
set(fig,'Position',[1314 397 600 600]);


for i=0:size(map,2)
    plot([0 size(map,1)],[i i]);
end
for i=0:size(map,1)
    plot([i i],[0 size(map,2)]);
end
for i=1:size(map,2)
    for j=1:size(map,1)
        if map(j,i) == 1
            fill([j-1 j j j-1],[i-1 i-1 i i],'b');
        end
    end
end


end


% %this is the script to set obstacles on the map
% while true
%     showmap(map);
%     [x,y]=getpts();
%     x=ceil(x);
%     y=ceil(y);
%     for i=1:length(x)
%         map(y(i),x(i)) = 1;
%     end
%     save map map;
% end

% %this script is used to create paths and save them
% path = cell(6,1);
% %this is the script to set obstacles on the map
% for i=1:length(path2)
%     close all;
%     showmap(map);
%     [x,y]=getpts();
%     x=ceil(x);
%     y=ceil(y);
%     path{i} = [x y];
% end
% save path path;
