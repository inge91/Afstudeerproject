function DrawValues( values, map, varargin )
%DRAWVALUES Summary of this function goes here
%   Detailed explanation goes here
    
    color = 'y';
    if ~isempty(varargin); color = varargin{1}; end
    
    minVal = min(min(values));
    maxVal = max(max(values));
    
    for i=1:size(map,1)
        for j=1:size(map,2)
            s = (i-1)*size(map,2) + j;
            if map(i,j)==0
                f = fill([j-1 j j j-1],[i-1 i-1 i i],color);
                alpha(f,(values(s)-minVal)/(maxVal-minVal));
            end
        end
    end
    drawnow;
end

