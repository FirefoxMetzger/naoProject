%% using data in format version 1
%load and format the data
T = readtable('meanPerGame_v1.csv');
T = table(T{:,1},T{:,2},str2double(T{:,3}),'VariableNames',T.Properties.VariableNames);
%do the ranova
rm = fitrm(T,'performance~game+user');
tbl1 = anova(rm);

%% using data in format version 2
T2 = readtable('meanPerGame_v2.csv');
T2 = table(T2{:,1},str2double(T2{:,2}),str2double(T2{:,3}),str2double(T2{:,4}),str2double(T2{:,5}),'VariableNames',T2.Properties.VariableNames);
W = table([1 2 3 4]','VariableNames',{'Games'});

rm2 = fitrm(T2,'game1-game4~1','WithinDesign',W);
tbl2 = ranova(rm2);

%% data version 3
%load and format the data
T3 = readtable('meanPerGame_v3.csv');
T3 = table(T3{:,1},T3{:,2},str2double(T3{:,3}),'VariableNames',T3.Properties.VariableNames);
%do the ranova
rm = fitrm(T3,'performance~game+user');
tbl3 = anova(rm)

num_games_max = 5;
m = zeros(num_games_max,1);
err = zeros(num_games_max,1);
for num_games = ['1' '2' '3' '4' '5' '6']
    idx = (cell2mat(T3{:,2}) == num_games);
    performance = T3{idx,3};
    m(str2double(num_games)) = mean(performance);
    err(str2double(num_games)) = std(performance)/sqrt(numel(performance));
end
errorbar(m,err)

