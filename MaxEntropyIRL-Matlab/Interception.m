function Interception()
%clear; close all; clc;

global Feat;

isLearning = 0;

N = 50;
W = [0.1228 1.9574 0.37318 1 1 1 1 1 1];

[map, obst] = LoadMap('map4.txt');
% for me feature count is much higher size(W) is approximately 16
Feat = zeros([size(map),length(W)]);
size(map)

%    for j=1:size(Feat,2)
data_list = csvread("MapInfo.csv");
data_list = data_list(2:end, :);

for i=1:size(Feat,1)
    for j=1:size(Feat,2)
        Feat(i,j,:) = Features(data_list, i,j,map,obst);
    end
end


end
% Start gate and end gate might be problematic... Keep in mind.
%stGate = 1;
%enGate = 4;
%
%%Just draws the map
%DrawMap(map);
%set(gca,'YDir','normal');
%
%%loads in the path data
%load(['paths' num2str(stGate) 'to' num2str(enGate)]);
%path = paths{1};
%
%
%
%% Calculate expected feature counts
%f = 0;
%for t=1:length(path)
%    %x value
%    r = path(t,1);
%    %y value
%    c = path(t,2);
%    %TODO: What is this?
%    f = f + Features(r,c,map,obst,gates);
%end
%
%
%if ~isLearning
%    [policy, values] = ValueIterationLP(W',@GetPhi,@GetProb);
%    DrawValues(values,map,'k');
%    DrawPath(path);
%    return;
%end
%
%
%
%numStates = numel(map);
%
%while true
%    Zs = zeros(numStates,1);
%    terminal = Coor2State(gates(enGate,1), gates(enGate,2));
%    Za = zeros(numStates,4);
%
%
%
%    %1. Z_{s_terminal} = 1
%    Zs(terminal) = 1;
%
%
%    % Backward pass
%    for n=1:N
%        for i=1:numStates
%        %     Za(i,1) = exp()*Z(
%            [r,c] = State2Coor(i);
%            if map(r,c)==1; continue; end
%            reward = W * squeeze(Feat(r,c,:));
%            if c>1
%                k = Coor2State(r,c-1);
%                Za(i,1) = exp(reward) * Zs(k);
%            end
%            if r<14
%                k = Coor2State(r+1,c);
%                Za(i,2) = exp(reward) * Zs(k);
%            end
%            if c<14
%                k = Coor2State(r,c+1);
%                Za(i,3) = exp(reward) * Zs(k);
%            end
%            if r>1
%                k = Coor2State(r-1,c);
%                Za(i,4) = exp(reward) * Zs(k);
%            end
%
%            Zs(i) = sum(Za(i,:));
%            if i==terminal
%                Zs(i) = Zs(i)+1;
%            end
%        end
%    end
%
%
%    P = zeros(numStates, 4);
%
%    % 3. Local action probability computation
%    for i=1:numStates
%        if Zs(i)==0; continue; end
%        for j=1:4
%            P(i,j) = Za(i,j)/Zs(i);
%        end
%    end
%
%    % Forward pass
%    T = N;
%    Dt = zeros(numStates, T);
%    initial = Coor2State(gates(stGate,1), gates(stGate,2));
%    % 4. D_{s_{i,t}} = P(s_i=s_{initial}
%    Dt(initial, 1) = 1;
%
%    for t=1:T-1;
%        for k=1:numStates
%            [r,c] = State2Coor(k);
%            total = 0;
%            if c<14
%                i = Coor2State(r,c+1);
%                total = total + Dt(i,t)*P(i,1);
%            end
%            if r>1
%                i = Coor2State(r-1,c);
%                total = total + Dt(i,t)*P(i,2);
%            end
%            if c>1
%                i = Coor2State(r,c-1);
%                total = total + Dt(i,t)*P(i,3);
%            end
%            if r<14
%                i = Coor2State(r+1,c);
%                total = total + Dt(i,t)*P(i,4);
%            end
%
%            Dt(k,t+1) = total;
%        end
%    end
%
%    % Feature expectation
%    fe = 0;
%
%    % 6. Summing frequencies
%    D = zeros(numStates,1);
%    for i=1:numStates
%        D(i) = sum(Dt(i,:));
%        [r,c] = State2Coor(i);
%        fe = fe + D(i) * squeeze(Feat(r,c,:));
%    end
%
%    dL = (f-fe)/50;
%    W = W+dL';
%    
%    %debug report
%    disp(['dL:  ' num2str(dL')]);
%    
%    if abs(dL) < 1E-5; break;  end
%
%end
%
%
%
%disp(['W:  ' num2str(W)]);
%
%
%
%end
%
%
%

%Each element in the feature vector is the distance to obstacle or gate
%State is the coordinate location of the cell
function f = Features(data_list, i,j, map, obst)
    f = [];
    for l =5:13
        c = data_list(:,l);
        m = max(c);
        val = data_list(((i-1) * 50) + j, l);
        if val == -1;
            f = [f; 1];
        else
            f = [f; val/m];
        end
    end
end
%
%
%function s = Coor2State(i, j)
%    mapLength = 14;
%    s = (i-1)*mapLength + j;
%end
%
%function [i,j] = State2Coor(s)
%    mapLength = 14;
%    i = ceil(s/mapLength);
%    j = mod(s-1,mapLength) + 1;
%end
%
%
%
%
%
%function phi = GetPhi(s)
%    global Feat;
%    [r,c] = State2Coor(s);
%    phi = squeeze(Feat(r,c,:));
%end
%
%
%
%%works in state coords
%function P = GetProb(s)
%% finds proceeding states by going to each coordinate direction
%% calculates the probabilities for all actions and
%% returns a A by S probability matrix
%    mapLength = 14;
%    P = zeros(4,mapLength*mapLength);
%    i = ceil(s/mapLength);
%    j = mod(s-1,mapLength) + 1;
%
%    %get proceeding states
%    if j~=1;   nW = s - 1;
%    else   nW = s;    end
%    
%    if i~=1; nN = s - mapLength;
%    else nN = s; end
%    
%    if j~=mapLength;  nE = s + 1;
%    else nE = s; end
%    
%    if i~=mapLength;  nS = s + mapLength;
%    else nS = s; end
%    
%    % all actions are 1, is this because of having a deterministic markov model?
%    %specific action: gets extra 0.6 which adds up to 0.7
%    % action - West
%    P(1,nW) = 1;
%    % action - North
%    P(2,nN) = 1;
%    % action - East
%    P(3,nE) = 1;
%    % action - South
%    P(4,nS) = 1;
%end
