%function R = resread(str,file)

function R = resread(str,file)

A = fileread(file);
I = strfind(A,str);
a = '';
length_of_I = length(I)
for i = 1:length(I)
    for j = 1:100
        a(j) = A(I(i)+length(str)+j-1);
        if length(str2num(a(j)))==0 & a(j)~='.' ...
          & a(j)~='-' & a(j)~='+' & a(j)~='E' & a(j)~='e'
            R(i,1) = str2num(a(1:j-1));
            a = '';
            break
        end;
    end;    
end;
