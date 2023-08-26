%G2 to Matlab test file
inputfile = 'Slope_Base.g2x';
runfile = [inputfile(1:length(inputfile)-8) 'RUN.g2x'];
runcommand = ['optumg2cmd ' runfile ' /log:logfile.m /echo'];

var{1} = '$X$';  

beta = 10:10:30;
X = 10./tand(beta);

for i = 1:length(beta)
    disp('beta = ')
    beta(i)
    oldstr = var{1};
    newstr = X(i);
    oldfile = inputfile;
    newfile = runfile;
    replacestr(oldstr,newstr,oldfile,newfile);
    dos(runcommand);
    res = resread('BEST STRENGTH REDUCTION FACTOR = ','logfile.m');
    FS(i) = res;
end;

