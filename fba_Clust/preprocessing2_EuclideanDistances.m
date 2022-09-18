% directory with all the matlab files
cd('reduced_ZeroAndCorr/');
% get all the patient's matrices
matfiles = dir('*.mat') ; 
N = length(matfiles) ; 
iwant = cell(N,1) ;  % to save output 
% browse each patient's matrices
for i = 1:N
    disp(matfiles(i).name);
    % load patient matrix
    load(matfiles(i).name);
    size(mydata);
    cd('../');
    NEDname = append('reduced_ZeroCorrEuc/EucDistances_',matfiles(i).name);
    AOSname = append('reduced_ZeroCorrEuc/ReducedBySol_',matfiles(i).name);
    CSname = append('reduced_ZeroCorrEuc/CentricSolution_',matfiles(i).name);
    % Save euclidean distances, array of solutions reduced and centric
    % solution points in the directory reduced_ZeroCorrEuc/
    ArrayOfSolutionsSortedByEuclideanDistances(mydata,NEDname,AOSname,CSname);
    % back to the directory with all the matlab files of the patient
    % matrices
    cd('reduced_ZeroAndCorr/');
end
cd('..')