function DrawPath( path )
%DRAWPATH Summary of this function goes here
%   Detailed explanation goes here

    for t=1:length(path)
        x = path(t,2);
        y = path(t,1);
        f = fill([x-1 x x x-1],[y-1 y-1 y y],'r');
        alpha(f,t/(2*length(path))+0.3);
    end
    drawnow;
end

