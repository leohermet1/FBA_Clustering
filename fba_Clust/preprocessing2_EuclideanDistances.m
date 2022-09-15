cd('reduced_ZeroAndCorr/');
matfiles = dir('*.mat') ; 
N = length(matfiles) ; 
iwant = cell(N,1) ;  % to save output 
for i = 1:N
    disp(matfiles(i).name);
    load(matfiles(i).name);
    size(mydata);
    cd('../');
    NEDname = append('reduced_ZeroCorrEuc/EucDistances_',matfiles(i).name);
    AOSname = append('reduced_ZeroCorrEuc/ReducedBySol_',matfiles(i).name);
    CSname = append('reduced_ZeroCorrEuc/CentricSolution_',matfiles(i).name);
    ArrayOfSolutionsSortedByEuclideanDistances(mydata,NEDname,AOSname,CSname);
    cd('reduced_ZeroAndCorr/');
end
cd('..')