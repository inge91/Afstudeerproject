function [policy, varargout] = ValueIterationLP(W, GetPhi, GetProb, varargin)
%RL value iteration takes weights as input
% Returns policy as output
% Params:
%   GetPhi returns a vertical vector (K by 1)
%   GetProb(s) returns A by N matrix, for each action returns the probabilities
%   of going to other states from state s
%   last input if you want to see the print outs


tic;
[A,N] = size(GetProb(1));

gamma = .8;

%cplex = Cplex('lpex1');
%cplex.Model.sense = 'minimize';
%cplex.addCols(ones(N,1));   %objective as single column vector
% no bound since values are unconstrained

f = ones(N,1);
Amatrix = [];
b = [];

for s=1:N
    prob = GetProb(s);
    reward = W'*GetPhi(s);
    s
    for a=1:A
        %v(s) - \sum_{s'} gamma*P(s,s',a)*v(s) >= r(s)
        C = -gamma*prob(a,:);
        C(s) = C(s) + 1;
        
        Amatrix(end+1,:) = -C;
        b(end+1,:) = -reward;
        
%        cplex.addRows(reward, C, inf);
    end
end




% Optimize the problem
%cplex.solve();
[x,fval] = linprog(f,Amatrix,b);

%[x,fval,exitflag,output] = glpk(f,amatrix,b);


% Write the solution
%fprintf('\nSolution status = %s\n',cplex.Solution.statusstring);
%fprintf('Solution value = %f\n',cplex.Solution.objval);
%values = cplex.Solution.x';
fprintf('\nStatus = UNKNOWN, in N iterations\n');
fprintf('Solution value = %f\n',fval);
values = x';

policy = zeros(N,1);
for s=1:N
    [m,policy(s)] = max(sum(GetProb(s) .* repmat(values,A,1),2));
end

disp(['It took ' num2str(toc) ' seconds to solve the linear program']);

str = '';
for i=1:N-1
    str = [str num2str(values(i)) ', '];
end
str = [str num2str(values(i))];
disp(['Values: ' str]);



varargout = {values};

end
