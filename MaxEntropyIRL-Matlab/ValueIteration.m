function [p, varargout] = ValueIteration(W, GetPhi, GetProb, varargin)
%RL value iteration takes weights as input
% returns policy as output
% Params:
% GetPhi returns a vertical vector (K by 1)
% GetProb(s) returns A by N matrix, for each action returns the probabilities
% of going to other states from state s
% last input if you want to see the print outs
    tic;
    N = size(GetProb(1),2);
    V = zeros(N,1);
    if ~isempty(varargin) && ~isempty(varargin{1})
        V = varargin{1};
    end
    p = zeros(N,1);
    gamma = .99;
    thres = 1e-4;
    done = false;
    numiter = 0;

    while ~done
        numiter = numiter+1;
        oldV = V;
        for s=1:N
            prob = GetProb(s);
            y = gamma*prob*V;
            
            [ymax,yind] = max(y);
            reward = W'*GetPhi(s);
            V(s) = reward + ymax;
            p(s) = yind;
        end
        
        if abs(V - oldV) < thres; done = true; end
        
        %200 iterations is enough
        if numiter == 200; done = true; end
        if length(varargin)>1 && varargin{2}==1
            disp(['Iter: ' num2str(numiter) '  diff: ' num2str(max(abs(V - oldV)))]);
            drawnow;
        end

    end

    disp(['Num iterations: ' num2str(numiter)]);
    disp(['It took ' num2str(toc) ' seconds to run value iteration']);

    if length(varargin)>1 && varargin{2}==1
        str = '';
        for i=1:N-1
            str = [str num2str(p(i)) ', '];
        end
        str = [str num2str(p(i))];
        disp(['int[] policy = new int[]{' str '};']);
    end
    
    %optionally return the values
    varargout = {V};
end