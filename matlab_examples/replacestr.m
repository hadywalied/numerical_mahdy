%function replacestr(oldstr,newstr,file,newfile)

function replacestr(oldstr,newstr,oldfile,newfile)

if isstr(newstr) == 0
    newstr = num2str(newstr);
end;
A = fileread(oldfile);
I = strfind(A,oldstr);

for i = 1:length(I)
    I = strfind(A,oldstr);
    Ib = I(1);
    Ie = Ib+length(oldstr);
    B = [A(1:Ib-1) newstr A(Ie:length(A))];
    A = B;
end;

fid = fopen(newfile,'w');
fwrite(fid,A);
fclose(fid);